# Implementation Prompt for Next Agent

## Mission

Implement the **Area/Light Selection System** for the Eglo Remote ZHA integration. This system replaces the manual 3-bank workaround with an intelligent area/light cycling mechanism.

## Context

You are working on the `R00S/eglo-remote-zha` repository, branch `copilot/fix-blueprint-loading-issue`. All architectural documentation has been completed. Your task is to implement the system according to the specifications.

## Required Reading

Before starting, read these files (in order):
1. `docs/AREA_LIGHT_SELECTION_SPEC.md` - Technical specification
2. `AGENT_HANDOVER.md` - Implementation instructions
3. `docs/AREA_LIGHT_SELECTION_USER_GUIDE.md` - User perspective

## Your Tasks

### Task 1: Simplify the Quirk (HIGH PRIORITY)

**File**: `custom_components/eglo_remote_zha/eglo_ercu_awox.py`

**What to do**:
1. Remove ALL 3-bank logic:
   - Remove bank suffix logic (`_1`, `_2`, `_3`)
   - Remove `dst_addressing.group` extraction
   - Remove bank mapping dictionaries
   - Simplify cluster handlers

2. Keep hardware long press support for:
   - Dimming buttons (up/down)
   - Color temperature buttons (warm/cold)
   - Color buttons (top/left/right/middle)
   - Power buttons (left/right)
   - Candle mode
   - Refresh button

3. Emit exactly 22 events:
   - `turn_on`, `turn_off`
   - `dim_up`, `dim_down`, `dim_up_long`, `dim_down_long`
   - `color_red`, `color_green`, `color_blue`, `color_cycle`
   - `color_red_long`, `color_green_long`, `color_blue_long`, `color_cycle_long`
   - `scene_1`, `scene_2`
   - `color_temp_up`, `color_temp_down`, `color_temp_up_long`, `color_temp_down_long`
   - `refresh`, `refresh_long`

**Testing**: Verify events are emitted correctly with no bank suffixes.

### Task 2: Create Area Selection Blueprint (HIGH PRIORITY)

**File**: `blueprints/eglo_awox_area_selection.yaml`

**Structure**:

```yaml
blueprint:
  name: Eglo Remote - Area & Light Selection
  description: Intelligent area and light cycling system
  domain: automation
  input:
    remote:
      name: Eglo Remote
      selector:
        device:
          integration: eglo_remote_zha
    excluded_areas:
      name: Excluded Areas
      selector:
        select:
          multiple: true
    default_area:
      name: Default Area
      selector:
        area: {}
    power_left_entity:
      name: Power Left Button Entity
      selector:
        entity: {}
      default: ""
    current_area_helper:
      name: Current Area Helper
      selector:
        entity:
          domain: input_select
    current_light_helper:
      name: Current Light Helper
      selector:
        entity:
          domain: input_select
    default_area_helper:
      name: Default Area Helper
      selector:
        entity:
          domain: input_text
    last_activity_helper:
      name: Last Activity Helper
      selector:
        entity:
          domain: input_datetime

trigger:
  # Define triggers for all 22 button events
  # Use device triggers from ZHA
  
action:
  # Use choose/conditions to handle each button
  # Implement cycling, visual feedback, state management
```

**Key automations to implement**:

1. **Candle Mode** → Area cycling
   - Get list of non-excluded areas
   - Cycle to next area
   - Blink all lights in new area twice (200ms on, 200ms off, repeat)
   - Update current_area helper
   - Update last_activity timestamp

2. **Middle Color** → Light cycling
   - Get all lights in current area using `area_entities(current_area)`
   - Cycle to next light (or "all")
   - Blink selected light twice
   - Update current_light helper
   - Update last_activity timestamp

3. **Power Left Short** → Toggle custom entity

4. **Power Left Long** → Save default area
   - Save current_area to default_area helper
   - Blink lights once to confirm

5. **Power Right Short** → Toggle current area/light

6. **Power Right Long** → Save default state
   - Create scene with current state
   - Store scene entity_id
   - Blink lights once to confirm

7. **Color Buttons Short** → Set color (red/green/blue)

8. **Color Buttons Long** → Cycle color temp within range

9. **Dimming/Temp Short** → Adjust by 5%

10. **Dimming/Temp Long** → Continuous adjustment (use repeat loop)

11. **Fav 1** → Recall default area state

12. **Fav 2** → Recall default light state

**Visual Feedback Template**:
```yaml
- repeat:
    count: 2
    sequence:
      - service: light.turn_on
        target:
          entity_id: "{{ target_lights }}"
        data:
          brightness_pct: 100
      - delay:
          milliseconds: 200
      - service: light.turn_off
        target:
          entity_id: "{{ target_lights }}"
      - delay:
          milliseconds: 200
```

**Testing**: Test each button behavior, verify area/light cycling, confirm visual feedback.

### Task 3: Create Timeout Automation (MEDIUM PRIORITY)

**File**: `blueprints/eglo_awox_timeout.yaml` (separate blueprint)

**Purpose**: Reset to default area after 5 minutes of inactivity

