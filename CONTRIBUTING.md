# Contributing to Eglo Remote ZHA

> ⚠️ **Note**: This is a development/"hacks" repository. Code is under active reorganization.

Thank you for your interest in contributing to this project! This document provides guidelines for contributing to the Eglo Remote ZHA hacks repository.

## Project Purpose

This is a **community-driven development and testing repository** ("hacks repo") for:
- Custom ZHA quirks for Eglo remote controls
- Home Assistant blueprints for common automation scenarios
- Documentation and guides
- Testing new features before official submission

Our goal is to achieve feature parity with Zigbee2MQTT while leveraging ZHA's native Home Assistant integration.

## Repository Structure

```
eglo-remote-zha/
├── quirks/           # Custom ZHA quirks (Python)
├── blueprints/       # Home Assistant blueprints (YAML)
├── docs/             # Documentation (Markdown)
├── README.md         # Main project documentation
├── CONTRIBUTING.md   # This file
└── LICENSE
```

## How to Contribute

### Reporting Issues

If you encounter problems with the quirk:

1. Check if the issue already exists in the Issues section
2. Provide detailed information:
   - Home Assistant version
   - ZHA version
   - Device pairing logs (from Home Assistant logs)
   - Steps to reproduce the issue
   - Expected vs actual behavior

### Testing

If you want to test the quirk:

1. Install the quirk following the README instructions
2. Pair your Eglo remote
3. Test all buttons (short press, long press, long release)
4. Report your findings


### Code Contributions

#### Improving Quirks

If you want to improve the Python quirks in the `quirks/` directory:

1. Fork the repository
2. Create a branch for your changes
3. Make your modifications to the appropriate quirk file:
   - `quirks/eglo_ercu_3groups.py` for TS004F (Tuya variant)
   - `quirks/eglo_ercu_awox.py` for AwoX variant
4. Test thoroughly with a real device
5. Submit a pull request with:
   - Description of changes
   - Why the changes are needed
   - Test results with your device
   - Device signature if different from documented

#### Blueprint Contributions

If you create useful blueprints in the `blueprints/` directory:

1. Test the blueprint thoroughly with real devices
2. Document all inputs and expected behavior
3. Add comments explaining complex logic
4. Include usage examples in a comment header
5. Submit a pull request with:
   - The blueprint YAML file
   - Description of what it does
   - Test results
   - Any special requirements or limitations

#### Code Style

Follow the existing code style:
- Use Python type hints where appropriate
- Follow PEP 8 guidelines
- Add comments for complex logic
- Keep the code compatible with Home Assistant's ZHA implementation

### Documentation Improvements

Documentation contributions are welcome! This includes:

- Fixing typos or unclear instructions in any `.md` file
- Adding examples to `README.md` or documentation in `docs/`
- Improving installation instructions
- Adding troubleshooting tips to `quirks/README.md` or `blueprints/README.md`
- Creating guides or tutorials

### Blueprint Contributions

If you create useful blueprints using this quirk:

1. Test the blueprint thoroughly
2. Document all inputs and expected behavior
3. Submit a pull request with the blueprint and description
4. Update `blueprints/README.md` with your blueprint information

## Submitting to Official ZHA Device Handlers

This quirk can be submitted to the official [zha-device-handlers](https://github.com/zigpy/zha-device-handlers) repository. If you'd like to help with this:

1. Follow the [zha-device-handlers contribution guidelines](https://github.com/zigpy/zha-device-handlers/blob/dev/CONTRIBUTING.md)
2. Place the quirk in the appropriate manufacturer directory
3. Add tests if possible
4. Submit a pull request

## Questions

If you have questions about contributing, feel free to open an issue with the "question" label.

## Code of Conduct

Be respectful and constructive in all interactions. This is a community project to help everyone get their devices working better.
