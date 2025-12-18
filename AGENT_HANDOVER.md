# Agent Handover Document - Eglo Remote ZHA Integration

## Current Status: MAJOR ARCHITECTURAL CHANGE IN PROGRESS

This PR is transitioning from a 3-bank manual workaround system to an intelligent **Area/Light Selection System**.

## What Needs To Be Implemented 🚀

### Overview of New System

The new system replaces manual 3-bank switching with an intelligent area/light cycling system that:
- Cycles through Home Assistant areas with a button press
- Selects individual lights within areas
- Provides visual feedback (light blinks)
- Auto-resets after 5 minutes or on HA restart
- Saves default areas and states

**Full specification**: See `docs/AREA_LIGHT_SELECTION_SPEC.md`

### Implementation Tasks

#### 1. Quirk Simplification ✅ TODO

**File**: `custom_components/eglo_remote_zha/eglo_ercu_awox.py`

**Changes needed**:
1. Remove all 3-bank logic (no more `_1`, `_2`, `_3` suffixes)
2. Remove bank detection code
3. Keep all hardware long press implementations
4. Emit simple events (22 total, no banks):
   - `turn_on`, `turn_off`
   - `dim_up`, `dim_down`, `dim_up_long`, `dim_down_long`
   - `color_red`, `color_green`, `color_blue`, `color_cycle`
   - `color_red_long`, `color_green_long`, `color_blue_long`, `color_cycle_long`
   - `scene_1`, `scene_2`
   - `color_temp_up`, `color_temp_down`
   - `color_temp_up_long`, `color_temp_down_long`
   - `refresh`, `refresh_long`

**What to remove**:
- `Awox99099Remote3Banks` class
- GroupID extraction logic
- Bank mapping dictionaries
- All references to `dst_addressing.group`

**What to keep**:
- Basic `Awox99099Remote` class
- All cluster handlers with long press support
- Command definitions
- Signature matching

#### 2. New Blueprint Creation ✅ TODO

**File**: `blueprints/eglo_awox_area_selection.yaml`

**Required inputs**:
```yaml
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
        options: []  # Auto-populate from HA areas
        
  default_area:
    name: Default Area
    selector:
      select:
        options: []  # Auto-populate from HA areas
        
  power_left_entity:
    name: Power Left Button Entity
    description: Entity to toggle with power left button
    selector:
      entity:
```

**Helper entities to create** (via blueprint or instructions):
- `input_select.eglo_remote_[id]_current_area`
- `input_select.eglo_remote_[id]_current_light`
- `input_text.eglo_remote_[id]_default_area`
- `input_datetime.eglo_remote_[id]_last_activity`

**Trigger definitions**: One for each of 22 button events

**Action sequences** for each button:
- State checks
- Area/light cycling logic
- Visual feedback (blink sequences using `repeat` with `light.turn_on`/`turn_off`)
- State updates
- Timeout reset

**Key automations to implement**:

1. **Candle Mode Button** (area cycling):
```yaml
- Check if single light selected
  - If yes: First press → select whole area
  - If no: Cycle to next non-excluded area
- Blink all lights in new area (on/off twice)
- Update current_area helper
- Reset last_activity timestamp
```

2. **Middle Color Button** (light cycling):
```yaml
- Get all lights in current area
- Cycle to next light (or "all")
- Blink selected light (on/off twice)
- Update current_light helper
- Reset last_activity timestamp
```

3. **Power Left Button**:
```yaml
Short press:
  - Toggle power_left_entity

Long press:
  - Save current_area to default_area
  - Show confirmation (blink once)
```

4. **Power Right Button**:
```yaml
Short press:
  - Toggle current area/light

Long press:
  - Create scene with current state
  - Save as default state
  - Show confirmation
```

5. **Color Buttons** (Top/Left/Right):
```yaml
Short press:
  - Set color to green/red/blue

Long press:
  - Cycle color temp within that color's range
  - Use repeat loop for continuous cycling
```

6. **Dimming/Color Temp Buttons**:
```yaml
Short press:
  - Adjust by 5%

Long press:
  - Continuous adjustment
  - Use repeat loop with brightness_step_pct
```

