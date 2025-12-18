# Installation Guide for AwoX ERCU_3groups_Zm with 3-Bank Support

This guide explains how to install and configure the AwoX ERCU_3groups_Zm remote with full 3-bank functionality in Home Assistant using ZHA.

## Prerequisites

- Home Assistant with ZHA integration installed
- HACS (Home Assistant Community Store) installed
- AwoX ERCU_3groups_Zm remote (Eglo Remote 2.0, Model 99099)

## Quick Start (3 Simple Steps!)

### Step 1: Install the Custom Quirk via HACS

#### Option A: Add as Custom Repository (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots menu (⋮) in the top right
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/R00S/eglo-remote-zha`
6. Select category: "Integration"
7. Click "Add"
8. Search for "Eglo Remote ZHA" in HACS
9. Click "Download"
10. Restart Home Assistant

#### Option B: Manual Installation

1. Download `quirks/eglo_ercu_awox_3banks.py` from this repository
2. Copy it to your Home Assistant configuration directory:
   ```
   /config/custom_zha_quirks/eglo_ercu_awox_3banks.py
   ```
3. Add to your `configuration.yaml`:
   ```yaml
   zha:
     custom_quirks_path: /config/custom_zha_quirks/
   ```
4. Restart Home Assistant

### Step 2: Pair the Remote with ZHA

1. Go to Settings → Devices & Services → ZHA
2. Click "Add Device"
3. Put the remote in pairing mode:
   - Hold buttons 1 + 2 together for ~10 seconds
   - Remote LED should blink to indicate pairing mode
4. Wait for Home Assistant to discover the remote
5. The remote should appear as "AwoX ERCU_3groups_Zm"

### Step 3: Configure the Blueprint

**No Touchlink or ZHA groups needed!** Just select your devices.

1. Go to Settings → Automations & Scenes → Blueprints
2. Click "Import Blueprint"
3. Enter the blueprint URL:
   ```
   https://github.com/R00S/eglo-remote-zha/blob/main/blueprints/eglo_awox_area_selection.yaml
   ```
4. Click "Preview" then "Import"

#### Create Area Selection Automation

1. Go to Settings → Automations & Scenes
2. Click "Create Automation" → "Use Blueprint"
3. Select "Eglo Remote - Area & Light Selection"
4. Configure:
   - **Remote**: Select your AwoX remote
   - **Default Area**: Select your primary area (e.g., "Living Room")
   - **Excluded Areas**: Optional - areas to skip when cycling
   - **Power Left Entity**: Optional - entity to toggle with power left button
   - **Helper Entities**: Select the 4 helper entities you created
   - **Timeout**: Set inactivity timeout (default 5 minutes)
5. Give it a name: "Eglo Remote - Area Control"
6. Save

#### Create Automations for Banks 2 and 3

Repeat the above steps for Banks 2 and 3, selecting different devices for each bank.

## That's It!

You're done! Press buttons **1**, **2**, or **3** on the remote to switch between banks, then use the control buttons (ON/OFF, colors, brightness, etc.) to control the selected devices.

**No complex setup needed!** Home Assistant handles everything.

## Usage

### Switching Between Banks

Press button **1**, **2**, or **3** on the remote to select which bank is active. The remote remembers your selection.

### Control Buttons

Once a bank is selected, use any control button:

**Power**:
- ON - Turn on devices
- OFF - Turn off devices

**Colors** (for lights):
- Red (short) - Set red color
- Red (long) - Set red at full brightness
- Green (short) - Set green color
- Green (long) - Set green at full brightness
- Blue (short) - Set blue color
- Blue (long) - Set blue at full brightness
- Cycle (short) - Enable colorloop effect
- Cycle (long) - Disable effects

**Brightness** (for lights):
- Dim UP (short) - Increase brightness by step
- Dim UP (long) - Set to 100%
- Dim DOWN (short) - Decrease brightness by step
- Dim DOWN (long) - Set to 1%

**Color Temperature** (for lights):
- Warm (short) - Step warmer
- Warm (long) - Set to warmest (454 mireds)
- Cold (short) - Step colder
- Cold (long) - Set to coldest (153 mireds)

**Scenes** (if configured):
- Heart 1 - Activate scene 1
- Heart 2 - Activate scene 2

**Special**:
- Refresh (short) - Toggle devices
- Refresh (long) - Custom action or update entity states

## Examples

### Example 1: 3 Rooms with Lights

**Bank 1** - Living Room:
- Target: `light.living_room_ceiling`, `light.living_room_lamp`
- Features: All enabled

**Bank 2** - Bedroom:
- Target: `light.bedroom_ceiling`, `light.bedside_lamp`
- Features: Power, brightness, temperature only

**Bank 3** - Kitchen:
- Target: `light.kitchen_ceiling`, `light.kitchen_under_cabinet`
- Features: Power and brightness only

### Example 2: Mixed Device Types

**Bank 1** - Entertainment:
- Target: `light.tv_backlight`, `switch.tv`, `media_player.living_room_tv`
- Features: Power only (ON/OFF for all)

**Bank 2** - Office:
- Target: `light.desk_lamp`, `switch.monitor`, `fan.desk_fan`
- Features: Power and brightness (lights get brightness, switches get on/off)

**Bank 3** - Garden:
- Target: `light.garden_path`, `light.garden_spotlights`, `switch.garden_fountain`
- Features: Power, scenes (different garden moods)

## Advanced Configuration

### Custom Refresh Actions

You can define custom actions for the long press on the refresh button:

```yaml
# In blueprint configuration
refresh_long_action:
  - service: script.turn_on
    target:
      entity_id: script.goodnight_routine
  - service: notify.mobile_app
    data:
      message: "Goodnight routine activated"
