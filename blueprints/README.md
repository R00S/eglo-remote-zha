# Eglo Remote Blueprints

This directory contains Home Assistant blueprints for Eglo remote controls using ZHA.

## Available Blueprints

### 🎯 Recommended: Area & Light Selection (`eglo_awox_area_selection.yaml`)

**Import URL:**
```
https://github.com/R00S/eglo-remote-zha/blob/main/blueprints/eglo_awox_area_selection.yaml
```

**Features:**
- Intelligent area cycling with Candle Mode button
- Individual light selection with Colour Middle button
- Visual feedback via light blinks
- Save/recall default states
- Configurable timeout with auto-reset
- Control ANY Home Assistant light entities
- Only ONE automation needed per remote

**Supported Devices:**
- AwoX ERCU_3groups_Zm (99099 Remote)

**Button Functions:**
- **Power Left**: Toggle configured entity
- **Power Right**: Toggle selected area/light
- **Colour Middle (short)**: Cycle through lights in area
- **Colour Middle (long)**: Save current state as default
- **Candle Mode**: Cycle through areas
- **Colour Top/Left/Right**: Set colors or adjust color temperature
- **Dimming**: Adjust brightness
- **White Tone**: Adjust color temperature
- **Favourites**: Recall saved states

**Required Setup:**
1. Create 4 helper entities (input_select, input_text, input_datetime)
2. Import blueprint
3. Configure default area and helpers
4. Done!

### 2. Basic 3-Group Control (`eglo_3group_basic.yaml`)

**Features:**
- Controls 3 separate light groups (one per remote button group)
- Short press: Turn on/off at 100% brightness
- Long press: Continuous brightness adjustment (up/down)
- Long release: Stop brightness adjustment
- Configurable brightness step percentage

**Supported Devices:**
- Eglo ERCU_3groups_Zm (TS004F / _TZ3000_4fjiwweb)

**How to Use:**
1. Import the blueprint to Home Assistant
2. Create a new automation from the blueprint
3. Select your Eglo remote device
4. Assign light entities or groups to each of the 3 groups
5. Adjust brightness step if desired (default: 10%)

**Button Mapping:**
- **Buttons 1 & 2** (left): Control Light Group 1
- **Buttons 3 & 4** (middle): Control Light Group 2
- **Buttons 5 & 6** (right): Control Light Group 3

Top buttons turn on/brighten, bottom buttons turn off/dim.

## Installing Blueprints

### Method 1: Direct Import (Recommended)

1. Navigate to **Configuration** → **Blueprints** in Home Assistant
2. Click **Import Blueprint**
3. Paste this URL for Area Selection blueprint:
   ```
   https://github.com/R00S/eglo-remote-zha/blob/main/blueprints/eglo_awox_area_selection.yaml
   ```
4. Click **Preview** then **Import**

### Method 2: File System

1. Copy the blueprint YAML file to:
   ```
   /config/blueprints/automation/eglo/
   ```
2. Restart Home Assistant
3. The blueprint will appear in the automation editor

## Creating Your Own Blueprint

Want to create a custom blueprint for your use case? Here's a template:

```yaml
blueprint:
  name: My Eglo Blueprint
  description: Custom automation for Eglo remote
  domain: automation
  input:
    remote:
      name: Eglo Remote
      selector:
        device:
          integration: zha
          manufacturer: _TZ3000_4fjiwweb
          model: TS004F
    # Add your custom inputs here

trigger:
  - platform: device
    domain: zha
    device_id: !input remote
    type: remote_button_short_press
    subtype: button_1
    id: "button_1_short"
  # Add more triggers as needed

action:
  - choose:
      - conditions:
          - condition: trigger
            id: "button_1_short"
        sequence:
          # Your action here
```

### Available Trigger Types

For each button (1-6), you can use:
- `remote_button_short_press`
- `remote_button_long_press`
- `remote_button_long_release`

## Blueprint Ideas (Contributions Welcome!)

Future blueprints we'd like to see:

- **Scene Control**: Recall different scenes with each button
- **Color Cycling**: Cycle through colors with long press
- **Room Control**: Control multiple rooms/zones
- **Advanced Dimming**: Exponential dimming curves
- **Mode Switching**: Switch between automation modes
- **Media Control**: Control media players
- **Macro Actions**: Complex multi-step actions per button

## Contributing Blueprints

Have a useful blueprint? Share it with the community!

1. Test your blueprint thoroughly
2. Add clear descriptions and comments
3. Document all inputs and their purposes
4. Submit a pull request with your blueprint
5. Update this README with your blueprint description

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

## Troubleshooting Blueprints

### Blueprint Not Importing
- Check YAML syntax with an online validator
- Ensure the blueprint domain is set to `automation`
- Verify all required fields are present

### Device Not Appearing in Selector
- Ensure your Eglo remote is paired with ZHA
- Check that the quirk is properly loaded
- Verify manufacturer and model match the blueprint filter
- Try restarting Home Assistant

### Automation Not Triggering
- Check that the remote's battery is good
- Test the device triggers manually in the automation editor
- View the ZHA event log to see if button presses are detected
- Enable debug logging to diagnose issues

### Brightness Control Issues
- Ensure your lights support brightness control
- Check that the lights are on before dimming
- Adjust the brightness step percentage if changes are too large/small
- Some lights may not respond well to rapid brightness changes

## Support

For blueprint-specific issues:
1. Check this README first
2. Search existing GitHub issues
3. Create a new issue with:
   - Blueprint name and version
   - Home Assistant version
   - Description of the problem
   - Relevant logs or error messages

---

**Note**: These blueprints are designed for ZHA. For Zigbee2MQTT blueprints, check other community resources.
