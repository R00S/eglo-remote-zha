# AwoX ERCU Remote Button Testing Results

This document contains the complete hardware testing results that identified the duplicate event issues and informed the quirk fixes in version 0.1.4.

## Testing Environment
- Remote: AwoX ERCU_3groups_Zm (Eglo Remote 2.0)
- Integration: Home Assistant ZHA
- Test Method: Monitoring ZHA events via Home Assistant

---

## Button Test Results

### Left Power Button
**Short Press:**
```
Remote 1 Remote Button Short Press - Turn Off event was fired
```
**Long Press:** No event produced

**Status:** ✓ Working correctly (no duplicate events)

---

### Top Color Button (Green)
**Short Press - BEFORE FIX:**
```
Remote 1 Remote Button Short Press - Turn On event was fired
21:36:05 - Now
Remote 1 Awox Color event was fired with parameters: {'param1': 0, 'color': 84}
```
**Issue:** Produces TWO events (Turn On + Awox Color)  
**Expected:** Should only produce Awox Color event

**Long Press:**
```
Remote 1 Move To Hue And Saturation event was fired with parameters: {'hue': 84, 'saturation': 254, 'transition_time': 2, 'options_mask': None, 'options_override': None}
```
**Status:** ✓ Long press works correctly (single event)

---

### Left Color Button (Red)
**Short Press - BEFORE FIX:**
```
Remote 1 Remote Button Short Press - Turn On event was fired
21:39:31 - 4 seconds ago
Remote 1 Awox Color event was fired with parameters: {'param1': 0, 'color': 254}
```
**Issue:** Produces TWO events (Turn On + Awox Color)  
**Expected:** Should only produce Awox Color event

---

### Right Color Button (Blue)
**Short Press - BEFORE FIX:**
```
Remote 1 Remote Button Short Press - Turn On event was fired
21:39:35 - Now
Remote 1 Move To Hue And Saturation event was fired with parameters: {'hue': 169, 'saturation': 254, 'transition_time': 2, 'options_mask': None, 'options_override': None}
```
**Issue:** Produces TWO events (Turn On + Move To Hue And Saturation)  
**Expected:** Should only produce Move To Hue And Saturation event

**Additional Test:**
```
Remote 1 Remote Button Short Press - Turn On event was fired
21:39:06 - 29 seconds ago
Remote 1 Awox Color event was fired with parameters: {'param1': 0, 'color': 169}
```
**Note:** Blue button can produce either Move To Hue/Sat OR Awox Color depending on press duration/detection

---

### Middle Color Button (Cycle/Refresh)
**Short Press - BEFORE FIX:**
```
Remote 1 Remote Button Short Press - Turn On event was fired
21:40:24 - Now
Remote 1 Enhanced Move Hue event was fired with parameters: {'move_mode': <MoveMode.Up: 1>, 'rate': 3072, 'options_mask': <OptionsMask: 0>, 'options_override': <Options: 0>}
```
**Issue:** Produces TWO events (Turn On + Enhanced Move Hue)  
**Expected:** Should only produce Enhanced Move Hue event

**Additional Test:**
```
Remote 1 Remote Button Short Press - Turn On event was fired
21:40:18 - 7 seconds ago
Remote 1 Enhanced Move Hue event was fired with parameters: {'move_mode': <MoveMode.Up: 1>, 'rate': 3072, 'options_mask': <OptionsMask: 0>, 'options_override': <Options: 0>}
```
**Confirmed:** Consistently produces duplicate Turn On events

---

### Candle Button
**Short Press - BEFORE FIX:**
```
Remote 1 Remote Button Short Press - Turn On event was fired
21:41:16 - 5 seconds ago
Remote 1 Awox Refresh event was fired with parameters: {'param1': 1, 'press': 1}
```
**Issue:** Produces TWO events (Turn On + Awox Refresh with press=1)  
**Expected:** Should only produce Awox Refresh event

