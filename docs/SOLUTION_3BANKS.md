# SOLUTION FOUND: How the 3 Banks Work on AwoX ERCU_3groups_Zm

## Complete Understanding - Confirmed from Multiple Sources

### TL;DR - The Two-Part Mechanism

1. **Setup Phase**: Remote uses **Touchlink to bind** lights to Zigbee groups **0x800A, 0x800B, 0x800C** (32778, 32779, 32780)
2. **Operational Phase**: Buttons 1/2/3 switch which **groupID** is included in subsequent commands

## Part 1: Setup - Touchlink Binding (from Google AI / User Reports)

### The Pairing Process

**Group Assignment Procedure**:
1. Factory reset lights to be grouped
2. Power on ONLY the lights for the target group
3. Bring remote within 30cm (~1 foot) of the light(s)
4. **Press and hold group button (1, 2, or 3) for ~10 seconds**
5. Lights blink 3 times to confirm pairing

**What This Does**:
- Remote uses **Touchlink/LightLink** (cluster 0x1000) to commission lights
- Lights are added to a **Zigbee group** with specific ID:
  - Button 1 → Group ID **32778** (0x800A)
  - Button 2 → Group ID **32779** (0x800B)
  - Button 3 → Group ID **32780** (0x800C)
- This creates **direct bindings** between remote and lights
- Bindings persist in the lights' memory

### Why 0x8000+ Range?

Group IDs 32778-32780 (0x800A-0x800C) are in the **Touchlink group range**:
- 0x0001-0x7FFF: Standard Zigbee groups (coordinator-managed)
- 0x8000+: Touchlink/LightLink groups (peer-to-peer, device-managed)

This is why:
- Groups work **without coordinator routing**
- Commands go **directly to lights** via multicast
- ZHA coordinator may not see the traffic
- Setup is physical (proximity-based), not software

## Part 2: Operation - GroupID in Commands (from Zigbee2MQTT Source)

### Discovery from Zigbee2MQTT Source Code

Found in: https://github.com/Koenkk/zigbee-herdsman-converters

**The remote sends ALL control commands with a `groupID` field.**

From `src/devices/eglo.ts`:
```typescript
zigbeeModel: ["ERCU_3groups_Zm"],
model: "99099",
vendor: "EGLO",
description: "3 groups remote controller",
exposes: [
    e.action([...]),
    e.numeric("action_group", ea.STATE),  // <-- KEY: Exposes groupID
],
```

### How Commands Work

1. **User presses button 1** → Remote sets internal state: "current group = 1" (groupID = 32778)
2. **User presses ON** → Remote sends:
   - Command: ON
   - Destination: Multicast to group 32778
   - GroupID field: 32778
3. **Only lights in group 32778** receive and respond to the command

Same for buttons 2 and 3 with their respective group IDs.

### Implementation in Zigbee2MQTT

From `src/converters/fromZigbee.ts` and `src/lib/utils.ts`:

```typescript
// For EVERY command converter (on, off, step, etc.):
export const command_on: Fz.Converter = {
    convert: (model, msg, publish, options, meta) => {
        const payload = {action: "on"};
        addActionGroup(payload, msg, model);  // <-- Extracts groupID
        return payload;
    },
};

// The addActionGroup function:
export function addActionGroup(payload, msg, definition) {
    if (msg.groupID) {
        payload.action_group = msg.groupID;  // <-- From Zigbee message
    }
}
```

**Result**: Zigbee2MQTT exposes both:
- `action`: "on", "off", "red", "brightness_step_up", etc.
- `action_group`: 32778, 32779, or 32780

## Complete Picture: How It All Works Together

### The Full Workflow

1. **Initial Setup** (One-time):
   - User holds button 1 near Light A → Light A joins group 32778
   - User holds button 2 near Light B → Light B joins group 32779
   - User holds button 3 near Light C → Light C joins group 32780

