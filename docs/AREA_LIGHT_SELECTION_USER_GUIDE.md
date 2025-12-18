# Area & Light Selection System - User Guide

## Welcome!

This guide will help you set up and use the intelligent Area & Light Selection System for your Eglo Remote. With this system, you can easily cycle through your Home Assistant areas and control all lights or individual lights with just a few button presses!

## What is This System?

Instead of manually switching between "banks" or creating complex automations, your Eglo remote now:

- **Cycles through your rooms/areas** - Press the Candle Mode button
- **Selects individual lights** - Press the Middle Color button  
- **Shows visual feedback** - Lights blink to confirm your selection
- **Remembers your defaults** - Long press to save your favorite area
- **Auto-resets** - Returns to your default area after 5 minutes

## Quick Start

### Step 1: Install the Integration

1. Add this repository in HACS as a custom integration
2. Install "Eglo Remote ZHA"
3. Restart Home Assistant
4. Add the integration: Settings → Devices & Services → + Add Integration → "Eglo Remote ZHA"

### Step 2: Pair Your Remote

1. Make sure ZHA is enabled
2. Put ZHA in pairing mode
3. Press any button on your Eglo remote
4. Wait for pairing to complete
5. Verify the remote appears in ZHA with manufacturer "AwoX"

### Step 3: Import the Blueprint

1. Go to Configuration → Blueprints
2. Click "+ Import Blueprint"
3. Enter URL: `https://github.com/R00S/eglo-remote-zha/blob/main/blueprints/eglo_awox_area_selection.yaml`
4. Or manually copy the blueprint YAML file

### Step 4: Create Helper Entities

Before creating the automation, you need to create some helper entities. Go to Settings → Devices & Services → Helpers → + Create Helper:

**1. Input Select: Current Area**
- Name: `Eglo Remote Current Area`
- Options: (Leave empty for now, blueprint will populate)

**2. Input Select: Current Light**
- Name: `Eglo Remote Current Light`
- Options: `all` (add this one option)

**3. Input Text: Default Area**
- Name: `Eglo Remote Default Area`
- Initial value: Your main living area (e.g., "Living Room")

**4. Input DateTime: Last Activity**
- Name: `Eglo Remote Last Activity`
- Date: No
- Time: Yes

### Step 5: Configure the Blueprint

1. Go to Configuration → Automations
2. Click "+ Add Automation" → "Use a blueprint"
3. Select "Eglo Remote Area Selection"
4. Fill in the configuration:
   - **Remote Device**: Select your Eglo remote
   - **Excluded Areas**: Check any areas you don't want to control (like bathrooms, outdoor areas)
   - **Default Area**: Select your primary area (where the remote resets to)
   - **Power Left Entity**: Choose what entity the Power Left button should toggle (optional - can be a switch, scene, script, etc.)
   - **Helper Entities**: Select the helpers you created in Step 4

5. Save the automation

### Step 6: Test It Out!

**Try cycling areas**:
1. Press the **Candle Mode** button
2. Your lights should blink twice - you've switched areas!
3. Press it again to cycle to the next area

**Try selecting a single light**:
1. Press the **Middle Color** button
2. One light blinks twice - it's now selected!
3. Use dimming, colors, etc. - only that light will respond
4. Press Middle Color again to select the next light

**Try saving your default**:
1. Cycle to your favorite area
2. **Long press Power Left** button
3. Lights blink once - your default is saved!

## How to Use Your Remote

### Basic Concept

Think of your remote in three modes:
1. **Controlling all lights in an area** (default)
2. **Controlling a single light in an area**
3. **Switching between areas**

### Cycling Through Areas

**Press Candle Mode button** → Next area
- Only cycles through areas you haven't excluded
- Lights in the new area blink twice to confirm
- After 5 minutes of no button presses, returns to your default area

### Selecting Individual Lights

**Press Middle Color button** → Next light in current area
- Cycles: All lights → First light → Second light → ... → All lights
- The selected light blinks twice to confirm
- Now all button actions affect only that light

### Returning to Whole Area

When you have a single light selected:
1. **Press Candle Mode once** → Selects the whole area again
2. **Press Candle Mode again** → Cycles to the next area

### Controlling Lights

Once you've selected an area or light, use these buttons:

**Power Right** - Turn selected area/light on or off

**Color Buttons**:
- **Top (Green)**: Short press → Set to green | Long press → Cycle green color temps
- **Left (Red)**: Short press → Set to red | Long press → Cycle red color temps  
- **Right (Blue)**: Short press → Set to blue | Long press → Cycle blue color temps

**Dimming**:
- **Up**: Short press → Brighten 5% | Long press → Continuous brighten
- **Down**: Short press → Dim 5% | Long press → Continuous dim

**Color Temperature**:
- **Warm**: Short press → Warmer 5% | Long press → Continuous warm
- **Cold**: Short press → Cooler 5% | Long press → Continuous cool

### Saving and Recalling Defaults

**Save Default Area**: Long press **Power Left**
- Saves the currently selected area as your default
- Remote will return to this area after timeout or HA restart

**Save Area State**: Long press **Power Right**  
- Saves the current state of all lights in the selected area
- Recall with **Fav 1** button

**Save Light State**: Long press **Power Right** (when single light selected)
- Saves the current state of the selected light
- Recall with **Fav 2** button

**Recall Saved States**:
- **Fav 1** → Restore your saved area state (all lights)
- **Fav 2** → Restore your saved single light state

### Special Features