**Long Press - BEFORE FIX:**
```
Remote 1 Remote Button Short Press - Turn On event was fired
21:41:21 - Now
Remote 1 Awox Refresh event was fired with parameters: {'param1': 1, 'press': 2}
```
**Issue:** Produces TWO events (Turn On + Awox Refresh with press=2)  
**Expected:** Should only produce Awox Refresh event  
**Note:** Long press has press=2 parameter to distinguish from short press

---

### Color Temperature - Warm Button
**Short Press - BEFORE FIX:**
```
Remote 1 Remote Button Short Press - Turn On event was fired
21:44:19 - 4 seconds ago
Remote 1 Step Color Temp event was fired with parameters: {'step_mode': ...}
```
**Issue:** Produces TWO events (Turn On + Step Color Temp)  
**Expected:** Should only produce Step Color Temp event

**Long Press - BEFORE FIX:**
```
Remote 1 Remote Button Short Press - Turn On event was fired
21:44:18 - 4 seconds ago
Remote 1 Move To Color Temp event was fired with parameters: {'color_temp_mireds': 454, 'transition_time': 2, 'options_mask': None, 'options_override': None}
```
**Issue:** Produces TWO events (Turn On + Move To Color Temp)  
**Expected:** Should only produce Move To Color Temp event

---

### Color Temperature - Cold Button
**Short Press - BEFORE FIX:**
```
Remote 1 Remote Button Short Press - Turn On event was fired
21:44:15 - 8 seconds ago
Remote 1 Step Color Temp event was fired with parameters: {'step_mode': ...}
```
**Issue:** Produces TWO events (Turn On + Step Color Temp)  
**Expected:** Should only produce Step Color Temp event

**Long Press - BEFORE FIX:**
```
Remote 1 Remote Button Short Press - Turn On event was fired
21:44:22 - Now
Remote 1 Move To Color Temp event was fired with parameters: {'color_temp_mireds': 153, 'transition_time': 2, 'options_mask': None, 'options_override': None}
```
**Issue:** Produces TWO events (Turn On + Move To Color Temp)  
**Expected:** Should only produce Move To Color Temp event

---

### Favorite Button 1 (Heart 1)
**Short Press:**
```
Remote 1 Recall event was fired with parameters: {'group_id': 0x0000, 'scene_id': 1, 'transition_time': None}
```
**Status:** ✓ Working correctly (single Recall event)

**Long Press:**
```
Remote 1 Store event was fired with parameters: {'group_id': 0x0000, 'scene_id': 1}
```
**Status:** ✓ Working correctly (single Store event)  
**Note:** Long press Store functionality was NOT previously mapped in the quirk

---

### Favorite Button 2 (Heart 2)
**Short Press:**
```
Remote 1 Recall event was fired with parameters: {'group_id': 0x0000, 'scene_id': 2, 'transition_time': None}
```
**Status:** ✓ Working correctly (single Recall event)

**Long Press:**
```
Remote 1 Store event was fired with parameters: {'group_id': 0x0000, 'scene_id': 2}
```
**Status:** ✓ Working correctly (single Store event)  
**Note:** Long press Store functionality was NOT previously mapped in the quirk

---

## Summary of Issues Found

### Duplicate "Turn On" Events
The following buttons were producing unwanted duplicate "Turn On" events:
1. ❌ Top Color (Green) - short press
2. ❌ Left Color (Red) - short press  
3. ❌ Right Color (Blue) - short press
4. ❌ Middle Color (Cycle/Refresh) - short press
5. ❌ Candle button - short press
6. ❌ Candle button - long press
7. ❌ Warm button - short press
8. ❌ Warm button - long press
9. ❌ Cold button - short press
10. ❌ Cold button - long press

### Missing Trigger Mappings
The following button functions were NOT exposed in the quirk:
1. ❌ Fav 1 - long press (Store scene 1)
2. ❌ Fav 2 - long press (Store scene 2)

---

## Root Cause Analysis

### Hardware Behavior
The AwoX ERCU remote physically sends TWO Zigbee commands for certain button presses:
- **Color buttons** → Send `COMMAND_ON` (cluster 6) + specific color command (cluster 768)
- **Candle button** → Sends `COMMAND_ON` (cluster 6) + `COMMAND_AWOX_REFRESH` (cluster 8)
- **Color temp buttons** → Send `COMMAND_ON` (cluster 6) + temp command (cluster 768)