7. **Favorite Buttons**:
```yaml
Fav 1:
  - Activate default_area_state scene

Fav 2:
  - Activate default_light_state scene
```

8. **Timeout Automation** (separate automation):
```yaml
trigger:
  - platform: template
    value_template: >
      {{ (now() - states('input_datetime.eglo_remote_[id]_last_activity') | as_datetime).total_seconds() > 300 }}

action:
  - Set current_area to default_area
  - Set current_light to "all"
  - Optional: Blink lights in default area
```

#### 3. Documentation Updates ✅ TODO

**Files to update**:

1. `README.md`: ✅ DONE
   - Updated key features section
   - Updated remote control layout
   - Added detailed button functions

2. `docs/TERMS_OF_REFERENCE.md`: ✅ DONE
   - Updated project goals

3. `AGENT_HANDOVER.md`: 🔄 IN PROGRESS (this file)

**Files to create**:

1. `docs/AREA_LIGHT_SELECTION_SPEC.md`: ✅ DONE
   - Complete technical specification

2. `docs/AREA_LIGHT_SELECTION_USER_GUIDE.md`: ✅ TODO
   - User-friendly setup guide
   - Step-by-step configuration
   - Troubleshooting section
   - Visual diagrams

**Files to archive** (move to `docs/archive/`):
- `3BANK_WORKAROUND_SOLUTION.md`
- `3BANK_INVESTIGATION_RESULTS.md`
- `3BANK_FINAL_SOLUTION.md`
- `DEEP_DEBUG_BANK_BUTTONS.md`
- `DEBUGGING_3BANKS.md`

#### 4. Remove Old 3-Bank Files ✅ TODO

**Files to delete**:
- `custom_components/eglo_remote_zha/eglo_ercu_awox_3banks.py`
- `blueprints/eglo_awox_3banks.yaml`
- `blueprints/eglo_awox_manual_bank.yaml`

**Files to modify**:
- `custom_components/eglo_remote_zha/__init__.py`
  - Remove import of `eglo_ercu_awox_3banks`
  - Keep only `eglo_ercu_awox` import

#### 5. Testing Checklist ✅ TODO

**Unit Tests**:
- [ ] Quirk emits correct 22 events
- [ ] No bank suffixes in event names
- [ ] Long press events fire correctly

**Integration Tests**:
- [ ] Area cycling works with exclusions
- [ ] Light cycling within area
- [ ] Visual feedback (blinks) work
- [ ] Timeout resets to default
- [ ] HA restart resets to default
- [ ] Default area save/recall
- [ ] Default state save/recall

**User Acceptance Tests**:
- [ ] Physical buttons trigger correct actions
- [ ] Candle mode cycles areas correctly
- [ ] Middle color cycles lights correctly
- [ ] Long press behaviors work
- [ ] Continuous dimming/temp work
- [ ] Favorites recall states correctly

## Implementation Order

1. **Phase 1: Quirk Simplification**
   - Modify `eglo_ercu_awox.py`
   - Remove 3-bank quirk
   - Test event emission

2. **Phase 2: Blueprint Development**
   - Create area selection blueprint
   - Implement helper entities
   - Implement button automations
   - Test locally

3. **Phase 3: Documentation**
   - Create user guide
   - Archive old docs
   - Update README references

4. **Phase 4: Testing & Validation**
   - Run all tests
   - Fix issues
   - Get user feedback

5. **Phase 5: Cleanup**
   - Delete obsolete files
   - Final PR review
   - Merge

## Technical Implementation Details

### Area Discovery

Blueprint should discover areas dynamically:

```yaml
variables:
  all_areas: "{{ states.light | map(attribute='entity_id') | map('area_name') | unique | list }}"
  selectable_areas: "{{ all_areas | reject('in', excluded_areas) | list }}"
```

### Light Discovery Within Area

```yaml
variables:
  current_area_lights: >
    {{ states.light
       | selectattr('entity_id', 'in', area_entities(current_area))
       | map(attribute='entity_id')
       | list }}
```

### Visual Feedback Implementation

