# Button-Group Analysis for AwoX ERCU_3groups_Zm

## Question 1: Which buttons send groupID and which don't?

### Buttons That INCLUDE GroupID (ALL 13 control buttons)

Based on Zigbee2MQTT source code analysis, **ALL 13 control buttons** send the groupID with their commands:

#### Power Controls
- ✅ **ON button** - sends `command_on` with groupID
- ✅ **OFF button** - sends `command_off` with groupID

#### Brightness Controls
- ✅ **Dim UP (short press)** - sends `command_step` with groupID
- ✅ **Dim UP (long press)** - sends `command_move` + `command_stop` with groupID
- ✅ **Dim DOWN (short press)** - sends `command_step` with groupID
- ✅ **Dim DOWN (long press)** - sends `command_move` + `command_stop` with groupID

#### Color Controls (AwoX Custom)
- ✅ **Red button** - sends `awox_color` command with groupID
- ✅ **Green button** - sends `awox_color` command with groupID
- ✅ **Blue button** - sends `awox_color` command with groupID
- ✅ **Cycle/Refresh colored** - sends `awox_refreshColored` with groupID

#### Scene Controls
- ✅ **Heart 1 button** - sends `command_recall` (scene_id=1) with groupID
- ✅ **Heart 2 button** - sends `command_recall` (scene_id=2) with groupID

#### Color Temperature Controls
- ✅ **Warm (short press)** - sends `command_step_color_temperature` with groupID
- ✅ **Warm (long press)** - sends `command_move_to_color_temp` with groupID
- ✅ **Cold (short press)** - sends `command_step_color_temperature` with groupID
- ✅ **Cold (long press)** - sends `command_move_to_color_temp` with groupID

#### Special Functions
- ✅ **Refresh button** - sends `awox_refresh` command with groupID

### Buttons That DO NOT Send Commands

#### Group Selector Buttons (Stateful Only)
- ❌ **Button 1** - No command sent, changes internal state to group 32778 (0x800A)
- ❌ **Button 2** - No command sent, changes internal state to group 32779 (0x800B)
- ❌ **Button 3** - No command sent, changes internal state to group 32780 (0x800C)

These buttons are **invisible to Zigbee** - they only change the remote's internal memory of which group is selected.

## Question 2: Can the quirk emulate these as different buttons?

**YES!** The quirk can (and should) expose separate triggers for each group combination.

### Implementation Strategy

Since **ALL control buttons** include the groupID, we can create separate device automation triggers for each button × group combination.

#### Option A: Explicit Group Suffixes (Recommended)

Create separate trigger subtypes like:
```python
device_automation_triggers = {
    # ON button - 3 variants (one per group)
    (SHORT_PRESS, "turn_on_1"): {COMMAND: COMMAND_ON, GROUP: 0x800A, ...},
    (SHORT_PRESS, "turn_on_2"): {COMMAND: COMMAND_ON, GROUP: 0x800B, ...},
    (SHORT_PRESS, "turn_on_3"): {COMMAND: COMMAND_ON, GROUP: 0x800C, ...},
    
    # OFF button - 3 variants
    (SHORT_PRESS, "turn_off_1"): {COMMAND: COMMAND_OFF, GROUP: 0x800A, ...},
    (SHORT_PRESS, "turn_off_2"): {COMMAND: COMMAND_OFF, GROUP: 0x800B, ...},
    (SHORT_PRESS, "turn_off_3"): {COMMAND: COMMAND_OFF, GROUP: 0x800C, ...},
    
    # Red button - 3 variants
    (SHORT_PRESS, "red_1"): {COMMAND: COMMAND_AWOX_COLOR, GROUP: 0x800A, ...},
    (SHORT_PRESS, "red_2"): {COMMAND: COMMAND_AWOX_COLOR, GROUP: 0x800B, ...},
    (SHORT_PRESS, "red_3"): {COMMAND: COMMAND_AWOX_COLOR, GROUP: 0x800C, ...},
    
    # ... and so on for ALL control buttons
}
```

This would result in triggers like:
- `remote_button_short_press` with subtype `turn_on_1`
- `remote_button_short_press` with subtype `turn_on_2`
- `remote_button_short_press` with subtype `turn_on_3`
- etc.

