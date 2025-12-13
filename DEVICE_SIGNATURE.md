# Device Technical Details

## Device Signature

The Eglo ERCU_3groups_Zm remote reports the following signature when paired:

```python
{
    "node_descriptor": "NodeDescriptor(logical_type=<LogicalType.EndDevice: 2>, complex_descriptor_available=0, user_descriptor_available=0, reserved=0, aps_flags=0, frequency_band=<FrequencyBand.Freq2400MHz: 8>, mac_capability_flags=<MACCapabilityFlags.AllocateAddress: 128>, manufacturer_code=4417, maximum_buffer_size=82, maximum_incoming_transfer_size=82, server_mask=11264, maximum_outgoing_transfer_size=82, descriptor_capability_field=<DescriptorCapability.NONE: 0>, *allocate_address=True, *is_alternate_pan_coordinator=False, *is_coordinator=False, *is_end_device=True, *is_full_function_device=False, *is_mains_powered=False, *is_receiver_on_when_idle=False, *is_router=False, *is_security_capable=False)",
    "endpoints": {
        "1": {
            "profile_id": 260,
            "device_type": "0x0820",
            "in_clusters": [
                "0x0000",  # Basic
                "0x0001",  # PowerConfiguration
                "0x0003",  # Identify
                "0x0004",  # Groups
                "0x0006",  # OnOff
                "0x1000"   # LightLink
            ],
            "out_clusters": [
                "0x0003",  # Identify
                "0x0004",  # Groups
                "0x0005",  # Scenes
                "0x0006",  # OnOff
                "0x0008",  # LevelControl
                "0x0019",  # OTA
                "0x1000"   # LightLink
            ]
        }
    },
    "manufacturer": "_TZ3000_4fjiwweb",
    "model": "TS004F",
    "class": "zigpy.device.Device"
}
```

## Clusters Explained

### Input Clusters (Commands the device receives)

- **Basic (0x0000)**: Device information
- **PowerConfiguration (0x0001)**: Battery status
- **Identify (0x0003)**: Device identification
- **Groups (0x0004)**: Zigbee group management
- **OnOff (0x0006)**: On/Off commands
- **LightLink (0x1000)**: Touchlink commissioning

### Output Clusters (Commands the device sends)

- **Identify (0x0003)**: Identification commands
- **Groups (0x0004)**: Group commands
- **Scenes (0x0005)**: Scene commands
- **OnOff (0x0006)**: On/Off commands
- **LevelControl (0x0008)**: Brightness/level commands
- **OTA (0x0019)**: Over-the-air updates
- **LightLink (0x1000)**: Touchlink commands

## Button Events

The remote sends the following Zigbee commands:

### Short Press (any button)
- **Command**: `on` or `off`
- **Cluster**: OnOff (0x0006)
- **Endpoint**: 1

### Long Press (top buttons)
- **Command**: `move` with `move_mode: 0` (move up)
- **Cluster**: LevelControl (0x0008)
- **Endpoint**: 1

### Long Press (bottom buttons)
- **Command**: `move` with `move_mode: 1` (move down)
- **Cluster**: LevelControl (0x0008)
- **Endpoint**: 1

### Long Release (any button after long press)
- **Command**: `stop`
- **Cluster**: LevelControl (0x0008)
- **Endpoint**: 1

## Pairing Instructions

1. Reset the remote:
   - Press and hold any button for approximately 10 seconds
   - The LED will start flashing rapidly indicating reset mode
   
2. Put your ZHA coordinator in pairing mode

3. Press any button on the remote to complete pairing

## Power Management

- **Power Source**: Battery (2x AAA)
- **Sleep Mode**: Device sleeps when not in use
- **Battery Reporting**: Reports battery percentage via PowerConfiguration cluster
- **Low Battery Warning**: Device sends notification when battery is low

## Zigbee Device Type

- **Profile**: Zigbee Home Automation (ZHA) - 0x0104
- **Device Type**: On/Off Light Switch (0x0820)
- **Endpoint**: 1

## Known Limitations

1. **Single Endpoint**: All buttons operate through endpoint 1
   - In some devices, different buttons use different endpoints
   - This device uses a single endpoint with group-based control

2. **No Scene Support**: While the device has a Scenes output cluster, button presses don't typically trigger scene commands directly

3. **Battery Reporting Interval**: Battery status updates may be infrequent to conserve power

## Comparison with Other Remotes

### vs. Philips Hue Remote
- Similar cluster structure
- Uses PhilipsRemoteCluster as base
- Different manufacturer codes

### vs. IKEA TRADFRI Remote
- TRADFRI uses multiple endpoints
- This device uses single endpoint with group management

### vs. Tuya Remotes
- Uses Tuya manufacturer code (_TZ3000_*)
- Standard Zigbee clusters (not Tuya-specific)
- Compatible with standard ZHA commands

## Debugging

To see raw events from the device:

1. Enable debug logging in Home Assistant:
   ```yaml
   logger:
     default: info
     logs:
       zigpy: debug
       homeassistant.components.zha: debug
   ```

2. Watch the logs when pressing buttons:
   ```
   tail -f /config/home-assistant.log | grep -i "eglo\|ercu\|TS004F"
   ```

3. Use ZHA device information page:
   - Navigate to Configuration → Devices & Services → ZHA
   - Select your remote device
   - Click "Manage Zigbee Device"
   - View clusters and commands

## References

- [Zigbee Cluster Library Specification](https://zigbeealliance.org/wp-content/uploads/2019/12/07-5123-06-zigbee-cluster-library-specification.pdf)
- [ZHA Device Handlers GitHub](https://github.com/zigpy/zha-device-handlers)
- [Zigbee2MQTT Device Database](https://www.zigbee2mqtt.io/devices/)
