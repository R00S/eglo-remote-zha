# Terms of Reference: Eglo Remote ZHA Hacks Repository

## Project Overview

This repository serves as a community-driven development and testing environment for Eglo remote controls in Home Assistant's ZHA (Zigbee Home Automation) integration. The project aims to achieve feature parity with Zigbee2MQTT implementations while providing enhanced functionality through custom quirks and blueprints.

## Background

The Eglo remote controls (manufactured by AwoX and sold under the Eglo brand) have limited support in ZHA out-of-the-box. While Zigbee2MQTT has better support for these devices, many users prefer ZHA for its native Home Assistant integration. This repository addresses that gap by providing:

1. Custom ZHA quirks for proper device recognition
2. Working blueprints for common use cases
3. Documentation for different device models
4. A testing ground for new features and improvements

## Supported Devices

### Primary Focus

1. **Eglo ERCU_3groups_Zm (Tuya variant)**
   - **Model**: TS004F
   - **Manufacturer**: _TZ3000_4fjiwweb
   - **Type**: 6-button remote (3 groups × 2 buttons)
   - **Features**: On/Off, Brightness control
   - **Status**: ✅ Fully supported

2. **Eglo ERCU_3groups_Zm (AwoX/Eglo Remote 2.0)**
   - **Model**: ERCU_3groups_Zm
   - **Manufacturer**: AwoX
   - **Alternative Model**: 99099
   - **Type**: Color remote with scene control
   - **Features**: On/Off, Brightness, Color control, Scenes
   - **Status**: 🔄 In development

### Future Targets

Additional Eglo and AwoX remote models may be added based on community demand and device availability.

## Project Goals

### Short-term Goals (Current Release)

1. ✅ Establish repository structure for quirks and blueprints
2. ✅ Fix known blueprint syntax errors
3. ✅ Document supported device models
4. ✅ Create comprehensive installation guide
5. 🔄 Achieve full 3-bank button support in ZHA
6. 🔄 Match Zigbee2MQTT feature set

### Medium-term Goals

1. 🔄 Add double-press and triple-press support
2. 🔄 Create advanced blueprints (scenes, color control, etc.)
3. 🔄 Add support for additional Eglo/AwoX models
4. 🔄 Submit stable quirks to official zha-device-handlers repository
5. 🔄 Create video tutorials and guides

### Long-term Goals

1. ⬜ Community blueprint library
2. ⬜ Automated testing framework
3. ⬜ Web-based configuration tool
4. ⬜ Integration with Home Assistant Blueprint Exchange

## Repository Structure

```
eglo-remote-zha/
├── quirks/                    # ZHA custom quirks
│   ├── __init__.py
│   ├── eglo_ercu_3groups.py  # Tuya TS004F quirk
│   └── eglo_ercu_awox.py     # AwoX variant quirk
├── blueprints/                # Home Assistant blueprints
│   ├── eglo_3group_basic.yaml
│   └── [future blueprints]
├── docs/                      # Documentation
│   ├── DEVICE_SIGNATURE.md
│   ├── TERMS_OF_REFERENCE.md
│   └── [additional docs]
├── README.md                  # Main documentation
├── CONTRIBUTING.md           # Contribution guidelines
└── LICENSE
```

## Development Approach

### Research & Analysis

1. **Zigbee2MQTT Study**: Analyze existing Zigbee2MQTT converters and implementations
2. **Device Testing**: Test quirks with real hardware
3. **Community Feedback**: Incorporate user reports and feature requests
4. **Comparative Analysis**: Compare ZHA capabilities with Zigbee2MQTT

### Development Workflow

1. **Branch Strategy**: Feature branches for new development
2. **Testing**: Test with actual devices before merging
3. **Documentation**: Update docs with every significant change
4. **Community Review**: Solicit feedback on major changes

### Quality Standards