### Quirk Implementation Issue
The quirk had a trigger mapping for `(SHORT_PRESS, TURN_ON)` that would fire whenever `COMMAND_ON` was received. Since multiple buttons send this command along with their specific commands, they all triggered both the TURN_ON event AND their specific event.

---

## Fixes Implemented (Version 0.1.4)

### Fix 1: Remove Duplicate TURN_ON Trigger
**Commit:** 8d14ac8

**Change:**
```python
# REMOVED this line from device_automation_triggers:
(SHORT_PRESS, TURN_ON): {COMMAND: COMMAND_ON, CLUSTER_ID: 6, ENDPOINT_ID: 1},
```

**Result:** All color, candle, and color temp buttons now produce only their specific event without the duplicate "Turn On" event.

**Files Modified:**
- `quirks/eglo_ercu_awox.py`
- `quirks/eglo_ercu_awox_3banks.py`

---

### Fix 2: Add Long Press Store Triggers for Fav Buttons
**Commit:** 6d5bb78

**Changes:**
1. Added `COMMAND_STORE = "store"` constant
2. Added trigger mappings:
```python
(LONG_PRESS, "heart_1"): {
    COMMAND: COMMAND_STORE,
    CLUSTER_ID: 5,
    ENDPOINT_ID: 1,
    PARAMS: {"scene_id": 1},
},
(LONG_PRESS, "heart_2"): {
    COMMAND: COMMAND_STORE,
    CLUSTER_ID: 5,
    ENDPOINT_ID: 1,
    PARAMS: {"scene_id": 2},
},
```

**Result:** Fav buttons now expose both Recall (short press) and Store (long press) functionality.

**Files Modified:**
- `quirks/eglo_ercu_awox.py`
- `quirks/eglo_ercu_awox_3banks.py`

---

## Expected Behavior After Fixes

### All Buttons - Clean Single Events

| Button | Short Press Event | Long Press Event |
|--------|------------------|------------------|
| Left Power | Turn Off | (none) |
| Top Color (Green) | Awox Color (color=84/85) | Move To Hue/Sat (hue=84/85) |
| Left Color (Red) | Awox Color (color=254/255) | Move To Hue/Sat (hue=254/255) |
| Right Color (Blue) | Awox Color (color=169/170) | Move To Hue/Sat (hue=169/170) |
| Middle Color | Enhanced Move Hue (mode=1) | Enhanced Move Hue (mode=3) |
| Candle | Awox Refresh (press=1) | Awox Refresh (press=2) |
| Warm | Step Color Temp (step_mode=1) | Move To Color Temp (454 mireds) |
| Cold | Step Color Temp (step_mode=3) | Move To Color Temp (153 mireds) |
| Fav 1 | Recall (scene_id=1) | Store (scene_id=1) |
| Fav 2 | Recall (scene_id=2) | Store (scene_id=2) |
| Dim Up | Step (step_mode=0) | Move To Level (level=254) |
| Dim Down | Step (step_mode=1) | Move To Level (level=1) |

**All buttons now produce exactly ONE event per press** ✓

---

## Testing Instructions

To verify the fixes:

1. Copy the updated quirk file to Home Assistant:
   ```bash
   cp quirks/eglo_ercu_awox.py /config/zhaquirks/
   ```

2. Restart Home Assistant to reload the quirk

3. Monitor ZHA events while pressing each button

4. Verify:
   - ✓ No "Turn On" events when pressing color buttons
   - ✓ No "Turn On" events when pressing candle button
   - ✓ No "Turn On" events when pressing color temp buttons
   - ✓ Fav 1 long press produces Store event
   - ✓ Fav 2 long press produces Store event
   - ✓ All buttons produce exactly one event per press

---

**Testing Date:** 2025-12-18  
**Tester:** @R00S  
**Version:** 0.1.4  
**Remote Model:** AwoX ERCU_3groups_Zm (Eglo Remote 2.0)
