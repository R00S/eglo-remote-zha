# Area/Light Source Selection System - Technical Specification

## Overview

This document specifies the intelligent area and light source selection system for the Eglo Remote ZHA integration. This replaces the previous 3-bank manual workaround approach with a stateful, user-friendly area/light cycling system.

## System Architecture

### 1. Quirk Layer (No Banks)
- Remove all 3-bank logic
- Implement all hardware-supported long presses
- Emit simple button events (no bank suffixes)
- No state management in quirk

### 2. Blueprint/Automation Layer (State Management)
- Track currently selected area
- Track currently selected light within area
- Implement 5-minute timeout logic
- Save/recall default area and states
- Handle area/light cycling
- Visual feedback via light blinks

## Button Naming Convention

**Power buttons:**
- Power left (ON)
- Power right (OFF)

**Color buttons:**
- Colour top
- Colour left  
- Colour middle
- Colour right

**Other buttons:**
- Dimming (brightness up/down)
- White tone selection (colour temp up/down)
- Candle mode
- Colour change (automatic mode)
- Favourites (Fav 1, Fav 2)
- Groups/zones (1, 2, 3 - send no events)

## Button Behaviors

### Power Left
**Short Press**: Toggle the entity chosen for it in blueprint setup (configurable entity selector)
**Long Press**: Save current area as the default area for this remote

### Power Right  
**Short Press**: Toggle the selected area/light source on/off
**Long Press**: Save the current state of the selected area/light source as the default state

### Colour Top
**Short Press**: Change colour of selected area/light to green
**Long Press**: Cycle colour temp within green colour range

### Colour Left
**Short Press**: Change colour of selected area/light to red
**Long Press**: Cycle colour temp within red colour range

### Colour Right
**Short Press**: Change colour of selected area/light to blue
**Long Press**: Cycle colour temp within blue colour range

### Candle Mode
**Short Press**: Cycle to next area
**Behavior when single light selected**: First press selects whole area again, second press cycles to next area

### Colour Middle
**Short Press**: Cycle through light sources within the selected area
**Note**: Used to select individual lights within an area

### Dimming Up/Down
**Short Press**: Dim up/down the selected area/light source by 5%
**Long Press**: Continuously dim up/down

### White Tone Selection (Colour Temp Up/Down)
**Short Press**: Warm/cool selected area/light source by 5%
**Long Press**: Continuously warm/cool

### Fav 1
**Short Press**: Recall the default state of the selected area

### Fav 2
**Short Press**: Recall the default state of the selected light source

## Area/Light Selection Logic

### Active Area/Light States
The system tracks:
1. **Current Area**: Which HA area is currently controlled
2. **Current Light**: Which specific light within that area (or "all lights")
3. **Default Area**: User-configured default area
4. **Default Area State**: Saved state for the default area
5. **Default Light State**: Saved state for the selected individual light

### Selection Flow

1. **Initial State**: 
   - Remote controls all lights in default area
   - Default area is set in blueprint configuration

2. **Cycling Areas** (Candle Mode Button):
   - Press candle mode → Next area in list
   - Cycles through only non-excluded areas
   - Visual feedback: Lights in new area blink on/off twice

3. **Cycling Lights** (Middle Colour Button):
   - Press middle colour → Next light in current area
   - Cycles through: All lights → Light 1 → Light 2 → ... → All lights
   - Visual feedback: Selected light blinks on/off twice

4. **Return from Individual Light** (Candle Mode):
   - When individual light is selected
   - First press of candle mode → Select whole area again
   - Second press → Cycle to next area

### Timeout Behavior

**5-Minute Inactivity Timer**:
- Starts after any button press
- Resets with each button press
- On timeout: Remote returns to default area (all lights)
- On HA restart: Remote returns to default area (all lights)

### Visual Feedback

**Area Selection**:
- All lights in selected area blink on/off twice
- Indicates area is now active

**Light Selection**:
- Selected light blinks on/off twice
- Other lights in area remain unchanged

## Blueprint Configuration

### Required Inputs

1. **Remote Device**: Device selector for Eglo remote
2. **Area List**: List of all HA areas (auto-populated)
3. **Excluded Areas**: Multi-select checkboxes to exclude specific areas
4. **Default Area**: Dropdown to select default area
5. **Power Left Entity**: Entity selector for power left button action

