# Button Count Correction

## Corrected Physical Button Count

**Total buttons on AwoX ERCU_3groups_Zm: 16**

### Breakdown:
- **3 bank selector buttons** (1, 2, 3) - stateful, don't send commands
- **13 control buttons** - send commands with groupID

## Control Buttons (13 total)

### Power Control (2 buttons)
1. ON
2. OFF

### Color Control (4 buttons)
3. Red
4. Green
5. Blue
6. Cycle/Refresh colored

### Scene Control (2 buttons)
7. Heart 1 (Scene 1)
8. Heart 2 (Scene 2)

### Brightness Control (2 buttons)
9. Dim UP
10. Dim DOWN

### Color Temperature Control (2 buttons)
11. Warm
12. Cold

### Special Functions (1 button)
13. Refresh

## Group Selector Buttons (3 total)

14. Button 1 (selects group 32778 / 0x800A)
15. Button 2 (selects group 32779 / 0x800B)
16. Button 3 (selects group 32780 / 0x800C)

## Implementation Impact

**Device Automation Triggers Needed:**
- 13 control buttons × 3 groups = **39 separate triggers**

**Previous Error:**
- Incorrectly stated "16 control buttons × 3 groups = 48 triggers"
- Should have been "13 control buttons × 3 groups = 39 triggers"

**Corrected in commit:** (to be added)

## Summary

- ✅ **13 control buttons** send commands with groupID
- ❌ **3 bank selector buttons** are stateful only
- 📊 **39 unique trigger combinations** (13 × 3)
- 🔢 **16 total physical buttons** on the remote