**Power Left Button** (Configurable):
- Short press → Toggle whatever entity you configured
- Could be a switch, a scene, a script, another light, etc.
- Long press → Save default area (always)

## Example Workflows

### Workflow 1: Morning Routine

1. **Press Fav 1** → Restore your saved "morning" area state (e.g., Kitchen at 100%)
2. Use the remote to adjust as needed
3. **Long press Power Left** → Save as default area

### Workflow 2: Movie Time

1. **Press Candle Mode** until you reach "Living Room"
2. **Press Middle Color** to select the lamp
3. **Dim Down** (short press several times) → Set to 20%
4. **Press Warm** (long press) → Make it very warm
5. **Long press Power Right** → Save this as your light default
6. Next time: **Press Fav 2** → Instant movie lamp setting!

### Workflow 3: Quick Bedroom Check

1. **Press Candle Mode** to cycle to "Bedroom"
2. **Power Right** → Toggle bedroom lights
3. Wait 5 minutes → Remote auto-returns to your default area (e.g., Living Room)

## Troubleshooting

### Lights don't blink when I press Candle Mode

**Problem**: Visual feedback not working  
**Solutions**:
- Check that the lights support on/off commands
- Verify the lights are assigned to the correct area in HA
- Try excluding problem areas and use only working lights

### Remote doesn't seem to control anything

**Problem**: Automation not triggering  
**Solutions**:
- Check that the automation is enabled
- Verify the remote device is selected correctly in blueprint
- Check HA logs for errors
- Re-pair the remote if needed

### Area cycling skips some rooms

**Check**: Are those areas in your "Excluded Areas" list?  
**Solution**: Edit the automation and remove them from exclusions

### Timeout doesn't work / doesn't reset

**Problem**: Last activity time not updating  
**Solutions**:
- Verify the `input_datetime` helper exists
- Check that the automation updates it on each button press
- Check the separate timeout automation is enabled

### Single light selection isn't working

**Problem**: Multiple lights respond instead of one  
**Solutions**:
- Verify lights are properly assigned to areas in HA
- Check that `current_light` helper is updating correctly
- Look at automation trace to see which entity_id is being targeted

### Power Left button doesn't toggle my entity

**Problem**: Wrong entity or entity doesn't support toggle  
**Solutions**:
- Check you selected the correct entity in blueprint config
- Try a different entity that supports `turn_on`/`turn_off` or `toggle`
- Use a script or scene if the entity type doesn't work directly

## Advanced Tips

### Create Multiple Automation Profiles

You can create multiple automations from the same blueprint:
- "Eglo Remote - Daytime Profile" (normal areas)
- "Eglo Remote - Night Profile" (only bedroom, bathroom)

Enable/disable them with a schedule or script!

### Use Scripts for Complex Power Left Actions

Instead of toggling a single entity with Power Left, create a script that:
- Toggles multiple entities
- Triggers a scene
- Runs other automations
- Sends notifications

### Combine with Voice Control

Use voice commands to change the current area:
```yaml
"Alexa, set Eglo remote area to Kitchen"
→ Updates input_select.eglo_remote_current_area
```

### Dashboard Card

Create a card showing current status:
```yaml
type: entities
entities:
  - entity: input_select.eglo_remote_current_area
    name: Current Area
  - entity: input_select.eglo_remote_current_light
    name: Selected Light
  - entity: input_text.eglo_remote_default_area
    name: Default Area
```

## Button Reference Card

Print this and keep it handy!

```
┌─────────────────────────────────────────┐
│ EGLO REMOTE - BUTTON REFERENCE          │
├─────────────────────────────────────────┤
│ POWER LEFT:                             │
│   Short → Toggle custom entity          │
│   Long  → Save default area             │
├─────────────────────────────────────────┤
│ POWER RIGHT:                            │
│   Short → Toggle area/light             │
│   Long  → Save state as default         │
├─────────────────────────────────────────┤
│ CANDLE MODE:                            │
│   → Cycle to next area                  │
│   (from single light: area then next)   │
├─────────────────────────────────────────┤
│ MIDDLE COLOR:                           │
│   → Cycle through lights in area        │
├─────────────────────────────────────────┤
│ COLOR TOP (Green):                      │
│   Short → Set green                     │
│   Long  → Cycle green temps             │
├─────────────────────────────────────────┤
│ COLOR LEFT (Red):                       │
│   Short → Set red                       │
│   Long  → Cycle red temps               │
├─────────────────────────────────────────┤
│ COLOR RIGHT (Blue):                     │
│   Short → Set blue                      │
│   Long  → Cycle blue temps              │
├─────────────────────────────────────────┤
│ DIMMING:                                │
│   Up Short   → Brighten 5%              │
│   Up Long    → Continuous brighten      │
│   Down Short → Dim 5%                   │
│   Down Long  → Continuous dim           │
├─────────────────────────────────────────┤
│ COLOR TEMP:                             │
│   Warm Short → Warmer 5%                │
│   Warm Long  → Continuous warm          │
│   Cold Short → Cooler 5%                │
│   Cold Long  → Continuous cool          │
├─────────────────────────────────────────┤
│ FAV 1: Recall default area state        │
│ FAV 2: Recall default light state       │
└─────────────────────────────────────────┘
```

## Getting Help

- **GitHub Issues**: Report bugs or request features
- **GitHub Discussions**: Ask questions and share tips
- **Home Assistant Community**: Join the discussion thread

## Credits

This system was designed to provide intuitive, remote-based control of your entire home lighting without complex configuration or manual switching. Enjoy!

---

**Version**: 1.0
**Last Updated**: 2025-12-18
