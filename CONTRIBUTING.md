# Contributing to Eglo Remote ZHA

Thank you for your interest in contributing to this project! This document provides guidelines for contributing.

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

#### Improving the Quirk

If you want to improve the Python quirk:

1. Fork the repository
2. Create a branch for your changes
3. Make your modifications to `eglo_ercu_3groups.py`
4. Test thoroughly with a real device
5. Submit a pull request with:
   - Description of changes
   - Why the changes are needed
   - Test results

#### Code Style

Follow the existing code style:
- Use Python type hints where appropriate
- Follow PEP 8 guidelines
- Add comments for complex logic
- Keep the code compatible with Home Assistant's ZHA implementation

### Documentation Improvements

Documentation contributions are welcome! This includes:

- Fixing typos or unclear instructions
- Adding examples
- Improving installation instructions
- Adding troubleshooting tips

### Blueprint Contributions

If you create useful blueprints using this quirk:

1. Test the blueprint thoroughly
2. Document all inputs and expected behavior
3. Submit a pull request with the blueprint and description

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