```

### Conditional Controls

Use Home Assistant conditions to control when features are available:

```yaml
# Only allow color changes during day
use_color_buttons: "{{ now().hour >= 6 and now().hour < 22 }}"
```

## Troubleshooting

### Remote not discovered by ZHA

- Try resetting the remote: Hold buttons 1 + 3 for 10 seconds
- Ensure you're using the enhanced quirk
- Check ZHA logs for errors

### Buttons don't respond

- Verify the automation is enabled
- Check automation traces to see if triggers are firing
- Enable debug logging to see Zigbee messages

### Only some buttons work

- Check that you've enabled the features in the blueprint configuration
- Verify device types support the commands (e.g., switches don't have brightness)

### Wrong bank activates

- Ensure you pressed the correct bank button (1, 2, or 3) before control buttons
- The remote remembers the last bank pressed

## Debug Logging

To see detailed Zigbee messages and groupID information:

```yaml
# configuration.yaml
logger:
  logs:
    zigpy: debug
    homeassistant.components.zha: debug
```

Check logs when pressing buttons to see:
- Command types
- Group IDs (should be 32778, 32779, or 32780)
- Any errors

## Benefits of This Approach

✅ **No complex Zigbee setup** - No Touchlink or ZHA groups needed
✅ **Control ANY device** - Not just Zigbee lights
✅ **Mix device types** - Lights, switches, fans, covers in same bank
✅ **Easy reconfiguration** - Change devices anytime in the blueprint
✅ **Full Home Assistant integration** - Use scenes, scripts, conditions
✅ **No proximity requirements** - Configure from anywhere
✅ **Works with cloud devices** - Even WiFi/cloud lights work!

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/R00S/eglo-remote-zha/issues
- Home Assistant Community: Tag posts with `#eglo-remote` and `#zha`

## Summary

You now have:
- ✅ 3 independent banks
- ✅ Control ANY Home Assistant device
- ✅ 13 control buttons per bank
- ✅ Short + long press support (22 actions per bank)
- ✅ 66 total unique trigger combinations
- ✅ Simple 3-step setup
- ✅ No Touchlink or ZHA groups needed!

Enjoy your fully functional 3-bank Eglo remote controlling any devices in your home!
