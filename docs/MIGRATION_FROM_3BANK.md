# Migration Guide: From 3-Bank System to Area/Light Selection

## Overview

Version 0.1.0 introduces a **major architectural change** that replaces the manual 3-bank workaround system with an intelligent **Area/Light Selection System**.

**Breaking Changes:**
- All 3-bank quirks and blueprints have been removed
- Automations using `*_1`, `*_2`, `*_3` bank suffixes will no longer work
- New helper entities are required
- Different button behaviors

## Why This Change?

The new system provides:
- ✅ **Intuitive operation** - No manual bank switching
- ✅ **Visual feedback** - Lights blink to show selection
- ✅ **Auto-timeout** - Returns to default after inactivity
- ✅ **Easier setup** - Just select areas, no complex configuration
- ✅ **More flexible** - Control any combination of areas and lights

## Migration Steps

### Step 1: Backup Your Current Setup

Before upgrading:
1. Document your current automation configurations
2. Note which devices are in which banks
3. Take screenshots of your automation settings

### Step 2: Update the Integration

1. Update via HACS or manually to version 0.1.0+
2. Restart Home Assistant
3. Verify the integration loads without errors in the logs

### Step 3: Remove Old Automations

Delete all automations created from the old 3-bank blueprints:
- Any automations with triggers like `turn_on_1`, `turn_on_2`, `turn_on_3`
- Automations from `eglo_awox_3banks.yaml` blueprint
- Automations from `eglo_awox_manual_bank.yaml` blueprint

**Note:** You can keep automations using the basic `eglo_awox_basic.yaml` blueprint if desired.

### Step 4: Create Helper Entities

You need to create 4 helper entities for the new system:

#### 4.1: Current Area Helper (input_select)

1. Settings → Devices & Services → Helpers → Create Helper
2. Select "Dropdown"
3. Name: `Eglo Remote Current Area`
4. Icon: `mdi:floor-plan`
5. Options: Leave empty or add your area names (will be auto-populated)

Entity ID: `input_select.eglo_remote_current_area`

#### 4.2: Current Light Helper (input_select)

1. Settings → Devices & Services → Helpers → Create Helper
2. Select "Dropdown"
3. Name: `Eglo Remote Current Light`
4. Icon: `mdi:lightbulb`
5. Options: `all` (just one option is fine, will be updated automatically)

Entity ID: `input_select.eglo_remote_current_light`

#### 4.3: Default Area Helper (input_text)

1. Settings → Devices & Services → Helpers → Create Helper
2. Select "Text"
3. Name: `Eglo Remote Default Area`
4. Icon: `mdi:home-floor-0`
5. Mode: `Text`

Entity ID: `input_text.eglo_remote_default_area`

#### 4.4: Last Activity Helper (input_datetime)

1. Settings → Devices & Services → Helpers → Create Helper
2. Select "Date and/or time"
3. Name: `Eglo Remote Last Activity`
4. Icon: `mdi:clock-outline`
5. Date: ✅ Enable
6. Time: ✅ Enable

Entity ID: `input_datetime.eglo_remote_last_activity`

### Step 5: Import the New Blueprint

1. Go to Settings → Automations & Scenes → Blueprints
2. Click "Import Blueprint"
3. Enter URL: `https://github.com/R00S/eglo-remote-zha/blob/main/blueprints/eglo_awox_area_selection.yaml`
4. Click "Preview" then "Import"

### Step 6: Configure the Area Selection Automation

1. Go to Settings → Automations & Scenes
2. Click "Create Automation" → "Use Blueprint"
3. Select "Eglo Remote - Area & Light Selection"
4. Configure inputs:
   - **Eglo Remote**: Select your paired remote device
   - **Excluded Areas**: Select any areas you don't want to control (optional)
   - **Default Area**: Select your primary area (e.g., "Living Room")
   - **Power Left Button Entity**: Select an entity to toggle (optional)
   - **Current Area Helper**: Select `input_select.eglo_remote_current_area`
   - **Current Light Helper**: Select `input_select.eglo_remote_current_light`
   - **Default Area Helper**: Select `input_text.eglo_remote_default_area`
   - **Last Activity Helper**: Select `input_datetime.eglo_remote_last_activity`
   - **Timeout (minutes)**: Set to 5 (or 0 to disable timeout)
