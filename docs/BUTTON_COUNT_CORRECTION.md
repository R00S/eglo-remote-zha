# Button Count Correction

## Corrected Physical Button Count with Long Press Support

**Total buttons on AwoX ERCU_3groups_Zm: 16**

### Breakdown:
- **3 bank selector buttons** (1, 2, 3) - stateful, don't send commands
- **13 control buttons** - send commands with groupID
- **22 unique actions** (including long press)

## Control Buttons with Actions (22 total actions)

### Power Control (2 buttons, 2 actions)
1. ON (short press)
2. OFF (short press)

### Color Control (4 buttons, 8 actions)
3. Red (short press, long press)
4. Green (short press, long press)
5. Blue (short press, long press)
6. Cycle/Refresh colored (short press, long press)

### Scene Control (2 buttons, 2 actions)
7. Heart 1 / Scene 1 (short press)
8. Heart 2 / Scene 2 (short press)

### Brightness Control (2 buttons, 4 actions)
9. Dim UP (short press, long press)
10. Dim DOWN (short press, long press)

### Color Temperature Control (2 buttons, 4 actions)
11. Warm (short press, long press)
12. Cold (short press, long press)

### Special Functions (1 button, 2 actions)
13. Refresh (short press, long press)

## Group Selector Buttons (3 total)

14. Button 1 (selects group 32778 / 0x800A)
15. Button 2 (selects group 32779 / 0x800B)
16. Button 3 (selects group 32780 / 0x800C)

## Implementation Impact

**Device Automation Triggers Needed:**
- **22 unique actions × 3 groups = 66 separate triggers**

**Breakdown:**
- Short press only: ON, OFF, Heart 1, Heart 2 (4 actions)
- Short + Long press: Colors (Red, Green, Blue, Cycle), Brightness (Up, Down), Temperature (Warm, Cold), Refresh (9 buttons = 18 actions)
- Total: 4 + 18 = 22 actions per bank
- 22 actions × 3 banks = 66 total triggers

**Previous Errors:**
- First: "16 control buttons × 3 groups = 48 triggers"
- Second: "13 control buttons × 3 groups = 39 triggers" (without long press)
- **Corrected**: "22 actions × 3 groups = 66 triggers" (with long press)

## Summary

- ✅ **13 control buttons** send commands with groupID
- ✅ **22 unique actions** (short + long press where applicable)
- ❌ **3 bank selector buttons** are stateful only
- 📊 **66 unique trigger combinations** (22 × 3)
- 🔢 **16 total physical buttons** on the remote
- 🚫 **Double click ignored** for now (future enhancement)