### State Storage

Blueprint creates/manages helper entities:
- `input_select.eglo_remote_[id]_current_area`: Current area name
- `input_select.eglo_remote_[id]_current_light`: Current light entity_id or "all"
- `input_text.eglo_remote_[id]_default_area`: Default area name
- `input_datetime.eglo_remote_[id]_last_activity`: Last button press timestamp
- `scene.eglo_remote_[id]_default_area_state`: Default area state
- `scene.eglo_remote_[id]_default_light_state`: Default light state

### Area/Light Discovery

Blueprint automatically discovers:
- All areas in Home Assistant
- All lights in each area
- Builds cycling order based on area names (alphabetical)

## Implementation Requirements

### Quirk Changes

**Files to modify:**
- `custom_components/eglo_remote_zha/eglo_ercu_awox.py`

**Changes:**
1. Remove all 3-bank logic
2. Remove bank suffix from event names
3. Keep all hardware long press implementations
4. Simplify cluster handlers to emit basic events

**Events emitted (22 total, no banks):**
- `turn_on`, `turn_off`
- `dim_up`, `dim_down`
- `dim_up_long`, `dim_down_long`  
- `color_red`, `color_green`, `color_blue`, `color_cycle`
- `color_red_long`, `color_green_long`, `color_blue_long`, `color_cycle_long`
- `scene_1`, `scene_2`
- `color_temp_up`, `color_temp_down`
- `color_temp_up_long`, `color_temp_down_long`
- `refresh`, `refresh_long`

### Blueprint Changes

**Files to create:**
- `blueprints/eglo_awox_area_selection.yaml`

**Blueprint structure:**
1. Input selectors (remote, areas, exclusions, default, entity)
2. Helper entity creation (via blueprint or setup instructions)
3. Trigger definitions for all 22 button events
4. Action sequences for each button:
   - State checks (current area/light)
   - Area/light cycling logic
   - Visual feedback (blink sequences)
   - State updates
   - Timeout management

### Documentation Changes

**Files to update:**
1. `README.md` - Update system description
2. `docs/TERMS_OF_REFERENCE.md` - Update project goals
3. `AGENT_HANDOVER.md` - New implementation instructions
4. Create `docs/AREA_LIGHT_SELECTION_GUIDE.md` - User guide

**Files to deprecate/archive:**
- `3BANK_WORKAROUND_SOLUTION.md`
- `3BANK_INVESTIGATION_RESULTS.md`
- `3BANK_FINAL_SOLUTION.md`
- `DEEP_DEBUG_BANK_BUTTONS.md`
- `DEBUGGING_3BANKS.md`

## Testing Requirements

### Unit Tests
1. Area cycling logic
2. Light cycling logic  
3. Timeout handling
4. Default state recall
5. Visual feedback triggers

### Integration Tests
1. Area selection with excluded areas
2. Light selection within areas
3. Candle mode behavior (area vs light context)
4. Default area saving and recall
5. Timeout reset to default
6. HA restart behavior

### User Acceptance Tests
1. Physical button presses trigger correct actions
2. Visual feedback is clear and intuitive
3. Timeout works as expected
4. Default area/states save and recall correctly
5. Area exclusions work properly

## Migration Path

### For Existing Users

**Upgrade steps:**
1. Update integration to new version
2. Remove old 3-bank blueprint automations
3. Import new area selection blueprint
4. Configure areas and exclusions
5. Set default area
6. Configure power left entity
7. Test all buttons

**Breaking changes:**
- Old `*_1`, `*_2`, `*_3` automation triggers will stop working
- Must recreate automations with new blueprint
- Helper entities from old system can be deleted

## Success Criteria

1. ✅ No manual bank switching required
2. ✅ Intuitive area/light selection via remote buttons
3. ✅ Clear visual feedback for selections
4. ✅ Automatic timeout and reset behavior
5. ✅ Configurable default area and states
6. ✅ Support for excluding unwanted areas
7. ✅ Works with any HA light entities (all protocols)

## Future Enhancements

- Double-click support for faster navigation
- Room groupings for hierarchical selection
- Voice feedback via TTS
- Dashboard card for visual status
- Multiple remote support with separate states

---

**Status**: Specification Complete - Ready for Implementation
**Version**: 1.0
**Date**: 2025-12-18