2. **During Use**:
   - User presses button 1 → Remote remembers "use group 32778"
   - User presses ON → Command sent to group 32778 → Light A turns on
   - User presses button 2 → Remote remembers "use group 32779"
   - User presses ON → Command sent to group 32779 → Light B turns on
   - Light A stays on (not affected by commands to group 32779)

3. **What ZHA/Coordinator Sees**:
   - Commands with `dst_addressing.group` = 32778, 32779, or 32780
   - Multicast messages (not unicast to specific device)
   - GroupID in the Zigbee message structure

### Why "Unorthodox"

1. **Touchlink group IDs (0x8000+)** instead of standard groups (0x0001-0x7FFF)
2. **Physical pairing** (holding button near light) instead of software configuration
3. **Buttons 1/2/3 don't send commands** - they only change internal state
4. **Direct device-to-device** communication, may bypass coordinator
5. **GroupID in message header**, not in ZCL payload

This is different from:
- Standard Zigbee groups (coordinator-managed)
- Multiple endpoint remotes (IKEA style)
- Simple 3-button remotes (each button = separate device trigger)

## Implementation for ZHA

### Current Problem

The existing quirk (`quirks/eglo_ercu_awox.py`) only exposes:
```python
device_automation_triggers = {
    (SHORT_PRESS, TURN_ON): {COMMAND: COMMAND_ON, CLUSTER_ID: 6, ENDPOINT_ID: 1},
    # ...
}
```

Missing:
- ❌ GroupID (32778/32779/32780) not exposed
- ❌ No indication which bank is active
- ❌ Cannot filter automations by group

### Solution: Expose GroupID in Events

The quirk needs to:

1. **Extract groupID from Zigbee message**
   - Access message's destination addressing (`dst_addressing.group`)
   - Group IDs will be 32778 (0x800A), 32779 (0x800B), or 32780 (0x800C)

2. **Include groupID in ZHA events**
   - Add `group` or `action_group` field to event data
   - Map to human-readable: 32778 → "group_1", 32779 → "group_2", 32780 → "group_3"

3. **Custom cluster to capture group addressing**
   - Override message handling to extract group before processing
   - Pass group info through to event generation

### Implementation Approach

#### Step 1: Capture Group in Cluster Handler

```python
class AwoxRemoteCluster(CustomCluster):
    """Custom cluster to capture group addressing."""
    
    def handle_cluster_general_request(self, hdr, args, dst_addressing=None):
        """Intercept commands to extract group ID."""
        group_id = None
        if dst_addressing and hasattr(dst_addressing, 'group'):
            group_id = dst_addressing.group
            
        # Map Touchlink group IDs to logical groups
        group_map = {
            0x800A: 1,  # 32778 → Group 1
            0x800B: 2,  # 32779 → Group 2  
            0x800C: 3,  # 32780 → Group 3
        }
        logical_group = group_map.get(group_id)
        
        # Store for use in command handlers
        self._current_group = logical_group
        
        # Continue with normal processing
        return super().handle_cluster_general_request(hdr, args, dst_addressing)
```

#### Step 2: Include Group in Device Automation Triggers

**Option A**: Include in event data (requires HA core support)
```python
# In command handler
self.listener_event("zha_send_event", {
    "command": "turn_on",
    "group": self._current_group,  # 1, 2, or 3
})
```

**Option B**: Separate triggers per group (works with current HA)
```python
device_automation_triggers = {
    # Group 1
    (SHORT_PRESS, "turn_on_1"): {COMMAND: COMMAND_ON, GROUP: 0x800A, ...},
    (SHORT_PRESS, "turn_off_1"): {COMMAND: COMMAND_OFF, GROUP: 0x800A, ...},
    # Group 2
    (SHORT_PRESS, "turn_on_2"): {COMMAND: COMMAND_ON, GROUP: 0x800B, ...},
    (SHORT_PRESS, "turn_off_2"): {COMMAND: COMMAND_OFF, GROUP: 0x800B, ...},
    # Group 3
    (SHORT_PRESS, "turn_on_3"): {COMMAND: COMMAND_ON, GROUP: 0x800C, ...},
    (SHORT_PRESS, "turn_off_3"): {COMMAND: COMMAND_OFF, GROUP: 0x800C, ...},
}
```

