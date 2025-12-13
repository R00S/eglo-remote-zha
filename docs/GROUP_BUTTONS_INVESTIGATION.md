# Group Selector Buttons Investigation Guide

## Summary

The AwoX ERCU_3groups_Zm has physical buttons labeled **1, 2, 3** that select which group of lights to control. These buttons are **NOT currently mapped** in the quirk.

## What We Know

### Physical Button Layout
```
┌─────────────────────────────────┐
│  [1]    [2]    [3]              │  ← Group Selectors (NOT MAPPED)
├─────────────────────────────────┤
│  [ON]  [OFF]  [Colors] [Dim]... │  ← Control Buttons (MAPPED)
└─────────────────────────────────┘
```

### Expected Behavior
1. User presses button **1** to select Group 1
2. User presses **ON** → lights in Group 1 turn on
3. User presses button **2** to select Group 2  
4. User presses **ON** → lights in Group 2 turn on (Group 1 unaffected)

### Device Characteristics
- **Manufacturer**: AwoX
- **Model**: ERCU_3groups_Zm
- **Endpoint 1**: Standard ZHA with Groups cluster (0x0004)
- **Endpoint 3**: Proprietary profile (0x128F) with clusters 0xFF50, 0xFF51

## Investigation Steps

### Step 1: Enable Debug Logging

Add to Home Assistant `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    zigpy: debug
    homeassistant.components.zha: debug
    zhaquirks: debug
```

Restart Home Assistant.

### Step 2: Monitor ZHA Events

In Home Assistant:
1. Go to Developer Tools → Events
2. Listen to event type: `zha_event`
3. Press button **1** on the remote
4. Observe what event is generated (if any)
5. Repeat for buttons **2** and **3**

### Step 3: Check Home Assistant Logs

```bash
tail -f /config/home-assistant.log | grep -i "ercu\|awox\|group"
```

While watching logs:
1. Press button **1**
2. Press button **2**
3. Press button **3**

Look for:
- Group membership commands (add_group, remove_group, view_group)
- Commands with group_id parameters
- Commands on endpoint 3
- Any proprietary cluster commands

### Step 4: Test Control Button Behavior

1. Press button **1** (select Group 1)
2. Press **ON** button
3. Note any differences in the command sent
4. Press button **2** (select Group 2)
5. Press **ON** button again
6. Compare commands - do they differ? Is there a group_id?

### Step 5: Check ZHA Device Info

In Home Assistant:
1. Configuration → Devices & Services → ZHA
2. Find the Eglo remote
3. Click "Manage Zigbee Device"
4. View "Clusters" tab
5. Check Groups cluster (0x0004):
   - What commands are available?
   - Can you manually send group commands?

### Step 6: Test Zigbee Groups

If the remote uses standard Zigbee groups:

1. Create Zigbee groups in ZHA:
   - Group 0x0001 (group 1)
   - Group 0x0002 (group 2)
   - Group 0x0003 (group 3)

2. Add different lights to each group

3. Test if pressing 1/2/3 switches which group receives commands

## What to Look For

### Scenario A: No ZHA Events (Most Likely)

If pressing buttons 1/2/3 generates **no** ZHA events:
- The buttons are **stateful** - they change remote's internal state
- Commands from control buttons include group context
- Implementation: Need to capture the group ID parameter in control button commands
- May require packet sniffing to see full Zigbee messages

### Scenario B: Group Cluster Commands

If pressing buttons 1/2/3 sends group-related commands:
- Look for: `add_group`, `view_group`, or similar
- The remote is managing group membership
- Implementation: Map these commands as device automation triggers

### Scenario C: Endpoint 3 Activity

If pressing buttons 1/2/3 triggers endpoint 3:
- Look for commands on clusters 0xFF50 or 0xFF51
- This is proprietary AwoX functionality
- Implementation: Need to understand proprietary cluster commands

### Scenario D: Different Endpoints per Group

If different groups use different source endpoints:
- Check if button 1 commands come from endpoint X
- Check if button 2 commands come from endpoint Y
- Note: Device only has 2 endpoints, so this is unlikely

## Expected Findings

Based on typical 3-group remotes, most likely outcome:

**The buttons change group context without generating events**:
- Pressing 1/2/3 doesn't trigger device automations
- Instead, it changes which Zigbee group ID is included in subsequent commands
- Control buttons (ON, OFF, etc.) send commands with `group_id` parameter
- Current quirk doesn't capture or expose the group_id

**What needs to be done**:
1. Modify quirk to expose group_id from commands
2. Add device automation triggers that include group information
3. Update blueprint to handle multi-group scenarios

## Implementation Strategies

### Option 1: Group ID in Trigger Data

```python
# In quirk device_automation_triggers
(SHORT_PRESS, TURN_ON, GROUP_1): {
    COMMAND: COMMAND_ON, 
    CLUSTER_ID: 6, 
    ENDPOINT_ID: 1,
    PARAMS: {"group_id": 0x0001}
}
```

### Option 2: Separate Triggers per Group

```python
# Expose different trigger subtypes
(SHORT_PRESS, "turn_on_group_1"): {...}
(SHORT_PRESS, "turn_on_group_2"): {...}
(SHORT_PRESS, "turn_on_group_3"): {...}
```

### Option 3: Group Selector as Trigger

```python
# If buttons 1/2/3 do generate events
(SHORT_PRESS, "group_1"): {COMMAND: ..., CLUSTER_ID: 4, ...}
(SHORT_PRESS, "group_2"): {COMMAND: ..., CLUSTER_ID: 4, ...}
(SHORT_PRESS, "group_3"): {COMMAND: ..., CLUSTER_ID: 4, ...}
```

## Questions to Answer

1. **Do buttons 1/2/3 generate ZHA events?**
   - Yes → Map as triggers
   - No → They're stateful, need different approach

2. **What cluster handles group selection?**
   - Groups (0x0004) → Standard Zigbee implementation
   - 0xFF50/0xFF51 → Proprietary AwoX implementation
   - OnOff (0x0006) → Group ID in command parameters

3. **How are groups identified in commands?**
   - Explicit group_id parameter?
   - Different source endpoints?
   - Destination address changes?

4. **Can we see group context in current events?**
   - Check ZHA event logs for group_id fields
   - Compare events after pressing different group buttons

## Resources

- **User Manual**: https://www.eglo.com/media/wysiwyg/PDF/User_Guide_connect.z.pdf
- **Zigbee Groups Cluster Spec**: ZCL section 3.6
- **ZHA Event Documentation**: https://www.home-assistant.io/integrations/zha/#zha-events

## Testing Checklist

- [ ] Enable debug logging
- [ ] Monitor zha_event while pressing 1/2/3
- [ ] Check Home Assistant logs for group-related messages
- [ ] Test control buttons after selecting different groups
- [ ] Inspect Groups cluster in ZHA device management
- [ ] Create Zigbee groups and test if remote uses them
- [ ] Compare behavior with and without Zigbee groups configured
- [ ] Document all findings

## Next Steps After Testing

Once we understand how group selection works:

1. Update `quirks/eglo_ercu_awox.py` to map group buttons
2. Modify device_automation_triggers to include group context
3. Update `blueprints/eglo_awox_basic.yaml` for multi-group support
4. Document complete button mappings including groups
5. Test with physical device to validate implementation

---

**Status**: Awaiting physical device testing  
**Priority**: HIGH - This is core functionality of the device  
**Impact**: Without this, the "3groups" feature is completely non-functional
