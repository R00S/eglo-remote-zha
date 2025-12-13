# Eglo Remote ZHA Hacks Repository

> 🔧 **Community-driven development and testing for Eglo remote controls in Home Assistant ZHA**

[![GitHub](https://img.shields.io/github/license/R00S/eglo-remote-zha)](LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/R00S/eglo-remote-zha)](https://github.com/R00S/eglo-remote-zha/issues)
[![GitHub stars](https://img.shields.io/github/stars/R00S/eglo-remote-zha)](https://github.com/R00S/eglo-remote-zha/stargazers)

---

## ⚠️ UNDER ACTIVE DEVELOPMENT

**🚧 This repository is currently being reorganized and is under active development. 🚧**

**Status**: The quirks and blueprints are being restructured, tested, and documented. While the code may work, documentation and installation instructions are still being finalized.

**Please check back soon or watch this repository for updates!**

- ✅ Repository structure: In progress
- ✅ Documentation: Being updated
- 🔄 Testing: Ongoing
- 🔄 Final validation: Pending

**For now, consider this a "hacks repo" for experimental use and testing. Stable releases will be tagged when ready.**

---

This repository serves as a development and testing environment ("hacks repo") for making Eglo remote controls work seamlessly with Home Assistant's ZHA (Zigbee Home Automation) integration. Our goal is to achieve feature parity with Zigbee2MQTT implementations while providing enhanced functionality through custom quirks and blueprints.

## 🎯 Project Status

**Current State**: Active development - Repository reorganized as hacks/development environment

**What Works**:
- ✅ All 6 buttons (3 groups) working in ZHA
- ✅ Short press events (on/off)
- ✅ Long press events (dimming up/down)
- ✅ Long release events (stop dimming)
- ✅ Working blueprints for basic automation
- ✅ Proper device automation triggers

**In Progress**:
- 🔄 Advanced button events (double-press, triple-press)
- 🔄 Support for additional Eglo/AwoX models
- 🔄 Enhanced color control blueprints
- 🔄 Matching Zigbee2MQTT feature completeness

## 📱 Supported Devices

### Currently Supported

#### Eglo ERCU_3groups_Zm (Tuya Variant) - **Fully Supported** ✅
- **Model**: TS004F
- **Manufacturer Code**: _TZ3000_4fjiwweb
- **Type**: 6-button remote (3 groups × 2 buttons)
- **Features**: On/Off, Brightness control
- **Quirk**: [`quirks/eglo_ercu_3groups.py`](quirks/eglo_ercu_3groups.py)

#### Eglo ERCU_3groups_Zm (AwoX Variant) - **In Development** 🔄
- **Model**: ERCU_3groups_Zm / 99099
- **Manufacturer**: AwoX (Eglo Remote 2.0)
- **Type**: Color remote with scene control
- **Features**: On/Off, Brightness, Color control, Scenes
- **Quirk**: [`quirks/eglo_ercu_awox.py`](quirks/eglo_ercu_awox.py)

### Button Layout

All variants have 6 buttons arranged in 3 groups:

```
┌─────────┬─────────┬─────────┐
│ Button 1│ Button 3│ Button 5│  ← Top row (ON/Bright)
│ Group 1 │ Group 2 │ Group 3 │
├─────────┼─────────┼─────────┤
│ Button 2│ Button 4│ Button 6│  ← Bottom row (OFF/Dim)
│ Group 1 │ Group 2 │ Group 3 │
└─────────┴─────────┴─────────┘
```

Each button supports:
- **Short Press**: Turn on/off or trigger action
- **Long Press**: Start dimming (up for top buttons, down for bottom buttons)
- **Long Release**: Stop dimming

## 🚀 Quick Start

### Installation

#### Option 1: Using Custom Quirks Directory (Recommended)

1. **Create the quirks directory** in your Home Assistant configuration:
   ```bash
   mkdir -p /config/zhaquirks
   ```

2. **Copy the appropriate quirk file**:
   - For **TS004F** (Tuya variant): Copy `quirks/eglo_ercu_3groups.py`
   - For **AwoX** variant: Copy `quirks/eglo_ercu_awox.py`
   
   ```bash
   # Example for TS004F
   cp quirks/eglo_ercu_3groups.py /config/zhaquirks/
   ```

3. **Configure ZHA** to use custom quirks in `configuration.yaml`:
   ```yaml
   zha:
     custom_quirks_path: /config/zhaquirks/
   ```

4. **Restart Home Assistant**

5. **Remove and re-pair your Eglo remote**:
   - Remove the device from ZHA
   - Reset the remote (hold any button for ~10 seconds until LED flashes)
   - Put ZHA in pairing mode
   - Press any button on the remote to pair

#### Option 2: Contributing to ZHA Device Handlers

This quirk can be submitted to the official [zha-device-handlers](https://github.com/zigpy/zha-device-handlers) repository. See our [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Installing Blueprints

1. **Navigate to Home Assistant Blueprints**:
   - Configuration → Blueprints → Import Blueprint

2. **Import from URL** or **copy the YAML**:
   - Basic 3-group control: [`blueprints/eglo_3group_basic.yaml`](blueprints/eglo_3group_basic.yaml)

3. **Create automation from blueprint**:
   - Select your Eglo remote device
   - Configure your light groups
   - Adjust brightness step if needed

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