```yaml
- repeat:
    count: 2
    sequence:
      - service: light.turn_on
        target:
          entity_id: "{{ target_lights }}"
      - delay:
          milliseconds: 200
      - service: light.turn_off
        target:
          entity_id: "{{ target_lights }}"
      - delay:
          milliseconds: 200
```

### Timeout Implementation

Use a separate automation that checks `input_datetime.last_activity`:

```yaml
trigger:
  - platform: time_pattern
    minutes: "/1"  # Check every minute
    
condition:
  - condition: template
    value_template: >
      {{ (now() - states('input_datetime.eglo_remote_current_last_activity') 
          | as_datetime).total_seconds() > 300 }}

action:
  - service: input_select.select_option
    target:
      entity_id: input_select.eglo_remote_current_area
    data:
      option: "{{ states('input_text.eglo_remote_default_area') }}"
  - service: input_select.select_option
    target:
      entity_id: input_select.eglo_remote_current_light
    data:
      option: "all"
```

## File Structure After Implementation

```
eglo-remote-zha/
├── custom_components/
│   └── eglo_remote_zha/
│       ├── __init__.py              # Import simplified quirk only
│       ├── config_flow.py           # UI-based setup flow
│       ├── manifest.json            # Integration metadata
│       ├── strings.json             # UI text
│       ├── eglo_ercu_awox.py        # ⭐ Simplified quirk (no banks)
│       └── eglo_ercu_3groups.py     # Tuya TS004F quirk
├── blueprints/
│   ├── eglo_awox_basic.yaml         # Basic blueprint (deprecated)
│   └── eglo_awox_area_selection.yaml # ⭐ NEW: Area selection blueprint
├── docs/
│   ├── AREA_LIGHT_SELECTION_SPEC.md    # ⭐ NEW: Technical spec
│   ├── AREA_LIGHT_SELECTION_USER_GUIDE.md # ⭐ NEW: User guide
│   ├── HACS_INSTALLATION.md
│   ├── TERMS_OF_REFERENCE.md       # Updated
│   └── archive/                    # ⭐ NEW: Old 3-bank docs
│       ├── 3BANK_WORKAROUND_SOLUTION.md
│       ├── 3BANK_INVESTIGATION_RESULTS.md
│       ├── 3BANK_FINAL_SOLUTION.md
│       ├── DEEP_DEBUG_BANK_BUTTONS.md
│       └── DEBUGGING_3BANKS.md
├── hacs.json                       # HACS metadata
├── README.md                       # ✅ Updated
├── AGENT_HANDOVER.md              # 🔄 This file (updated)
└── LICENSE

⭐ = New or significantly modified
✅ = Already updated
🔄 = In progress
```

## Breaking Changes

### For Existing Users

**What stops working**:
- All automations using `*_1`, `*_2`, `*_3` triggers
- 3-bank blueprint automations
- Manual bank switching

**Migration path**:
1. Remove old automations
2. Update integration
3. Import new blueprint
4. Configure areas and exclusions
5. Set default area
6. Test all buttons

**User communication**:
- Add prominent notice in README
- Create migration guide
- Version bump to 1.0.0 (breaking change)

## Success Criteria

Implementation is complete when:

1. ✅ Quirk emits 22 simple events (no banks)
2. ✅ Blueprint handles area/light selection
3. ✅ Visual feedback works correctly
4. ✅ Timeout and reset behavior works
5. ✅ Default area/state save/recall works
6. ✅ All documentation updated
7. ✅ Old files archived or deleted
8. ✅ Tests pass
9. ✅ Physical device testing successful

## Contact Points

- **Repository**: https://github.com/R00S/eglo-remote-zha
- **Issue Tracker**: For bug reports
- **Discussions**: For questions

## Next Agent Instructions

You are receiving this handover to implement the area/light selection system. Your tasks:

1. **Read the spec**: `docs/AREA_LIGHT_SELECTION_SPEC.md`
2. **Simplify the quirk**: Remove 3-bank logic from `eglo_ercu_awox.py`
3. **Create the blueprint**: Implement `eglo_awox_area_selection.yaml`
4. **Write user guide**: Create `AREA_LIGHT_SELECTION_USER_GUIDE.md`
5. **Archive old docs**: Move 3-bank docs to `docs/archive/`
6. **Delete obsolete files**: Remove 3-bank quirk and blueprints
7. **Test thoroughly**: Validate all functionality
8. **Prepare for merge**: Final review and documentation

