# Deep Debugging Bank Buttons 1/2/3

## Goal

Discover what pressing bank buttons 1, 2, and 3 actually does at the Zigbee protocol level.

## Why We Need This

- ZHA events show nothing when pressing 1/2/3
- But the buttons clearly DO something (they change which lights respond)
- We need to see the raw Zigbee frames/commands

## Setup Debug Logging

### Step 1: Enable Zigpy Debug Logging

Add this to your `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    # Zigpy core logging
    zigpy: debug
    zigpy.zcl: debug
    zigpy.application: debug
    zigpy.device: debug
    zigpy.endpoint: debug
    zigpy.quirks: debug
    
    # ZHA component logging
    homeassistant.components.zha: debug
    
    # Custom integration logging
    custom_components.eglo_remote_zha: debug
```

### Step 2: Restart Home Assistant

```bash
# From Home Assistant UI: Developer Tools → Restart
# Or from command line:
ha core restart
```

### Step 3: Clear Logs (Optional)

Before testing, you can clear old logs to make finding the new entries easier:
- Settings → System → Logs → Clear

## Testing Procedure

### Test 1: Press Bank Button 1

1. Press button **1** on the remote
2. Immediately go to Settings → System → Logs
3. Look for ANY log entries related to the remote
4. Copy ALL log entries (especially from zigpy.zcl)

### Test 2: Press Bank Button 2

1. Press button **2** on the remote
2. Check logs
3. Copy ALL log entries

### Test 3: Press Bank Button 3

1. Press button **3** on the remote
2. Check logs
3. Copy ALL log entries

### Test 4: Long Press

1. Try **long-pressing** (hold 2-3 seconds) buttons 1, 2, 3
2. Check if different logs appear

## What to Look For

In the logs, search for:

### Device Identifier
```
AwoX ERCU_3groups_Zm
A4:C1:38:9B:FF:80:25:1B
0xb599
```

### Cluster Activity
Look for messages mentioning:
- `cluster_id` (especially 0x0004 Groups, 0x0005 Scenes, 0xFF50/0xFF51 proprietary)
- `endpoint` (especially endpoint 3)
- `command_id`
- `group` or `group_id`
- `dst_addressing`

### Example Log Patterns

```
zigpy.zcl: [0xb599:1:0x0005] Received command 0x00 ...
zigpy.zcl: [0xb599:3:0xFF50] Received command ...
zigpy.device: [0xb599] Received frame: ...
```

## What We're Testing

### Hypothesis 1: Scene Commands
Buttons might use Scenes cluster (0x0005) with scene_id 3, 4, 5:
```
cluster_id=0x0005, command_id=0x05 (recall_scene), scene_id=3/4/5
```

### Hypothesis 2: Group Commands
Buttons might use Groups cluster (0x0004):
```
cluster_id=0x0004, command_id varies, group_id=1/2/3
```

### Hypothesis 3: Endpoint 3 Activity
Buttons might use proprietary clusters on endpoint 3:
```
endpoint=3, cluster_id=0xFF50 or 0xFF51
```

### Hypothesis 4: Binding Table Changes
Buttons might modify the device's binding table (not visible in logs directly, but we'd see confirmation responses)

### Hypothesis 5: No Commands Sent
Buttons might truly be internal-only (firmware changes state without Zigbee messages)

## Alternative: Packet Capture

If logging doesn't show anything, we can use a Zigbee sniffer:

### Option 1: Wireshark with Zigbee Sniffer
- Requires compatible hardware (nRF52840 dongle, CC2531, etc.)
- Captures ALL Zigbee traffic including coordinator-to-device

### Option 2: ZHA Toolkit
Install ZHA Toolkit custom component:
```bash
# HACS → Integrations → Search "ZHA Toolkit"
```

Use the `zha_toolkit.binds_get` service to see bindings:
```yaml
service: zha_toolkit.binds_get
data:
  ieee: "A4:C1:38:9B:FF:80:25:1B"
```

Press button 1, check bindings. Press button 2, check again. See if they change.

## Expected Outcomes

### Outcome A: Commands Found
If we see Zigbee commands when pressing 1/2/3:
- **Extract command details** (cluster, command_id, parameters)
- **Map them in the quirk** as device automation triggers
- **Implement state tracking** to emit bank-specific events
- ✅ **Full automatic 3-bank support possible**

### Outcome B: Binding Table Changes
If bindings change but no commands sent:
- **Document the binding pattern**
- **Explain Touchlink setup process**
- **Keep manual workaround** as only solution
- ❌ **Automatic detection not possible**

### Outcome C: Nothing Visible
If truly no Zigbee activity:
- **Confirm firmware-level operation**
- **Manual workaround is the only solution**
- **Document the limitation clearly**
- ❌ **Automatic detection not possible**

## Next Steps

Once you share the debug logs:
1. I'll analyze what commands (if any) are sent
2. If commands exist, I'll implement quirk support
3. If no commands, we confirm the manual workaround is necessary
4. Either way, we'll have definitive answers

## Log Sharing

When sharing logs, please include:
- **Full timestamp range** (so we know when you pressed the button)
- **Multiple entries** (press each button 1/2/3 at least twice)
- **Context** (e.g., "Pressed button 1 at 02:15:30")
- **Raw text** (not screenshots if possible, for easier searching)

This will give us the complete picture of what's happening!
