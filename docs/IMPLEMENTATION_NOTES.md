# Implementation Notes: Bank/Group Handling in Quirk

## Overview

The AwoX ERCU_3groups_Zm remote sends commands with a groupID embedded in the Zigbee message's destination addressing. This quirk intercepts these messages to extract the groupID and map it to the appropriate bank.

## Technical Approach

### Group ID to Bank Mapping

The remote uses Touchlink group IDs:
- Button 1 → Group ID **0x800A** (32778) → Bank 1
- Button 2 → Group ID **0x800B** (32779) → Bank 2
- Button 3 → Group ID **0x800C** (32780) → Bank 3

### Cluster Interception

We create custom cluster classes for all clusters that receive commands from the remote:

1. **AwoxOnOffCluster** - Intercepts ON/OFF commands
2. **AwoxScenesCluster** - Intercepts scene recall commands
3. **AwoxLevelControlCluster** - Intercepts brightness and refresh commands
4. **AwoxColorCluster** - Intercepts color and color temperature commands

Each custom cluster overrides `handle_cluster_request()` to:
1. Extract `group_id` from `dst_addressing.group`
2. Map the group_id to a logical bank number (1, 2, or 3)
3. Store the bank number in `self._current_bank`
4. Continue with normal command processing

### Device Automation Triggers

The `device_automation_triggers` dictionary is generated programmatically:

```python
# Base triggers without bank suffix
_base_triggers = {
    (SHORT_PRESS, TURN_ON): {...},
    (SHORT_PRESS, TURN_OFF): {...},
    # ... 22 total actions
}

# Generate 66 triggers (22 actions × 3 banks)
device_automation_triggers = {}
for (press_type, action), trigger_def in _base_triggers.items():
    for bank in [1, 2, 3]:
        action_with_bank = f"{action}_{bank}"
        trigger_with_bank = trigger_def.copy()
        trigger_with_bank["bank"] = bank
        device_automation_triggers[(press_type, action_with_bank)] = trigger_with_bank
```

This creates triggers like:
- `(SHORT_PRESS, "turn_on_1")` for Bank 1 ON
- `(SHORT_PRESS, "turn_on_2")` for Bank 2 ON
- `(SHORT_PRESS, "turn_on_3")` for Bank 3 ON
- etc.

## How ZHA Uses the Triggers

When a button is pressed:

1. Remote sends Zigbee command with `dst_addressing.group` = 0x800A/B/C
2. ZHA routes the command to the appropriate output cluster
3. Custom cluster's `handle_cluster_request()` extracts groupID
4. Maps groupID → bank number (1/2/3)
5. ZHA matches the command + bank to a trigger in `device_automation_triggers`
6. Fires the appropriate Home Assistant device automation trigger

## Limitations & Considerations

### Current Implementation

The current implementation stores `_current_bank` but relies on ZHA's standard trigger matching. ZHA will match commands based on:
- Command type (e.g., COMMAND_ON)
- Cluster ID
- Endpoint ID
- Parameters (if specified)

However, ZHA's standard matching **does not** automatically include groupID filtering.

### Full Implementation Would Require

For complete bank separation in ZHA, we would need to:

1. **Override event emission** in each cluster to include bank in the event data
2. **Modify trigger matching** to consider the bank field
3. **Or use ZHA core changes** to natively support groupID in events

### Current Workaround

The quirk generates 66 separate triggers with bank suffixes. In theory, ZHA should treat these as distinct triggers. However, **physical device testing is required** to confirm that:

1. GroupID is actually present in `dst_addressing.group`
2. ZHA properly routes commands to custom clusters
3. Trigger matching works correctly with bank suffixes

### Alternative Approach (If Needed)

If the current approach doesn't work, we can:

1. **Override `_handle_cluster_request_wrapper`** in the device class
2. **Manually emit ZHA events** with custom event data including bank
3. **Use event-based triggers** instead of device automation triggers

Example:
```python
def _handle_cluster_request_wrapper(self, *args, **kwargs):
    # Extract groupID from message
    # Emit custom event with bank info
    self.zha_send_event(
        "button_press",
        {
            "command": command_name,
            "bank": bank_number,
            "press_type": "short" or "long"
        }
    )
```

## Testing Requirements

To validate this implementation:

1. **Enable debug logging**:
   ```yaml
   logger:
     logs:
       zigpy: debug
       homeassistant.components.zha: debug
   ```

2. **Test each bank**:
   - Press button 1, then ON → Check logs for groupID 0x800A
   - Press button 2, then ON → Check logs for groupID 0x800B
   - Press button 3, then ON → Check logs for groupID 0x800C

3. **Verify trigger firing**:
   - Create test automations for each bank
   - Confirm correct automation triggers for each bank
   - Ensure no cross-bank activation

4. **Test all 66 trigger combinations**:
   - 22 actions × 3 banks
   - Short + long press where applicable

## Future Enhancements

1. **Add double-click support** - Requires timing logic in clusters
2. **Add hold/release tracking** - For smoother brightness/color transitions
3. **Optimize trigger generation** - Reduce code duplication
4. **Add configuration options** - Allow users to customize bank assignments

## References

- Zigpy documentation: https://github.com/zigpy/zigpy
- ZHA quirks: https://github.com/zigpy/zha-device-handlers
- Zigbee2MQTT implementation: https://github.com/Koenkk/zigbee-herdsman-converters