**Priority**: Focus on getting the core area/light cycling working first, then add advanced features like long press behaviors and favorites.

**Timeline**: This is a major feature - budget 2-3 hours for complete implementation and testing.

---

**Status**: Ready for Next Agent Implementation
**Version**: 1.0.0-beta (breaking change)
**Date**: 2025-12-18


### 1. HACS Integration Structure
- ✅ Created proper `custom_components/eglo_remote_zha/` package structure
- ✅ Added `manifest.json` with HA 2025.12+ compatibility
- ✅ Added `hacs.json` for HACS metadata
- ✅ Implemented UI-based config flow (`config_flow.py`)
- ✅ Added `strings.json` for UI text
- ✅ Module-level quirk imports for auto-registration with zigpy

### 2. Custom Quirks (3 Total)
- ✅ `eglo_ercu_awox.py` - Basic AwoX quirk (22 triggers, single bank)
- ✅ `eglo_ercu_awox_3banks.py` - Advanced 3-bank quirk (66 triggers)
- ✅ `eglo_ercu_3groups.py` - Tuya TS004F quirk (different device)

### 3. Blueprints (2 Total)
- ✅ `eglo_awox_basic.yaml` - Single-bank control
- ✅ `eglo_awox_3banks.yaml` - Universal 3-bank control (ANY protocol)

### 4. Documentation (Complete)
- ✅ `HACS_INSTALLATION.md` - Step-by-step HACS guide
- ✅ `UNIVERSAL_CONTROL.md` - Universal device control examples
- ✅ `SOLUTION_3BANKS.md` - Technical 3-bank explanation
- ✅ `BUTTON_GROUP_ANALYSIS.md` - Complete button/groupID matrix
- ✅ `BUTTON_COUNT_CORRECTION.md` - Physical button count (66 triggers)
- ✅ `IMPLEMENTATION_NOTES.md` - Technical details
- ✅ `AUTOMATION_ANALYSIS.md` - Automation approach
- ✅ `RESEARCH_SUMMARY.md` - Complete research
- ✅ `TERMS_OF_REFERENCE.md` - Project charter
- ✅ Updated `README.md` with HACS badges

### 5. Code Quality
- ✅ Comprehensive error handling
- ✅ Debug/info/error logging throughout
- ✅ Type hints for HA 2025.12
- ✅ Clean uninstall support
- ✅ Single instance enforcement

## What Needs Testing 🔬

### After Merge - User Testing Required

1. **HACS Installation**
   - [ ] Add custom repository in HACS (select "Integration")
   - [ ] Install via HACS successfully
   - [ ] Restart Home Assistant
   - [ ] Verify no errors in logs

2. **Integration Setup**
   - [ ] Settings → Devices & Services → + Add Integration
   - [ ] Search for "Eglo Remote ZHA"
   - [ ] Add integration successfully
   - [ ] Verify logs show quirks imported

3. **Device Pairing**
   - [ ] Pair AwoX ERCU_3groups_Zm remote via ZHA
   - [ ] Verify custom quirk is applied
   - [ ] Check device shows correct manufacturer/model
   - [ ] Verify all 66 automation triggers appear

4. **Blueprint Testing**
   - [ ] Import `eglo_awox_3banks.yaml` blueprint
   - [ ] Create automation for Bank 1
   - [ ] Select devices (try different protocols)
   - [ ] Test all button types:
     - [ ] Power ON/OFF
     - [ ] Brightness Up/Down (short + long)
     - [ ] Colors: Red, Green, Blue, Cycle (short + long)
     - [ ] Scenes: Heart 1, Heart 2
     - [ ] Temperature: Warm, Cold (short + long)
     - [ ] Refresh (short + long)

5. **Bank Switching**
   - [ ] Press button 1 on remote
   - [ ] Test a control button (e.g., Power ON)
   - [ ] Verify `*_1` trigger fires
   - [ ] Press button 2 on remote
   - [ ] Test same control button
   - [ ] Verify `*_2` trigger fires
   - [ ] Repeat for button 3