```yaml
trigger:
  - platform: time_pattern
    minutes: "/1"

condition:
  - condition: template
    value_template: >
      {{ (now() - states('input_datetime.eglo_remote_last_activity') | as_datetime).total_seconds() > 300 }}

action:
  - service: input_select.select_option
    target:
      entity_id: !input current_area_helper
    data:
      option: "{{ states(!input default_area_helper) }}"
  - service: input_select.select_option
    target:
      entity_id: !input current_light_helper
    data:
      option: "all"
```

**Testing**: Wait 5 minutes after button press, verify reset to default.

### Task 4: Cleanup Old Files (MEDIUM PRIORITY)

**Delete these files**:
1. `custom_components/eglo_remote_zha/eglo_ercu_awox_3banks.py`
2. `blueprints/eglo_awox_3banks.yaml`
3. `blueprints/eglo_awox_manual_bank.yaml`

**Update this file**:
- `custom_components/eglo_remote_zha/__init__.py`
  - Remove import of `Awox99099Remote3Banks`
  - Keep only `Awox99099Remote` and `EgloERCU3Groups` imports

**Archive these files** (create `docs/archive/` folder):
1. `3BANK_WORKAROUND_SOLUTION.md`
2. `3BANK_INVESTIGATION_RESULTS.md`
3. `3BANK_FINAL_SOLUTION.md`
4. `DEEP_DEBUG_BANK_BUTTONS.md`
5. `DEBUGGING_3BANKS.md`

**Testing**: Verify integration still loads without errors.

### Task 5: Update Documentation (LOW PRIORITY)

**Update README.md**:
- Add setup instructions for helper entities
- Add link to user guide
- Remove references to "3-bank" system

**Create migration guide** (`docs/MIGRATION_FROM_3BANK.md`):
- Explain breaking changes
- Provide step-by-step migration
- List what to delete
- Show helper entity creation

**Testing**: Review all documentation for consistency.

## Implementation Order

1. **Start with Task 1** (Quirk simplification) - Everything depends on this
2. **Then Task 2** (Blueprint creation) - Core functionality
3. **Then Task 3** (Timeout automation) - Supporting functionality
4. **Then Task 4** (Cleanup) - Remove obsolete code
5. **Finally Task 5** (Documentation) - Polish

## Button Naming Convention (IMPORTANT)

Use these exact names in all code and documentation:
- **Power buttons**: Power left, Power right
- **Color buttons**: Colour top, Colour left, Colour middle, Colour right
- **Other**: Candle mode, Dimming, White tone selection, Favourites (Fav 1, Fav 2)

## Testing Checklist

After implementation, verify:

- [ ] Quirk loads without errors
- [ ] 22 events emitted (no bank suffixes)
- [ ] Long press events work
- [ ] Candle mode cycles areas correctly
- [ ] Middle color cycles lights correctly
- [ ] Visual feedback (blinks) work
- [ ] Power left short toggles entity
- [ ] Power left long saves default area
- [ ] Power right short toggles area/light
- [ ] Power right long saves state
- [ ] Color buttons set colors
- [ ] Long press color buttons cycle temps
- [ ] Dimming/temp adjust by 5%
- [ ] Long press dimming/temp continuous
- [ ] Fav 1 recalls area state
- [ ] Fav 2 recalls light state
- [ ] Timeout resets after 5 minutes
- [ ] HA restart resets to default
- [ ] Excluded areas are skipped
- [ ] Helper entities update correctly

## Success Criteria

Implementation is complete when:

1. All 5 tasks are done
2. All tests pass
3. Integration loads without errors
4. Physical device testing successful (if available)
5. Documentation is complete and accurate
6. Code is clean and well-commented
7. No breaking changes to non-3-bank features

## Important Notes

- **Don't break existing Tuya TS004F support** - Only modify AwoX quirk
- **Keep config flow intact** - Don't modify UI setup
- **Preserve existing button names** - Use naming convention above
- **Test after each major change** - Don't wait until the end
- **Comment complex logic** - Especially area/light discovery
- **Use templates carefully** - Test with various HA configurations

## Resources

- **ZHA Device Automation**: https://www.home-assistant.io/integrations/device_automation/
- **Blueprint Documentation**: https://www.home-assistant.io/docs/automation/using_blueprints/
- **Template Documentation**: https://www.home-assistant.io/docs/configuration/templating/
- **Helper Entities**: https://www.home-assistant.io/integrations/#helper

## Questions?

If you're unsure about anything:
1. Check the spec: `docs/AREA_LIGHT_SELECTION_SPEC.md`
2. Check the handover: `AGENT_HANDOVER.md`
3. Look at existing blueprint examples in repo
4. Ask for clarification before proceeding

## Final Step

When complete:
1. Run all tests
2. Verify on physical device if possible
3. Update AGENT_HANDOVER.md status to "Implementation Complete"
4. Create comprehensive commit message
5. Push changes
6. Mark PR as ready for review

Good luck! This is a significant architectural improvement that will make the remote much more user-friendly. 🚀

---

**Priority**: HIGH
**Estimated Time**: 2-3 hours
**Dependencies**: None (all specs complete)
**Version**: 1.0.0-beta (breaking change)
