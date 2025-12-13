# Installation Guide for AwoX ERCU_3groups_Zm with 3-Bank Support

This guide explains how to install and configure the AwoX ERCU_3groups_Zm remote with full 3-bank functionality in Home Assistant using ZHA.

## Prerequisites

- Home Assistant with ZHA integration installed
- HACS (Home Assistant Community Store) installed
- AwoX ERCU_3groups_Zm remote (Eglo Remote 2.0, Model 99099)

## Installation Steps

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

### Step 3: Create ZHA Groups for 3-Bank Support

The remote uses specific Zigbee group IDs for its 3 banks:
- Bank 1: Group ID **32778** (0x800A)
- Bank 2: Group ID **32779** (0x800B)
- Bank 3: Group ID **32780** (0x800C)

**Create the groups:**

1. Go to Settings → Devices & Services → ZHA
2. Click on the "Groups" tab
3. Click "Add Group"
4. For each bank:
   - Name: "Bank 1" (or "Bank 2", "Bank 3")
   - Group ID: Enter **32778** (or 32779, 32780)
   - Click "Add"

### Step 4: Assign Lights to Banks using Touchlink

The remote uses Touchlink to bind lights directly to each bank. This creates a direct Zigbee connection between the remote and the lights.

**For each bank:**

1. **Factory reset the lights** you want to assign to this bank:
   - Power cycle 5-6 times (on for 2 seconds, off for 2 seconds)
   - Or use the AwoX app to remove them
   - Lights should flash to confirm reset

2. **Power on ONLY the lights** for the target bank

3. **Bring the remote within 30cm** (~1 foot) of the lights

4. **Press and hold the bank button** (1, 2, or 3) for ~10 seconds:
   - Remote LED will flash
   - Lights will blink 3 times to confirm pairing

5. **Test the pairing:**
   - Press button 1 (or 2, or 3) on the remote
   - Press the ON button
   - The lights should turn on

6. **Repeat for other banks** with different lights

### Step 5: Install the Blueprint

1. Go to Settings → Automations & Scenes → Blueprints
2. Click "Import Blueprint"
3. Enter the blueprint URL:
   ```
   https://github.com/R00S/eglo-remote-zha/blob/main/blueprints/eglo_awox_3banks.yaml
   ```
4. Click "Preview" then "Import"

### Step 6: Create Automations from Blueprint

Create one automation per bank:

#### Bank 1 Automation

1. Go to Settings → Automations & Scenes
2. Click "Create Automation" → "Use Blueprint"
3. Select "Eglo/AwoX Remote 3-Bank Control (ZHA)"
4. Configure:
   - **Remote**: Select your AwoX remote
   - **Bank Number**: Select "Bank 1"
   - **Target Lights**: Select the lights you paired to bank 1
   - **Enable features**: Check the controls you want to use
   - **Adjust settings**: Brightness step, color temp step, etc.
5. Give it a name: "Eglo Remote - Bank 1"
6. Save

#### Bank 2 and 3 Automations

Repeat the above steps for Banks 2 and 3 with their respective lights.

## Verification

### Test Bank Selection

1. Press button **1** on the remote
2. Press **ON** → Bank 1 lights should turn on
3. Press **OFF** → Bank 1 lights should turn off

4. Press button **2** on the remote
5. Press **ON** → Bank 2 lights should turn on (Bank 1 stays off)
6. Press **OFF** → Bank 2 lights should turn off

5. Press button **3** on the remote
6. Press **ON** → Bank 3 lights should turn on
7. Press **OFF** → Bank 3 lights should turn off

### Test All Control Buttons

For each bank, test:
- ✓ ON/OFF buttons
- ✓ Brightness up/down (short + long press)
- ✓ Color buttons (red, green, blue, cycle)
- ✓ Color temperature (warm, cold)
- ✓ Scene buttons (heart 1, heart 2)
- ✓ Refresh button

## Troubleshooting

### Remote not discovered by ZHA

- Try resetting the remote: Hold buttons 1 + 3 for 10 seconds
- Ensure you're using the enhanced quirk
- Check ZHA logs for errors

### Lights don't respond to bank buttons

- Verify ZHA groups are created with correct IDs (32778, 32779, 32780)
- Re-do the Touchlink pairing procedure
- Ensure only target lights are powered on during pairing
- Hold bank button close to lights (< 30cm) for full 10 seconds

### Only some buttons work

- Check that you've enabled the features in the blueprint configuration
- Verify the automation is running (check automation traces)
- Enable ZHA debug logging to see if commands are received

### Commands affect wrong lights

- Verify you pressed the correct bank button (1, 2, or 3) before control buttons
- Check that lights are properly assigned to ZHA groups
- Re-do Touchlink pairing if needed

## Debug Logging

To see detailed Zigbee messages and groupID information:

```yaml
# configuration.yaml
logger:
  logs:
    zigpy: debug
    homeassistant.components.zha: debug
```

After enabling, check the logs when pressing buttons to see:
- Group ID in messages (should be 32778, 32779, or 32780)
- Command types
- Any errors

## Advanced Configuration

### Custom Actions per Bank

You can create custom automations that react to specific button+bank combinations:

```yaml
trigger:
  - platform: device
    domain: zha
    device_id: <your_remote_id>
    type: remote_button_short_press
    subtype: "red_1"  # Red button on bank 1

action:
  - service: scene.turn_on
    target:
      entity_id: scene.movie_mode
```

### Using with Node-RED

The 66 separate triggers are also available in Node-RED:
- Use the "Events: state" node
- Filter by device
- Look for `zha_event` events
- Check the `command` and `bank` fields

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/R00S/eglo-remote-zha/issues
- Home Assistant Community: Tag posts with `#eglo-remote` and `#zha`

## Summary

You now have:
- ✅ 3 independent banks/groups
- ✅ 13 control buttons per bank
- ✅ Short + long press support (22 actions per bank)
- ✅ 66 total unique trigger combinations
- ✅ Direct Zigbee control via Touchlink
- ✅ Flexible automation via blueprints

Enjoy your fully functional 3-bank Eglo remote!
