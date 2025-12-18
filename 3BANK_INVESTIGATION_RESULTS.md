# 3-Bank Functionality Investigation Results

## Summary

The bank selector buttons (1/2/3) on the AwoX ERCU_3groups_Zm remote **do not send Zigbee commands that Home Assistant can detect**. Therefore, the 3-bank quirk cannot provide bank-specific events or triggers.

## Debug Output Analysis

When pressing buttons after selecting different banks, the debug logs showed:

```
AwoxOnOffCluster: cmd_id=1, dst_addressing=None, has_group=False, group=None
AwoxLevelControlCluster: cmd_id=X, dst_addressing=None, has_group=False, group=None
```

**Key Finding**: `dst_addressing=None` - The groupID/bank information is NOT present in the Zigbee frames received by Home Assistant.

## Why Bank Buttons Don't Work

According to the remote's design and documentation:

1. **Buttons 1/2/3 are stateful only** - They change the remote's internal state but don't send Zigbee commands
2. **Touchlink/LightLink implementation** - The remote uses direct device-to-device bindings
3. **Commands bypass coordinator** - Control commands may go directly to bound lights
4. **Firmware-level operation** - Bank selection happens inside the remote's firmware

## What This Means for Home Assistant

### Cannot Be Implemented:
- ❌ Detecting which bank is currently selected
- ❌ Emitting bank-specific events (e.g., `dim_up_1`, `dim_up_2`, `dim_up_3`)
- ❌ Separate automations per bank
- ❌ Bank selection as an automation trigger

### Can Be Implemented:
- ✅ Basic remote control (on/off, brightness, colors, temperature)
- ✅ All control buttons work correctly
- ✅ Single automation for all remote buttons

## Recommendation

**Use the basic quirk (`Awox99099Remote`)** instead of the 3-bank quirk. The basic quirk provides:
- All control button functionality
- Reliable event emission  
- Simpler configuration
- No false expectations about bank support

The 3-bank quirk (`Awox99099Remote3Banks`) should be considered **experimental/non-functional** because it cannot deliver the promised functionality.

## Technical Details

### How the Remote Actually Works

1. **Setup Phase** (done once):
   - User holds button 1/2/3 near lights for 10 seconds
   - Remote creates Touchlink binding for that bank
   - Lights store the groupID (32778, 32779, or 32780)

2. **Operational Phase**:
   - User presses button 1/2/3 (no Zigbee command sent)
   - Remote's firmware switches active binding
   - Control buttons send commands with groupID header
   - Commands go directly to bound lights
   - **Coordinator may not see the commands at all**

### Why This is "Unorthodox"

- Uses Touchlink bindings instead of coordinator-managed groups
- Direct device-to-device communication
- GroupID in message header, not ZCL payload
- Bank selection is hardware-level, not protocol-level

## Alternative Approach (Not Recommended)

It might be theoretically possible to:
1. Track which bank button was pressed last (if they DO send events)
2. Store that in device state
3. Emit different triggers based on stored bank

However, since `dst_addressing=None`, this approach won't work either. The remote truly doesn't send distinguishable commands for different banks to the coordinator.

## Conclusion

The 3-bank functionality is a **hardware/firmware feature** that operates at the Touchlink/LightLink layer, below what Home Assistant/ZHA can observe or control. 

**Users should use the basic quirk and understand that bank selection affects the physical lights (via direct bindings) but cannot be detected or automated in Home Assistant.**

The original vision of having 66 separate triggers (22 actions × 3 banks) is not achievable with this hardware design.

## Next Steps

1. Revert to using the basic quirk (`Awox99099Remote`) as default
2. Update documentation to explain the limitations
3. Remove the 3-bank blueprint or mark it as non-functional
4. Focus documentation on the Touchlink setup process for users who want physical 3-bank control