**Total triggers**: 13 control buttons × 3 groups = **39 separate triggers**

#### Benefits of This Approach

1. **Easy to use in automations**: Each button+group combo is a distinct trigger
2. **Clear in UI**: User sees "turn_on_1", "turn_on_2", "turn_on_3" as separate options
3. **Works with existing Home Assistant**: No core changes needed
4. **Blueprints can filter by group**: Easy to create group-specific automations

#### Implementation in Quirk

The quirk needs to:

1. **Intercept commands at cluster level**:
   ```python
   class AwoxRemoteCluster(CustomCluster):
       def handle_cluster_general_request(self, hdr, args, dst_addressing=None):
           # Extract groupID from dst_addressing
           group_id = dst_addressing.group if dst_addressing else None
           
           # Map to logical group
           group_map = {0x800A: 1, 0x800B: 2, 0x800C: 3}
           logical_group = group_map.get(group_id, 1)  # Default to 1
           
           # Store for event generation
           self._current_group = logical_group
           
           # Continue processing
           return super().handle_cluster_general_request(hdr, args, dst_addressing)
   ```

2. **Generate appropriate trigger**:
   ```python
   # When generating event, append group suffix
   action = f"{base_action}_{self._current_group}"
   # e.g., "turn_on_1", "turn_on_2", "turn_on_3"
   ```

3. **Register all combinations**:
   ```python
   for group in [1, 2, 3]:
       for base_action in ["turn_on", "turn_off", "red", "green", ...]:
           device_automation_triggers[(SHORT_PRESS, f"{base_action}_{group}")] = {
               COMMAND: ...,
               GROUP: group_to_hex_map[group],
               ...
           }
   ```

### Blueprint Usage Example

```yaml
trigger:
  - platform: device
    domain: zha
    device_id: !input remote
    type: remote_button_short_press
    subtype: turn_on_1  # Group 1 ON
    id: "group1_on"
    
  - platform: device
    domain: zha
    device_id: !input remote
    type: remote_button_short_press
    subtype: turn_on_2  # Group 2 ON
    id: "group2_on"
    
  - platform: device
    domain: zha
    device_id: !input remote
    type: remote_button_short_press
    subtype: turn_on_3  # Group 3 ON
    id: "group3_on"

action:
  - choose:
      - conditions: [{condition: trigger, id: "group1_on"}]
        sequence:
          - service: light.turn_on
            target:
              entity_id: light.living_room_group1
              
      - conditions: [{condition: trigger, id: "group2_on"}]
        sequence:
          - service: light.turn_on
            target:
              entity_id: light.living_room_group2
              
      - conditions: [{condition: trigger, id: "group3_on"}]
        sequence:
          - service: light.turn_on
            target:
              entity_id: light.living_room_group3
```

## Summary

### Answer 1: Button-GroupID Matrix

| Button Category | Buttons | Include GroupID? | Count |
|----------------|---------|------------------|-------|
| Power | ON, OFF | ✅ YES | 2 |
| Brightness | Dim Up, Dim Down | ✅ YES | 2 |
| Colors | Red, Green, Blue, Cycle | ✅ YES | 4 |
| Scenes | Heart 1, Heart 2 | ✅ YES | 2 |
| Temperature | Warm, Cold | ✅ YES | 2 |
| Special | Refresh | ✅ YES | 1 |
| **Subtotal Control** | | | **13** |
| **Group Selectors** | **1, 2, 3** | ❌ **NO** (stateful only) | **3** |
| **TOTAL** | | | **16 buttons** |

**Result**: 13 control buttons × 3 groups = **39 possible button+group combinations**

### Answer 2: Emulation Strategy

**YES**, the quirk can emulate these as different buttons by:
1. Extracting groupID from `dst_addressing.group` 
2. Creating separate triggers with group suffix (e.g., `turn_on_1`, `turn_on_2`, `turn_on_3`)
3. Registering 39 device automation triggers total (13 control buttons × 3 groups)
4. Users get button+group combos as distinct automation triggers

This provides the best user experience - each physical button press with a group context appears as a unique trigger in Home Assistant.