5. Save the automation

**Note**: The timeout is now integrated into the main blueprint - no separate automation needed!

### Step 7: Test Your Setup

Test each button:
1. **Candle Mode** - Should cycle through areas (lights blink)
2. **Colour Middle** - Should cycle through lights in current area
3. **Power Right** - Should toggle lights on/off
4. **Colour Top/Left/Right** - Should change colors
5. **Dimming** - Should adjust brightness
6. **White Tone** - Should adjust color temperature
7. **Favourites** - Should recall saved states (after configuring)
8. Wait 5+ minutes without pressing buttons - Should reset to default area (if timeout enabled)

## Button Behavior Changes

### Old System (3-Bank)

| Button | Behavior |
|--------|----------|
| Buttons 1/2/3 | Switch between 3 banks |
| All control buttons | Affected only current bank |

### New System (Area/Light Selection)

| Button | Short Press | Long Press |
|--------|-------------|------------|
| **Power Left** | Toggle custom entity | Save default area |
| **Power Right** | Toggle area/light | Save default state |
| **Colour Top** | Green color | Cycle green temps |
| **Colour Left** | Red color | Cycle red temps |
| **Colour Right** | Blue color | Cycle blue temps |
| **Colour Middle** | Cycle lights | (unused) |
| **Candle Mode** | Cycle areas | (unused) |
| **Dimming** | Adjust 5% | Continuous |
| **White Tone** | Adjust temp | Jump to extreme |
| **Favourites** | Recall states | - |

## Troubleshooting

### Issue: Blueprint won't import

**Solution**: Make sure you're on the correct branch and the URL is correct. Try using the raw GitHub URL.

### Issue: Automations not triggering

**Solution**: 
1. Check that the remote is paired and showing in ZHA
2. Verify the custom quirk is applied (check device info)
3. Enable debug logging to see events
4. Restart Home Assistant

### Issue: Area cycling not working

**Solution**:
1. Ensure helper entities are created correctly
2. Check that areas have lights assigned
3. Verify excluded areas aren't blocking all options
4. Check automation logs for errors

### Issue: Lights not blinking for feedback

**Solution**:
1. Ensure selected area has controllable lights
2. Check that lights are responsive
3. Try with a single light first
4. Verify light entities are correct

### Issue: Timeout not resetting

**Solution**:
1. Check that the main automation is enabled
2. Verify last_activity timestamp is updating
3. Check timeout duration setting (must be > 0)
4. Review automation traces

## FAQ

**Q: Can I still use the old 3-bank system?**

A: No, the 3-bank quirks have been removed. The new system is designed to be better in every way.

**Q: Do I need to re-pair my remote?**

A: No, your remote will continue to work. You just need to update the automations.

**Q: Can I control devices in different protocols now?**

A: Yes! The new system works with ANY Home Assistant light entities, regardless of protocol.

**Q: What if I only have one area?**

A: That's fine! You can still use light selection to control individual lights. Just set that as your default area.

**Q: Can I have multiple remotes?**

A: Yes, but each remote needs its own set of helper entities with unique names.

**Q: How do I save my default area?**

A: Long press the Power Left button when in your preferred area. Lights will blink to confirm.

**Q: How do I save a favorite state?**

A: Long press the Power Right button when lights are in desired state. Recall with Fav 1 or Fav 2 buttons.

## Getting Help

If you encounter issues:

1. Check the [User Guide](AREA_LIGHT_SELECTION_USER_GUIDE.md)
2. Review the [Technical Spec](AREA_LIGHT_SELECTION_SPEC.md)
3. Enable debug logging:
   ```yaml
   logger:
     default: info
     logs:
       custom_components.eglo_remote_zha: debug
   ```
4. Open an issue on GitHub with logs attached

## Rollback (If Needed)

If you absolutely need to rollback:

1. Download version 0.x.x from GitHub releases
2. Manually install the old version
3. Restore your old automation configurations
4. Restart Home Assistant

**Note:** We strongly recommend giving the new system a fair trial before rolling back. It's designed to be much better once you get used to it.

---

**Version:** 0.1.0  
**Date:** 2025-12-18