This would create triggers like:
- `remote_button_short_press` with subtype `turn_on_1`
- `remote_button_short_press` with subtype `turn_on_2`
- `remote_button_short_press` with subtype `turn_on_3`

### User Setup Instructions

1. **Create ZHA Groups** in Home Assistant:
   - Group 32778 (0x800A) for bank 1
   - Group 32779 (0x800B) for bank 2
   - Group 32780 (0x800C) for bank 3

2. **Use Touchlink to pair lights**:
   - Factory reset lights
   - Power on only lights for target group
   - Hold remote button 1/2/3 near lights for 10 seconds
   - Lights blink 3 times to confirm

3. **Add lights to ZHA groups**:
   - In HA: Settings → Devices & Services → ZHA → Groups
   - Ensure lights are in correct groups (32778/32779/32780)

4. **Use in automations**:
   - Trigger on remote button presses with group filtering
   - Control lights via ZHA groups
   - Groups ensure synchronized response

### Blueprint Example

```yaml
trigger:
  - platform: device
    domain: zha
    device_id: !input remote
    type: remote_button_short_press
    subtype: turn_on_1  # Group 1
    id: "group1_on"
  - platform: device
    domain: zha
    device_id: !input remote
    type: remote_button_short_press
    subtype: turn_on_2  # Group 2
    id: "group2_on"

action:
  - choose:
      - conditions: [{condition: trigger, id: "group1_on"}]
        sequence:
          - service: light.turn_on
            target:
              area_id: !input area_group_1
      - conditions: [{condition: trigger, id: "group2_on"}]
        sequence:
          - service: light.turn_on
            target:
              area_id: !input area_group_2
```

## Testing & Validation

### Debug Commands

```yaml
# configuration.yaml
logger:
  logs:
    zigpy: debug
    homeassistant.components.zha: debug
```

### What to Look For

1. **Press button 1, then ON**:
   - Log should show: `group=32778` or `dst_addressing.group=0x800A`
   
2. **Press button 2, then ON**:
   - Log should show: `group=32779` or `dst_addressing.group=0x800B`
   
3. **Press button 3, then ON**:
   - Log should show: `group=32780` or `dst_addressing.group=0x800C`

### Verification Steps

1. ✓ Confirm group IDs appear in debug logs
2. ✓ Verify different buttons produce different group IDs
3. ✓ Check lights respond only to their assigned group
4. ✓ Test all control buttons with each group
5. ✓ Validate ZHA groups configuration matches

## Key Insights Summary

1. **Buttons 1/2/3 don't send commands** - they're stateful switches on the remote
2. **Setup is via Touchlink** - physical proximity pairing, not software config
3. **Group IDs are 0x800A/0x800B/0x800C** - Touchlink range, not standard groups
4. **GroupID is in message header** - not in ZCL command payload
5. **Commands are multicast** - sent to group, not individual devices
6. **ZHA must expose groupID** - currently missing from quirk
7. **Not "missing buttons"** - the functionality exists, just not exposed

## References

- **Zigbee2MQTT source**: https://github.com/Koenkk/zigbee-herdsman-converters
  - Device definition: `src/devices/eglo.ts`
  - Group handling: `src/lib/utils.ts` `addActionGroup`
  - Converters: `src/converters/fromZigbee.ts`
- **Google AI Overview**: Touchlink pairing procedure and group IDs
- **Zigbee Specification**: Touchlink/LightLink commissioning (cluster 0x1000)
- **Group ID Range**: 0x8000+ for Touchlink groups
