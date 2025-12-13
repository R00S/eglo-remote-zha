# Eglo Remote ZHA Support

Custom quirk to make the Eglo remote (ERCU_3groups_Zm by AwoX) work better in ZHA (Zigbee Home Automation).

## Device Information

- **Model**: ERCU_3groups_Zm
- **Manufacturer**: AwoX (sold as Eglo)
- **Device ID**: TS004F
- **Manufacturer Code**: _TZ3000_4fjiwweb

This is a 6-button wireless remote control with 3 groups. Each group has two buttons (on/off or up/down).

## Features

- ✅ All 6 buttons working
- ✅ Short press events (on/off)
- ✅ Long press events (dimming up/down)
- ✅ Long release events (stop dimming)
- ✅ Proper device automation triggers
- ✅ Compatible with Home Assistant automations and blueprints

## Installation

### Option 1: Using Custom Quirks Directory (Recommended)

1. Create a `zhaquirks` directory in your Home Assistant configuration folder if it doesn't exist:
   ```
   /config/zhaquirks/
   ```

2. Copy the `eglo_ercu_3groups.py` file to this directory:
   ```
   /config/zhaquirks/eglo_ercu_3groups.py
   ```

3. Add the following to your `configuration.yaml`:
   ```yaml
   zha:
     custom_quirks_path: /config/zhaquirks/
   ```

4. Restart Home Assistant

5. Remove and re-pair your Eglo remote

### Option 2: Contributing to ZHA Device Handlers

This quirk can also be submitted to the official [zha-device-handlers](https://github.com/zigpy/zha-device-handlers) repository for inclusion in future releases.

## Button Mapping

The remote has 6 buttons arranged in 3 groups:

```
┌─────────┬─────────┬─────────┐
│ Button 1│ Button 3│ Button 5│  ← Top row (ON/Bright)
│  (Grp1) │  (Grp2) │  (Grp3) │
├─────────┼─────────┼─────────┤
│ Button 2│ Button 4│ Button 6│  ← Bottom row (OFF/Dim)
│  (Grp1) │  (Grp2) │  (Grp3) │
└─────────┴─────────┴─────────┘
```

### Button Functions

Each button supports:
- **Short Press**: Turn on/off
- **Long Press**: Start dimming (up for top buttons, down for bottom buttons)
- **Long Release**: Stop dimming

## Usage with Home Assistant

After installation, the remote will expose automation triggers for each button action. You can use these in:

1. **Automations**: Create automations in the UI using device triggers
2. **Blueprints**: Use or create blueprints for the remote
3. **Scripts**: Reference the device in your scripts

### Example Automation

```yaml
automation:
  - alias: "Eglo Remote - Button 1 Short Press"
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
```

### Example Blueprint Usage

```yaml
blueprint:
  name: Eglo Remote Control
  description: Control lights with Eglo 3-group remote
  domain: automation
  input:
    remote:
      name: Eglo Remote
      selector:
        device:
          integration: zha
          manufacturer: _TZ3000_4fjiwweb
          model: TS004F
    light_group_1:
      name: Light Group 1
      selector:
        target:
          entity:
            domain: light
    light_group_2:
      name: Light Group 2
      selector:
        target:
          entity:
            domain: light
    light_group_3:
      name: Light Group 3
      selector:
        target:
          entity:
            domain: light

trigger:
  - platform: device
    domain: zha
    device_id: !input remote
    type: remote_button_short_press
    subtype: button_1
    id: "group1_on"
  - platform: device
    domain: zha
    device_id: !input remote
    type: remote_button_short_press
    subtype: button_2
    id: "group1_off"
  # ... (add more triggers as needed)

action:
  - choose:
      - conditions:
          - condition: trigger
            id: "group1_on"
        sequence:
          - service: light.turn_on
            target: !input light_group_1
      - conditions:
          - condition: trigger
            id: "group1_off"
        sequence:
          - service: light.turn_off
            target: !input light_group_1
      # ... (add more conditions as needed)
```

## Comparison with Zigbee2MQTT

This quirk brings the Eglo remote functionality in ZHA to parity with Zigbee2MQTT by:

1. **Proper button mapping**: All 6 buttons are correctly identified and mapped
2. **Action types**: Short press, long press, and long release are all supported
3. **Device automation triggers**: Native Home Assistant device triggers work out of the box
4. **Blueprint compatibility**: Can be used with blueprints just like in Zigbee2MQTT

## Troubleshooting

### Remote not detected correctly
- Remove the device from ZHA
- Restart Home Assistant
- Re-pair the remote (hold any button for 10 seconds until LED flashes)

### Buttons not responding
- Check battery level
- Ensure the quirk is loaded (check ZHA device signature)
- Verify the device shows the correct manufacturer and model

### Automations not triggering
- Use the Home Assistant automation editor to see available triggers
- Check the ZHA event log for incoming events
- Ensure you're using the correct button numbers (1-6)

## Contributing

If you find issues or have improvements, please open an issue or pull request on the [GitHub repository](https://github.com/R00S/eglo-remote-zha).

## License

This project is provided as-is for the Home Assistant community.

## Credits

Based on the ZHA quirk architecture and inspired by similar remote control implementations in the zha-device-handlers repository.
