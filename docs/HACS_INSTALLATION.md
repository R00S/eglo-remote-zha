# HACS Installation Guide

This guide explains how to install the Eglo Remote ZHA integration via HACS (Home Assistant Community Store).

## Prerequisites

- Home Assistant 2025.12 or newer
- HACS installed and configured
- ZHA integration enabled

## Installation Steps

### 1. Add Custom Repository to HACS

1. Open Home Assistant
2. Go to **HACS** (in the sidebar)
3. Click on **Integrations**
4. Click the three dots menu (⋮) in the top right corner
5. Select **Custom repositories**
6. Add the following information:
   - **Repository**: `https://github.com/R00S/eglo-remote-zha`
   - **Category**: Select **Integration**
7. Click **Add**

### 2. Install the Integration

1. In HACS, search for "Eglo Remote ZHA"
2. Click on the integration
3. Click **Download**
4. Select the latest version
5. Click **Download** again to confirm

### 3. Restart Home Assistant

After installation, you **must** restart Home Assistant:

1. Go to **Settings** → **System**
2. Click **Restart**
3. Wait for Home Assistant to restart (1-2 minutes)

### 4. Add the Integration via UI

After restart, add the integration:

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration** (bottom right)
3. Search for "Eglo Remote ZHA"
4. Click on it
5. Click **Submit** to confirm
6. The integration will be added and quirks will be registered with ZHA

**That's it!** No configuration.yaml editing needed!

### 5. Pair Your Remote

1. Go to **Settings** → **Devices & Services** → **ZHA**
2. Click **Add Device**
3. Put your Eglo remote into pairing mode (refer to manual)
4. Wait for the remote to be discovered
5. The custom quirk will be automatically applied

### 6. Verify Installation

Check that the quirk is loaded:

1. Go to **Settings** → **Devices & Services** → **ZHA**
2. Find your Eglo remote in the device list
3. Click on the device
4. In the device information, you should see:
   - **Model**: ERCU_3groups_Zm or similar
   - **Manufacturer**: AwoX
   - The device should have **66 automation triggers** (for 3-bank quirk)

### 7. Install Blueprint (Optional)

The blueprints are included in the repository:

1. Go to **Settings** → **Automations & Scenes** → **Blueprints**
2. Click **Import Blueprint**
3. Enter the blueprint URL:
   ```
   https://github.com/R00S/eglo-remote-zha/blob/main/blueprints/eglo_awox_3banks.yaml
   ```
4. Click **Preview**
5. Click **Import**

**Alternative**: Manually copy the blueprint file from `blueprints/eglo_awox_3banks.yaml` to your Home Assistant `config/blueprints/automation/` directory.

## Configuration

### Using the 3-Bank Blueprint

1. Go to **Settings** → **Automations & Scenes**
2. Click **Create Automation**
3. Select **Use Blueprint**
4. Find **Eglo Remote 3-Bank Universal Control**
5. Configure for each bank (create 3 automations):
   - **Bank 1**: Configure devices/entities for bank 1
   - **Bank 2**: Configure devices/entities for bank 2
   - **Bank 3**: Configure devices/entities for bank 3

### Selecting Devices

The blueprint allows you to control **ANY** Home Assistant device:
- ✅ Zigbee lights, switches, plugs
- ✅ WiFi devices (TP-Link, Shelly, Tuya, LIFX, etc.)
- ✅ Thread devices (Matter-over-Thread, Nanoleaf, Eve)
- ✅ Bluetooth devices
- ✅ Z-Wave devices
- ✅ RF devices (via bridges)
- ✅ Cloud-connected devices
- ✅ Virtual entities (scripts, helpers, groups)

**You can mix different protocols in the same bank!**

## Troubleshooting

### Remote Not Detected

If your remote isn't detected:
1. Make sure ZHA integration is enabled
2. Restart Home Assistant after installing the integration
3. Try re-pairing the remote
4. Check ZHA logs for errors: **Settings** → **System** → **Logs** → Filter by "zha"

### Quirk Not Applied

If the standard quirk is applied instead of the custom one:
1. Remove the device from ZHA
2. Restart Home Assistant
3. Re-pair the device
4. Check that the custom_components folder exists: `config/custom_components/eglo_remote_zha/`

### Not All Buttons Work

The 3-bank quirk provides **66 automation triggers**:
- 13 control buttons × 3 banks = 39 base triggers
- With long press support: 22 actions × 3 banks = 66 total triggers

If you see fewer triggers:
1. Check which quirk is loaded (see device information)
2. Try using the `eglo_ercu_awox_3banks.py` quirk specifically
3. Restart Home Assistant after any changes

### Blueprint Not Working

If the blueprint doesn't work as expected:
1. Make sure you've created automations for each bank (1, 2, 3)
2. Check automation logs for errors
3. Verify device/entity IDs are correct
4. Test with a single device first before adding multiple

### Debug Logging

Enable debug logging for troubleshooting:

```yaml
logger:
  default: info
  logs:
    zigpy: debug
    homeassistant.components.zha: debug
    custom_components.eglo_remote_zha: debug
```

Add this to your `configuration.yaml`, restart Home Assistant, and check the logs.

## Updates

To update the integration:

1. Go to **HACS** → **Integrations**
2. Find "Eglo Remote ZHA"
3. If an update is available, click **Update**
4. Restart Home Assistant after updating

## Uninstallation

To remove the integration:

1. Go to **HACS** → **Integrations**
2. Find "Eglo Remote ZHA"
3. Click the three dots menu (⋮)
4. Select **Remove**
5. Restart Home Assistant

**Note**: Your automations using the remote will need to be reconfigured if you uninstall.

## Support

For issues, questions, or feature requests:
- **GitHub Issues**: https://github.com/R00S/eglo-remote-zha/issues
- **Discussions**: https://github.com/R00S/eglo-remote-zha/discussions

## Additional Resources

- **Installation Guide**: [docs/INSTALLATION.md](INSTALLATION.md)
- **Universal Control Guide**: [docs/UNIVERSAL_CONTROL.md](UNIVERSAL_CONTROL.md)
- **3-Bank Solution**: [docs/SOLUTION_3BANKS.md](SOLUTION_3BANKS.md)
- **Button Analysis**: [docs/BUTTON_GROUP_ANALYSIS.md](BUTTON_GROUP_ANALYSIS.md)
- **Implementation Notes**: [docs/IMPLEMENTATION_NOTES.md](IMPLEMENTATION_NOTES.md)

## What's Included

- **3 Custom Quirks**:
  - `eglo_ercu_awox.py`: Basic AwoX quirk (single bank, 22 triggers)
  - `eglo_ercu_awox_3banks.py`: Advanced 3-bank quirk (66 triggers)
  - `eglo_ercu_3groups.py`: TS004F Tuya variant (different device)

- **2 Blueprints**:
  - `eglo_awox_basic.yaml`: Basic single-bank control
  - `eglo_awox_3banks.yaml`: Universal 3-bank control (supports ANY protocol)

- **Comprehensive Documentation**: See the `docs/` directory for detailed guides

## Version Compatibility

- **Home Assistant**: 2025.12.0 or newer
- **ZHA Integration**: Latest version
- **HACS**: Any recent version

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
