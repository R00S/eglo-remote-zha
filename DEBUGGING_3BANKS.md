# Debugging 3-Bank Functionality

## Current Status

The 3-bank quirk (`Awox99099Remote3Banks`) has been updated with debug logging to investigate why bank differentiation isn't working.

## What's Implemented

1. **66 Device Automation Triggers**: The quirk defines separate triggers for each bank:
   - Bank 1: `turn_on_1`, `dim_up_1`, `red_1`, etc.
   - Bank 2: `turn_on_2`, `dim_up_2`, `red_2`, etc.
   - Bank 3: `turn_on_3`, `dim_up_3`, `red_3`, etc.

2. **Debug Logging**: Added to capture:
   - `dst_addressing` object contents
   - `group` attribute presence
   - `group_id` values (expected: 32778, 32779, 32780 for banks 1, 2, 3)
   - Mapped bank numbers

3. **Blueprints**: Updated to use bank-specific triggers with `enabled` conditions

## Testing Instructions

1. **Remove and re-pair the remote** to load the updated quirk
2. **Check logs** in Home Assistant (Settings → System → Logs)
3. **Test sequence**:
   - Press button 1 (select bank 1)
   - Press dim up
   - Look for log: `AwoxLevelControlCluster: group_id=32778, bank=1`
   - Press button 2 (select bank 2)
   - Press dim up
   - Look for log: `AwoxLevelControlCluster: group_id=32779, bank=2`
   - Press button 3 (select bank 3)
   - Press dim up
   - Look for log: `AwoxLevelControlCluster: group_id=32780, bank=3`

## Expected Outcomes

### Scenario A: group_id IS present
Log will show:
```
AwoxLevelControlCluster: group_id=32778, bank=1
AwoxLevelControlCluster: group_id=32779, bank=2
AwoxLevelControlCluster: group_id=32780, bank=3
```

**Solution**: Modify cluster handlers to emit events with bank suffix based on group_id.

### Scenario B: group_id is NOT present
Log will show:
```
AwoxLevelControlCluster: dst_addressing=None, has_group=False, group=None
```
OR
```
AwoxLevelControlCluster: dst_addressing=<object>, has_group=False, group=None
```

**Solution**: Need alternative approach:
- Track last pressed bank button (1/2/3) in device state
- Use stored bank for subsequent button presses
- Or investigate if bank info is in a different part of the message

### Scenario C: group_id is always the same
Log will show the same group_id for all banks:
```
AwoxLevelControlCluster: group_id=32778, bank=1  # Always 32778
```

**Solution**: Bank buttons don't change group_id. Need to:
- Make buttons 1/2/3 emit their own events
- Track which was pressed last
- Use that for subsequent control buttons

## Next Steps

After receiving logs:
1. Analyze which scenario applies
2. Implement the appropriate solution
3. Test with updated quirk
4. Update blueprints if needed
5. Document final solution

## Current Commit

Debug logging added in: `e5b526b`
