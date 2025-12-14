# Using the Eglo/AwoX Blueprints

## Important Update: 3-Bank Functionality Not Working

**Current Status**: The 3-bank quirk (`Awox99099Remote3Banks`) does not actually work. Testing shows that pressing buttons 1/2/3 to select different banks does NOT generate different events in Home Assistant. All button presses generate identical events regardless of which bank is selected.

**Root Cause**: The quirk tries to extract bank information from `dst_addressing.group`, but this information either isn't present in the Zigbee messages or isn't being captured correctly by the current implementation.

**What This Means**:
- The basic quirk (`Awox99099Remote`) is now the default
- All buttons control the same set of lights
- Bank buttons (1/2/3) don't do anything in Home Assistant
- The 3-bank blueprints (`eglo_awox_3banks.yaml`) won't work

## Current Working Setup

### Blueprint to Use

Use either:
- `roos/eglo99099-blueprint.yaml` (recommended)
- `blueprints/eglo_awox_basic.yaml` (same functionality)

These blueprints work with the basic quirk and provide:
- Power control (ON/OFF)
- Brightness control (dim up/down, long press for min/max)
- Color control (red, green, blue)
- Color temperature control (warm/cold)
- Scene buttons (heart 1/2)
- Refresh button

### Setup Instructions

1. **Import the Blueprint**
   - Go to Settings → Blueprints → Import Blueprint
   - Use the file URL or copy the YAML content

2. **Create One Automation**
   - Name: "Eglo Remote - All Lights"
   - Select your remote device
   - Select the lights you want to control
   - Set brightness step (default 10%)

3. **Use the Remote**
   - All control buttons work
   - Bank buttons (1/2/3) currently have no effect in Home Assistant

## Future Work Needed

To make the 3-bank functionality work, someone needs to:

1. **Investigate the actual Zigbee messages**:
   - Enable ZHA debug logging
   - Press button 1, then a control button
   - Press button 2, then the same control button
   - Press button 3, then the same control button
   - Compare the raw Zigbee frames to see if/how bank info is transmitted

2. **Fix the quirk** to properly capture and emit bank-specific events

3. **Update the blueprints** once the quirk emits different events per bank

## Technical Details

The activity log shows identical events regardless of bank:
```
AwoX ERCU_3groups_Zm Step With On Off event was fired with parameters: 
{'step_mode': <StepMode.Up: 0>, 'step_size': 18, 'transition_time': 2}
```

This happens whether you press bank 1, 2, or 3 before the button. The event doesn't include any bank identifier.

## Troubleshooting

### Error: "device does not have trigger"
You tried to use the 3-bank blueprint, but the device is using the basic quirk. Solution: Use the basic blueprint instead.

### Buttons don't respond
1. Check remote has good batteries
2. Verify quirk is loaded: Device info should show `custom_components.eglo_remote_zha.eglo_ercu_awox.Awox99099Remote`
3. Check automation is enabled
4. Look at ZHA events to see if button presses are detected

### Wrong lights respond
The basic quirk only supports one set of lights. All buttons control the same lights.