1. **Code Quality**: Follow PEP 8 for Python code
2. **Documentation**: Clear, comprehensive documentation for all features
3. **Testing**: Verify with real hardware when possible
4. **Compatibility**: Maintain backward compatibility when feasible

## Scope

### In Scope

- Custom ZHA quirks for Eglo remote controls
- Home Assistant blueprints for common automation scenarios
- Documentation and installation guides
- Testing and validation with real devices
- Community support and bug fixes
- Integration with official zha-device-handlers (when ready)

### Out of Scope

- Support for non-Eglo/AwoX devices (unless closely related)
- Zigbee2MQTT converters (this is ZHA-focused)
- Home Assistant core modifications
- Hardware repairs or modifications
- Commercial support or warranties

## Success Criteria

The project will be considered successful when:

1. **Feature Parity**: ZHA implementation matches or exceeds Zigbee2MQTT functionality
2. **Community Adoption**: Active use by Home Assistant community members
3. **Stability**: Quirks work reliably without requiring frequent fixes
4. **Documentation**: Comprehensive guides allow users to install and use easily
5. **Upstream Integration**: Stable quirks accepted into official zha-device-handlers

## Known Issues and Limitations

### Current Limitations

1. **Single Endpoint Architecture**: The TS004F variant uses a single endpoint for all buttons, which limits some advanced features
2. **Battery Reporting**: May be infrequent due to device sleep mode
3. **Scene Support**: Not all device variants support scene commands
4. **Testing Coverage**: Limited by available hardware for testing

### Comparison with Zigbee2MQTT

**ZHA Advantages:**
- Native Home Assistant integration
- No separate MQTT broker required
- Direct device triggers in automations

**Zigbee2MQTT Advantages (to match):**
- More mature device converters
- More button events exposed (double-press, etc.)
- Better documentation of device capabilities

## Contributing

We welcome contributions from the community! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

### Ways to Contribute

1. **Testing**: Test quirks with your devices and report results
2. **Blueprints**: Create and share useful automation blueprints
3. **Documentation**: Improve guides and tutorials
4. **Code**: Submit quirk improvements or bug fixes
5. **Support**: Help other users in discussions and issues

## Project Governance

### Maintainer Responsibilities

- Review and merge pull requests
- Maintain documentation
- Coordinate testing efforts
- Engage with community feedback
- Prepare releases

### Community Input

- Issues and discussions are welcome
- Feature requests will be prioritized based on:
  - Community demand
  - Feasibility
  - Device availability for testing
  - Alignment with project goals

## Timeline

### Phase 1: Foundation (Current)
- ✅ Repository reorganization
- ✅ Fix critical blueprint bugs
- ✅ Update documentation
- 🔄 Create Terms of Reference

### Phase 2: Enhancement (Next 3 months)
- Add advanced button events
- Create additional blueprints
- Expand device model support
- Improve testing coverage

### Phase 3: Maturity (6-12 months)
- Submit to official zha-device-handlers
- Create video tutorials
- Build community blueprint library
- Establish automated testing

## Communication

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Pull Requests**: For code contributions
- **Home Assistant Community**: Link to relevant community forum threads

## References

- [Home Assistant ZHA Documentation](https://www.home-assistant.io/integrations/zha/)
- [zha-device-handlers Repository](https://github.com/zigpy/zha-device-handlers)
- [Zigbee2MQTT Supported Devices](https://www.zigbee2mqtt.io/supported-devices/)
- [Home Assistant Community Thread](https://community.home-assistant.io/t/eglo-connect-z-with-home-assistent-cant-find-a-way-to-make-them-usable-with-my-home-assistent/378439/17)

## Version History

- **v1.0** (Current): Initial Terms of Reference, repository reorganization
- **v0.x**: Pre-reorganization development

## License

This project is provided under the terms specified in the LICENSE file. All contributions are made under the same license.

---

**Document Status**: ✅ Active  
**Last Updated**: December 2025  
**Next Review**: March 2026
