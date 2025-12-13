# Eglo Remote ZHA Quirks

> ⚠️ **UNDER DEVELOPMENT**: These quirks are being tested and validated. Use with caution.

This directory contains custom ZHA quirks for Eglo remote controls.

## What are ZHA Quirks?

ZHA quirks are Python modules that extend Home Assistant's Zigbee support for devices that don't fully comply with standard Zigbee specifications or need special handling. They define how the device's Zigbee clusters map to Home Assistant entities and events.

## Available Quirks

### 1. Eglo ERCU_3groups_Zm (Tuya Variant) - `eglo_ercu_3groups.py`

**Status**: ✅ Tested and working

**Device Information:**
- **Model**: TS004F
- **Manufacturer**: _TZ3000_4fjiwweb
- **Type**: 6-button remote (3 groups × 2 buttons)

**Features:**
- All 6 buttons mapped (buttons 1-6)
- Short press events (on/off)
- Long press events (dimming)
- Long release events (stop dimming)
- Uses PhilipsRemoteCluster as base
- Single endpoint architecture

**Clusters:**
- Input: Basic, PowerConfiguration, Identify, Groups, OnOff, LightLink
- Output: OnOff (cluster 6), LevelControl (cluster 8)

### 2. Eglo ERCU_3groups_Zm (AwoX Variant) - `eglo_ercu_awox.py`

**Status**: 🔄 In development/testing

**Device Information:**
- **Model**: ERCU_3groups_Zm / 99099
- **Manufacturer**: AwoX
- **Type**: Color remote with scene control

**Features:**
- Extended button mapping with color controls
- Scene recall support
- Color temperature control
- Custom AwoX clusters
- Dual endpoint architecture (endpoints 1 and 3)

**Clusters:**
- Standard ZHA clusters
- Custom AwoX Color cluster (0x30 command)
- Custom AwoX LevelControl cluster (0x10 command)
- Manufacturer-specific clusters on endpoint 3 (0xFF50, 0xFF51)

## Installation

### Prerequisites

- Home Assistant with ZHA integration configured
- Zigbee coordinator supported by ZHA
- Eglo remote control (see supported models above)

### Installation Steps

1. **Create custom quirks directory**:
   ```bash
   mkdir -p /config/zhaquirks
   ```

2. **Copy the appropriate quirk file**:
   ```bash
   # For TS004F (Tuya variant)
   cp eglo_ercu_3groups.py /config/zhaquirks/
   
   # For AwoX variant
   cp eglo_ercu_awox.py /config/zhaquirks/
   
   # Optional: Copy __init__.py if using as a package
   cp __init__.py /config/zhaquirks/
   ```

3. **Configure ZHA in configuration.yaml**:
   ```yaml
   zha:
     custom_quirks_path: /config/zhaquirks/
   ```

4. **Restart Home Assistant**

5. **Remove and re-pair the device**:
   - Remove the Eglo remote from ZHA if already paired
   - Reset the remote (hold any button for ~10 seconds until LED flashes)
   - Put ZHA in pairing mode
   - Press any button on the remote to pair

6. **Verify quirk is loaded**:
   - Go to Configuration → Devices & Services → ZHA
   - Find your Eglo remote
   - Click on it and check "Device Info"
   - Should show the custom quirk class name

## Verifying the Quirk Works

### Check Device Signature

In ZHA device info, you should see:
- Manufacturer: `_TZ3000_4fjiwweb` (Tuya) or `AwoX`
- Model: `TS004F` or `ERCU_3groups_Zm`
- Quirk: `EgloERCU3Groups` or `Awox99099Remote`

### Test Button Events

1. Go to Developer Tools → Events
2. Listen to `zha_event`
3. Press buttons on the remote
4. You should see events with:
   - `device_ieee` (your device address)
   - `command` (on, off, move, stop)
   - `endpoint_id` (usually 1)
   - Button information

### Test Automation Triggers

1. Create a new automation
2. Add trigger: Device
3. Select your Eglo remote
4. You should see triggers like:
   - `remote_button_short_press` with subtype `button_1` through `button_6`
   - `remote_button_long_press` with subtype `button_1` through `button_6`
   - `remote_button_long_release` with subtype `button_1` through `button_6`

## Troubleshooting

### Quirk Not Loading

**Symptom**: Device shows generic Zigbee remote, no custom triggers

**Solutions**:
1. Check file path: Ensure quirk file is in `/config/zhaquirks/`
2. Check configuration.yaml: Verify `custom_quirks_path` is set
3. Check Home Assistant logs for quirk loading errors
4. Restart Home Assistant after adding quirk
5. Re-pair the device

### Wrong Device Signature

**Symptom**: Your device has a different manufacturer or model code

**Solution**:
1. Get your device signature from ZHA
2. Open an issue with the signature
3. We may need to create a new quirk or update the existing one

### Buttons Not Working

**Symptom**: No events when pressing buttons

**Solutions**:
1. Check battery level
2. Verify device is not in sleep mode (press any button to wake)
3. Check ZHA event log for any Zigbee messages
4. Re-pair the device
5. Enable debug logging (see below)

### Enable Debug Logging

Add to `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    zigpy: debug
    homeassistant.components.zha: debug
    zhaquirks: debug
```

Then monitor logs:
```bash
tail -f /config/home-assistant.log | grep -i "eglo\|ercu\|TS004F\|quirk"
```

## Technical Details

### Device Automation Triggers

The quirks define these automation triggers:

**TS004F (Tuya variant):**
- 6 buttons × 3 event types = 18 total triggers
- Each trigger maps to specific Zigbee commands:
  - Short press → `on` or `off` command on cluster 6
  - Long press → `move` command on cluster 8 (with move_mode parameter)
  - Long release → `stop` command on cluster 8

**AwoX variant:**
- Additional color and scene controls
- Custom cluster commands
- Extended button mappings for RGB control

### Cluster Architecture

**Single Endpoint (TS004F)**:
- All buttons send commands through endpoint 1
- Button differentiation through command parameters and timing

**Dual Endpoint (AwoX)**:
- Endpoint 1: Standard ZHA profile (0x0104)
- Endpoint 3: Custom profile (0x128F) with manufacturer-specific clusters

## Contributing

Found an issue or have an improvement?

1. **Test thoroughly** with your physical device
2. **Document** your changes and findings
3. **Submit** a pull request with:
   - Description of the change
   - Why it's needed
   - Test results
   - Device signature if different

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

## References

- [ZHA Device Handlers GitHub](https://github.com/zigpy/zha-device-handlers)
- [Zigpy Documentation](https://github.com/zigpy/zigpy)
- [Zigbee Cluster Library](https://zigbeealliance.org/wp-content/uploads/2019/12/07-5123-06-zigbee-cluster-library-specification.pdf)
- [Home Assistant ZHA Integration](https://www.home-assistant.io/integrations/zha/)

## License

See [LICENSE](../LICENSE) for details.