6. **Multi-Protocol Testing**
   - [ ] Configure Bank 1 with Zigbee lights
   - [ ] Configure Bank 2 with WiFi lights
   - [ ] Configure Bank 3 with mixed devices
   - [ ] Verify all work correctly

## Known Issues / Limitations

### Current Limitations
1. **Double-click not implemented** - Reserved for future enhancement
2. **Physical device testing needed** - Implementation based on Zigbee2MQTT source and user reports, not yet tested with physical hardware

### Potential Issues to Watch For

#### Issue 1: GroupID Extraction
**Symptom**: All buttons trigger `*_1` variants regardless of which bank button (1/2/3) was pressed
**Cause**: `dst_addressing.group` might not contain groupID as expected
**Debug**:
```yaml
logger:
  default: info
  logs:
    custom_components.eglo_remote_zha: debug
    zigpy.quirks: debug
    homeassistant.components.zha: debug
```
**Look for**: Log messages showing groupID values (should be 32778, 32779, or 32780)
**Fix if needed**: Adjust where groupID is extracted from in cluster handlers

#### Issue 2: Quirks Not Registering
**Symptom**: Remote pairs but uses default ZHA handler, no custom triggers
**Cause**: Module-level import failed or zigpy didn't register quirks
**Debug**: Check logs for import errors
**Fix if needed**: Verify ZHA is enabled, check for import exceptions

#### Issue 3: HACS Validation Fails
**Symptom**: Can't add repository in HACS or validation errors
**Cause**: Missing required HACS files or incorrect structure
**Debug**: Check HACS validation errors
**Fix if needed**: Compare against working integration structures

#### Issue 4: Integration Won't Load
**Symptom**: Integration doesn't appear in "Add Integration" list
**Cause**: manifest.json issues or missing dependencies
**Debug**: Check HA logs for integration loading errors
**Fix if needed**: Verify manifest.json structure and ZHA dependency

## Technical Implementation Details

### Quirk Registration Mechanism

The quirks register automatically via **module-level imports**:

```python
# In custom_components/eglo_remote_zha/__init__.py
from .eglo_ercu_3groups import EgloERCU3Groups
from .eglo_ercu_awox import Awox99099Remote
from .eglo_ercu_awox_3banks import Awox99099Remote3Banks
```

When HA restarts:
1. HA scans `custom_components/` directory
2. Imports `eglo_remote_zha` module to read manifest.json
3. Module-level imports execute
4. `CustomDevice` classes are defined
5. `_RegistryMetaclass` (from zigpy.quirks) auto-registers quirks in DEVICE_REGISTRY
6. Quirks are available when ZHA needs them

**No explicit registration needed!** The metaclass handles everything.

### 3-Bank Implementation

Each control button command includes groupID in Zigbee message header:
- Button 1 pressed → commands sent with groupID 0x800A (32778)
- Button 2 pressed → commands sent with groupID 0x800B (32779)
- Button 3 pressed → commands sent with groupID 0x800C (32780)

Custom cluster handlers intercept commands and extract groupID:

```python
def handle_cluster_request(self, hdr, args, *, dst_addressing=None):
    group_id = dst_addressing.group if dst_addressing else None
    bank = {0x800A: 1, 0x800B: 2, 0x800C: 3}.get(group_id, 1)
    action = f"{base_action}_{bank}"  # e.g., "turn_on_1"
    # Fire event with bank-specific action
```

This creates 66 unique triggers (22 actions × 3 banks).

### Universal Device Control

Blueprint uses standard HA service calls:
- `light.turn_on` works for Zigbee, WiFi, Thread, BLE lights
- `switch.turn_on` works for any switch entity
- HA handles protocol translation
- No Touchlink or ZHA groups required
- User just selects entities in blueprint

## File Structure

