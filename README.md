Not ready to use yet

# Eglo Remote ZHA

> 🔧 **Custom ZHA integration for Eglo remote controls with universal device control**

[![GitHub](https://img.shields.io/github/license/R00S/eglo-remote-zha)](LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/R00S/eglo-remote-zha)](https://github.com/R00S/eglo-remote-zha/issues)
[![GitHub stars](https://img.shields.io/github/stars/R00S/eglo-remote-zha)](https://github.com/R00S/eglo-remote-zha/stargazers)
[![HACS](https://img.shields.io/badge/HACS-Integration-41BDF5.svg)](https://github.com/hacs/integration)

---

## 📦 Installation via HACS

This integration can be installed through HACS (Home Assistant Community Store).

### Quick Start

1. **Add repository to HACS**:
   - HACS → Integrations → ⋮ → Custom repositories
   - Repository: `https://github.com/R00S/eglo-remote-zha`
   - Category: **Integration**

2. **Install**: Search for "Eglo Remote ZHA" in HACS and click Download

3. **Restart Home Assistant**

4. **Add Integration via UI**:
   - Settings → Devices & Services → + Add Integration
   - Search for "Eglo Remote ZHA" and add it

5. **Pair your remote** via ZHA

6. **Configure blueprint** to control ANY devices (Zigbee, WiFi, Thread, BLE, RF, Z-Wave, etc.)

📖 **Full installation guide**: [docs/HACS_INSTALLATION.md](docs/HACS_INSTALLATION.md)

---

## 🌟 Key Features

### Intelligent Area & Light Selection
- **Cycle through your Home Assistant areas** with a single button
- **Select individual lights** within each area  
- **Visual feedback**: Lights blink to confirm selection
- **Auto-timeout**: Returns to default area after 5 minutes of inactivity
- **Save defaults**: Long press to save your preferred area and states

### Universal Device Control
Control **ANY Home Assistant light** with your Eglo remote:
- ✅ **Zigbee** (lights, switches, plugs)
- ✅ **WiFi** (TP-Link, Shelly, Tuya, LIFX, etc.)
- ✅ **Thread** (Matter-over-Thread, Nanoleaf, Eve)
- ✅ **Bluetooth** (BLE devices)
- ✅ **Cloud** lights

**No protocol restrictions!**

### Advanced Button Functions
- **All hardware long press** actions implemented
- **Configurable power button** - control any entity
- **Color presets** with temperature cycling
- **Dimming & color temp** with continuous long press
- **Favorite recalls** for area and light defaults

### No Complex Setup Required
- ❌ No Touchlink binding needed
- ❌ No ZHA groups to create
- ❌ No manual bank switching
- ✅ Just select your areas and configure exclusions

---

## 🎮 Remote Control Layout

```
┌─────────────────────────────────┐
│  [1]    [2]    [3]              │  ← Groups/Zones (NO EVENTS)
├─────────────────────────────────┤
│  [ON]              [OFF]        │  ← Power controls
├─────────────────────────────────┤
│  [🔴] [🟢] [🔵] [🔄]           │  ← Color controls
├─────────────────────────────────┤
│  [❤️1]         [❤️2]          │  ← Favorites
├─────────────────────────────────┤
│  [Dim▲]           [Dim▼]        │  ← Brightness
├─────────────────────────────────┤
│  [Warm]           [Cold]        │  ← Color temperature  
├─────────────────────────────────┤
│         [🕯️Candle]             │  ← Cycle areas
└─────────────────────────────────┘
```

### How It Works

1. **Cycle Areas**: Press **Candle Mode** button to cycle through your Home Assistant areas
   - Only cycles through non-excluded areas
   - Lights in selected area blink twice to confirm
   
2. **Select Individual Light**: Press **Middle Color** button to cycle through lights in current area
   - Cycles: All lights → Light 1 → Light 2 → ... → All lights
   - Selected light blinks twice to confirm

3. **Control Selected Area/Light**: Use all other buttons (power, colors, dimming, etc.)
   - Actions apply to currently selected area or light
   
4. **Set Defaults**:
   - **Long press Power Left**: Save current area as default
   - **Long press Power Right**: Save current state as default
   - **Press Fav 1**: Recall default area state
   - **Press Fav 2**: Recall default light state

5. **Auto-Reset**: After 5 minutes of inactivity or HA restart, remote returns to default area

### Detailed Button Functions

**Power Left** (ON):
- Short: Toggle configurable entity (set in blueprint)
- Long: Save current area as default

**Power Right** (OFF):
- Short: Toggle selected area/light
- Long: Save state as default

**Color Buttons** (Top/Left/Right):
- Short: Change to green/red/blue
- Long: Cycle color temp within that color range

**Middle Color** (Cycle):
- Short: Cycle through lights in area

**Candle Mode**:
- Short: Cycle to next area
- From single light: First press → whole area, Second → next area

**Dimming** (Up/Down):
- Short: Adjust by 5%
- Long: Continuous adjustment

**Color Temp** (Warm/Cold):
- Short: Adjust by 5%
- Long: Continuous adjustment

**Favorites**:
- Fav 1: Recall default area state
- Fav 2: Recall default light state

For the simpler Tuya variant (TS004F), see the [quirks documentation](quirks/README.md).

### Installation (AwoX ERCU_3groups_Zm ONLY)

**Note**: These instructions are ONLY for the **AwoX ERCU_3groups_Zm** (Eglo Remote 2.0). If you have the TS004F (Tuya variant), that's a different device entirely.

#### Step 1: Copy the Quirk File

1. **Create the quirks directory** in your Home Assistant configuration:
   ```bash
   mkdir -p /config/zhaquirks
   ```

2. **Copy the AwoX quirk file**:
   ```bash
   cp quirks/eglo_ercu_awox.py /config/zhaquirks/
   ```

#### Step 2: Configure ZHA

Add to your `configuration.yaml`:
```yaml
zha:
  custom_quirks_path: /config/zhaquirks/
```

#### Step 3: Restart and Pair

1. **Restart Home Assistant**

2. **Remove the device** if already paired:
   - Go to Configuration → Devices & Services → ZHA
   - Find the Eglo remote and remove it

3. **Reset the remote**:
   - Hold any button for ~10 seconds until LED flashes rapidly

4. **Pair the device**:
   - Put ZHA in pairing mode
   - Press any button on the remote
   - Wait for pairing to complete

5. **Verify the quirk loaded**:
   - Check device info in ZHA
   - Should show: Manufacturer: "**AwoX**", Model: "**ERCU_3groups_Zm**"
   - Quirk class: "**Awox99099Remote**"
   - **NOT** TS004F or Tuya - that's a different device!

#### Alternative: If You Have the TS004F (Different Device)

If you have the Tuya variant instead:
- Use `quirks/eglo_ercu_3groups.py` instead
- Follow the same installation steps
- See [quirks README](quirks/README.md) for specific instructions

### Installing Blueprints

1. **Assign Remote to Area** (important!):
   - Settings → Devices & Services → Find your remote
   - Assign it to an area (this becomes the default area)

2. **Import the Area Selection Blueprint**:
   ```
   https://github.com/R00S/eglo-remote-zha/blob/main/blueprints/eglo_awox_area_selection.yaml
   ```
   
   Or for basic 3-group control: [`blueprints/eglo_3group_basic.yaml`](blueprints/eglo_3group_basic.yaml)

3. **Create automation from blueprint**:
   - Select your Eglo remote device
   - Set excluded areas if desired
   - Configure timeout settings
   - **No manual helper creation needed!** - Auto-created on first use

## 📚 Documentation

### Repository Structure

```
eglo-remote-zha/
├── quirks/                    # ZHA custom quirks
│   ├── eglo_ercu_3groups.py  # Tuya TS004F quirk
│   └── eglo_ercu_awox.py     # AwoX variant quirk
├── blueprints/                # Home Assistant blueprints
│   └── eglo_3group_basic.yaml
├── docs/                      # Documentation
│   ├── DEVICE_SIGNATURE.md   # Technical device details
│   └── TERMS_OF_REFERENCE.md # Project goals and roadmap
├── README.md                  # This file
└── CONTRIBUTING.md           # Contribution guidelines
```

### Available Documentation

- 📖 [Terms of Reference](docs/TERMS_OF_REFERENCE.md) - Project goals, roadmap, and governance
- 🔧 [Device Technical Details](docs/DEVICE_SIGNATURE.md) - Zigbee clusters, endpoints, and debugging
- 🤝 [Contributing Guide](CONTRIBUTING.md) - How to contribute to the project

## 💡 Usage Examples

### Basic Automation (Manual YAML)

```yaml
automation:
  - alias: "Eglo Remote - Group 1 On"
    trigger:
      - platform: device
        domain: zha
        device_id: YOUR_DEVICE_ID
        type: remote_button_short_press
        subtype: button_1
    action:
      - service: light.turn_on
        target:
          entity_id: light.living_room
        data:
          brightness_pct: 100
```

### Using the Blueprint

The included blueprint handles all 3 groups with on/off and brightness control:

1. **Import the blueprint** (see installation section)
2. **Create automation** from blueprint
3. **Configure inputs**:
   - Select your Eglo remote device
   - Assign lights to Group 1, 2, and 3
   - Set brightness step percentage (5-25%)

The blueprint automatically handles:
- Short press → Turn on/off at 100% brightness
- Long press → Continuous brightness adjustment
- Long release → Stop brightness adjustment

## 🔍 Comparison with Zigbee2MQTT

| Feature | ZHA (This Quirk) | Zigbee2MQTT | Status |
|---------|------------------|-------------|--------|
| All 6 buttons working | ✅ Yes | ✅ Yes | ✅ Parity |
| Short press events | ✅ Yes | ✅ Yes | ✅ Parity |
| Long press events | ✅ Yes | ✅ Yes | ✅ Parity |
| Long release events | ✅ Yes | ✅ Yes | ✅ Parity |
| Double press | ⏳ Planned | ✅ Yes | 🔄 In Progress |
| Triple press | ⏳ Planned | ✅ Yes | 🔄 In Progress |
| Native HA integration | ✅ Yes | ❌ No (MQTT) | ✅ ZHA Advantage |
| Device triggers | ✅ Yes | ⚠️ Via MQTT | ✅ ZHA Advantage |
| Battery reporting | ✅ Yes | ✅ Yes | ✅ Parity |

**Our Goal**: Achieve 100% feature parity with Zigbee2MQTT while maintaining ZHA's native integration advantages.

## 🐛 Troubleshooting

### Remote Not Detected Correctly

1. Remove the device from ZHA
2. Restart Home Assistant
3. Ensure the quirk file is in the correct directory
4. Re-pair the remote (hold button for 10 seconds until LED flashes)
5. Check ZHA logs for quirk loading messages

### Buttons Not Responding

- Check battery level (replace with fresh AAA batteries)
- Verify the quirk is loaded: Check device info in ZHA
- Ensure correct manufacturer and model are shown
- Try re-pairing the device

### Automations Not Triggering

- Use the automation editor to see available triggers
- Check the ZHA event log for incoming button events
- Verify you're using the correct button numbers (1-6)
- Test with a simple automation first

### Enable Debug Logging

Add to `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    zigpy: debug
    homeassistant.components.zha: debug
```

Then watch logs:
```bash
tail -f /config/home-assistant.log | grep -i "eglo\|ercu\|TS004F"
```

## 🤝 Contributing

This is a community project! We welcome contributions of all kinds:

- 🧪 **Testing**: Test quirks with your devices and report results
- 📝 **Documentation**: Improve guides, add examples, fix typos
- 💻 **Code**: Submit quirk improvements or new features
- 🎨 **Blueprints**: Create and share automation blueprints
- 💬 **Support**: Help other users in issues and discussions

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Roadmap

See our [Terms of Reference](docs/TERMS_OF_REFERENCE.md) for the complete project roadmap. Key upcoming features:

- 🔄 Advanced button events (double-press, triple-press)
- 🔄 Additional device model support
- 🔄 Enhanced blueprints for scenes and color control
- 🔄 Submission to official zha-device-handlers
- 🔄 Video tutorials and guides

## 📖 References & Resources

### Related Projects & Documentation

- [Home Assistant ZHA Documentation](https://www.home-assistant.io/integrations/zha/)
- [zha-device-handlers Repository](https://github.com/zigpy/zha-device-handlers)
- [Zigbee2MQTT Supported Devices](https://www.zigbee2mqtt.io/supported-devices/)
- [Zigbee Cluster Library Specification](https://zigbeealliance.org/wp-content/uploads/2019/12/07-5123-06-zigbee-cluster-library-specification.pdf)

### Community Discussion

- [Home Assistant Community Thread](https://community.home-assistant.io/t/eglo-connect-z-with-home-assistent-cant-find-a-way-to-make-them-usable-with-my-home-assistent/378439/17) - Original discussion about Eglo remote support

### Zigbee2MQTT Implementation References

For reference on how Zigbee2MQTT handles these devices (learning purposes only, this is a ZHA project):
- Search Zigbee2MQTT device database for "Eglo" or "AwoX"
- Compare exposed button events and capabilities
- Note: We aim to match or exceed their feature set in ZHA

## 📜 License

This project is provided as-is for the Home Assistant community. See [LICENSE](LICENSE) for details.

## 🙏 Credits

- Based on the ZHA quirk architecture
- Inspired by similar remote control implementations in zha-device-handlers
- Community feedback and testing from Home Assistant users
- Zigbee2MQTT project for reference implementations

## ⚠️ Disclaimer

This is a community-maintained "hacks repository" for development and testing. While we strive for quality and stability:

- Test thoroughly in your own environment before relying on these quirks
- No warranties or guarantees are provided
- Use at your own risk
- Always maintain backups of your Home Assistant configuration

---

**🌟 Star this repository** if you find it useful!  
**🐛 Report issues** to help improve the project  
**💬 Join discussions** to share ideas and get help  
**🤝 Contribute** to make ZHA better for everyone

Made with ❤️ by the Home Assistant community
