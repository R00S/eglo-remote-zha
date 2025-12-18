# Changelog

All notable changes to the Eglo Remote ZHA integration.

## [Unreleased - BROKEN BUILD - DO NOT USE]

### ⚠️ CRITICAL: THIS BUILD IS NON-FUNCTIONAL

**Status**: USELESS - Random button behavior, no predictable operation

**Problem**: Button presses generate random light events with no pattern. The Store-based state management system has fundamental issues that cause unpredictable behavior.

**Recommendation**: Use the stable `main` branch with 3-bank system instead.

---

### Attempted Changes (All Non-Functional)

#### Added (Non-Functional)
- Store-based state persistence system (`homeassistant.helpers.storage`)
- Integration services: `eglo_remote_zha.set_state` and `eglo_remote_zha.get_state`
- State stored in `.storage/eglo_remote_zha_state.json`
- Per-device state isolation using device_id
- Service response support with `SupportsResponse.ONLY`
- ZHA event trigger system (bypassing device automation triggers)
- Area/light selection system with cycling
- Automatic state initialization from device area
- Visual confirmation via light blinks
- 5-minute timeout to return to default area
- Favorite state save/recall functionality

#### Changed (Breaking)
- Removed all 3-bank functionality (was working, now broken)
- Converted blueprint to use ZHA event triggers instead of device triggers
- Removed helper entity auto-creation attempts
- Removed manual helper entity selection
- Changed power button functions (long press removed due to hardware limitation)
- Moved save state functionality to middle colour button long press
- Complete blueprint rewrite to use Store services

#### Fixed Bugs (During Development)
- Device discovery issue with duplicate power button entries
- Template rendering errors (`area_name` filter vs function)
- Service response variable support declaration
- Variable name conflict (`device_id` vs `remote_device_id`)
- Available areas template syntax error

#### Technical Debt Created
- Random light events with no predictable pattern
- State management fundamentally broken
- Blueprint logic not executing correctly
- Area exclusions not being respected
- Service calls failing intermittently
- Unclear root cause of random behavior

### Known Issues (Blocking)
1. **Random button behavior** - Buttons trigger unpredictable light events
2. **State persistence broken** - Store system not functioning correctly
3. **Logic errors** - Blueprint automation logic has fundamental flaws
4. **No debugging path** - Unable to determine root cause of randomness
5. **Area exclusions ignored** - Excluded areas still receive events

### Removed (Working Features Deleted)
- 3-bank system (was functional)
- Bank switching automation
- Manual bank selection
- Helper entity workflow (attempted automation failed)
- Device automation triggers (replaced with ZHA events)

### Migration from v0.0.1 (Stable)
**DO NOT MIGRATE** - This version is broken. Stay on v0.0.1 with 3-bank system.

If you accidentally upgraded:
1. Remove this integration
2. Checkout the `main` branch
3. Reinstall from stable version
4. Reconfigure your 3-bank automations

---

## [v0.0.1] - 2024 (STABLE - USE THIS VERSION)

### Working Features
- 3-bank system for organizing lights
- Manual bank switching via special button combinations
- All 22 button events functional
- Device automation triggers working
- ZHA event triggers available
- Basic blueprint for 3-group control
- Power button short press only (hardware limitation confirmed)
- Proper quirk registration and device discovery

### Recommended Setup
- Use quirk: `quirks/eglo_ercu_awox.py`
- Use blueprint: Available in stable branch
- Manual 3-bank configuration via automations
- Helper entities created by user
- Documented in QUICKSTART.md

---

## Development Notes

### What Went Wrong
1. **Attempted Store-based persistence** - Created complex service-based state management
2. **Removed working 3-bank code** - Deleted functional system for experimental replacement
3. **Blueprint complexity** - Over 700 lines of template logic with unclear execution path
4. **Variable naming conflicts** - Multiple namespace collisions in templates
5. **Insufficient testing** - Changes pushed without validating basic functionality
6. **No rollback strategy** - Committed to non-functional approach without fallback

### Lessons Learned
- Simple helper-based approach was likely better than Store complexity
- Should have kept 3-bank system working while developing new features
- Template debugging in Home Assistant is extremely difficult
- Service-based state management adds significant complexity
- Integration testing needed before committing major refactors

### Future Recommendations
- Revert to v0.0.1 as baseline
- If improving, keep 3-bank system functional
- Add small incremental features
- Test each change thoroughly before next change
- Consider helper entities acceptable if they work
- Avoid complex template logic in blueprints
- Use simpler state management patterns

---

## Version History

- **Current (Broken)**: v0.1.3 - Store-based persistence (NON-FUNCTIONAL)
- **Stable**: v0.0.1 - 3-bank system (USE THIS)