```
eglo-remote-zha/
├── custom_components/
│   └── eglo_remote_zha/
│       ├── __init__.py              # Main integration + quirk imports
│       ├── config_flow.py           # UI-based setup flow
│       ├── manifest.json            # Integration metadata
│       ├── strings.json             # UI text
│       ├── eglo_ercu_awox.py        # Basic quirk
│       ├── eglo_ercu_awox_3banks.py # 3-bank quirk ⭐
│       └── eglo_ercu_3groups.py     # Tuya TS004F quirk
├── blueprints/
│   ├── eglo_awox_basic.yaml         # Basic blueprint
│   └── eglo_awox_3banks.yaml        # Universal 3-bank blueprint ⭐
├── docs/
│   ├── HACS_INSTALLATION.md         # Installation guide
│   ├── UNIVERSAL_CONTROL.md         # Universal control examples
│   ├── SOLUTION_3BANKS.md           # 3-bank technical details
│   ├── BUTTON_GROUP_ANALYSIS.md     # Button/groupID matrix
│   ├── BUTTON_COUNT_CORRECTION.md   # 66 triggers breakdown
│   ├── IMPLEMENTATION_NOTES.md      # Technical implementation
│   ├── AUTOMATION_ANALYSIS.md       # Automation approach
│   └── ...
├── quirks/                          # Original location (kept for reference)
├── hacs.json                        # HACS metadata
├── README.md                        # Updated with HACS info
└── LICENSE

⭐ = Core functionality for 3-bank support
```

## Installation Instructions (For Users)

### Via HACS (Recommended)
1. HACS → Integrations → ⋮ → Custom repositories
2. Add: `https://github.com/R00S/eglo-remote-zha` as **Integration**
3. Search "Eglo Remote ZHA" and install
4. Restart Home Assistant
5. Settings → Devices & Services → + Add Integration → "Eglo Remote ZHA"
6. Pair remote via ZHA
7. Import and configure blueprint

### Manual Installation (Alternative)
1. Copy `custom_components/eglo_remote_zha/` to `<config>/custom_components/`
2. Restart Home Assistant
3. Settings → Devices & Services → + Add Integration → "Eglo Remote ZHA"
4. Pair remote via ZHA
5. Import and configure blueprint

## Debugging Commands

### Check if integration loaded:
```bash
# In HA logs, look for:
DEBUG (custom_components.eglo_remote_zha) Eglo Remote ZHA quirks imported successfully
INFO (custom_components.eglo_remote_zha) Eglo Remote ZHA integration enabled
```

### Check if quirks registered with zigpy:
```bash
# Enable debug logging:
logger:
  logs:
    zigpy.quirks: debug

# Look for device signature match in logs when pairing
```

### Check groupID in messages:
```bash
# Enable debug logging:
logger:
  logs:
    custom_components.eglo_remote_zha: debug

# Press buttons on remote, look for groupID values in logs
```

## Next Agent Tasks

### Immediate Priority (After Merge)
1. **Monitor initial user feedback** on HACS installation
2. **Gather debug logs** from physical device testing
3. **Verify groupID extraction** works correctly
4. **Confirm all 66 triggers** appear and fire correctly
5. **Test universal device control** with multiple protocols

### Short-term Enhancements
1. Add double-click support (currently ignored)
2. Add more blueprint examples
3. Create video installation guide
4. Add more troubleshooting scenarios

### Long-term Goals
1. Submit to HA core for potential inclusion
2. Add support for other Eglo remote models
3. Community feedback integration
4. Performance optimizations

## Contact Points

- **Repository**: https://github.com/R00S/eglo-remote-zha
- **Issue Tracker**: For bug reports and feature requests
- **Discussions**: For questions and community support

## Final Notes

This integration is **ready for merge and community testing**. The implementation is based on:
- Zigbee2MQTT source code analysis
- User reports and manual analysis
- Zigpy quirk patterns
- Home Assistant 2025.12 best practices

**Physical device testing is the final validation step** - the code structure is sound, but real-world testing will confirm the groupID extraction approach works correctly.

All core functionality is implemented:
- ✅ HACS installation support
- ✅ UI-based configuration
- ✅ 3-bank quirk with 66 triggers
- ✅ Universal device control blueprint
- ✅ Comprehensive documentation
- ✅ Error handling and logging
- ✅ Clean code structure

**Status**: Production Ready (pending physical device validation)

---

*Generated: 2025-12-13*
*Version: 0.0.1*
*Home Assistant: 2025.12.0+*
