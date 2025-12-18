# 3-Bank Functionality Workaround Solution

## Problem Summary

Bank buttons (1/2/3) on the AwoX ERCU_3groups_Zm remote **do not send detectable Zigbee events** to Home Assistant. They operate at the firmware/MAC layer, making automatic bank detection impossible.

## The Solution: Manual Bank Selection

Since we can't auto-detect which bank is active, we use a manual workaround that still gives you full 3-bank functionality.

### How It Works

1. **Create 3 Automations** - One for each bank
2. **Manual Synchronization** - Enable/disable automations to match physical bank selection
3. **Full Control** - Each bank independently controls different lights

## Setup Instructions

### Step 1: Create 3 Automations

Create 3 separate automations using the blueprint `eglo_awox_manual_bank.yaml`:

#### Automation 1 - Bank 1
- Name: "Eglo Remote - Bank 1 (Living Room)"
- Remote: Your AwoX remote
- Target Lights: Living room lights
- **Initially: ENABLED**

#### Automation 2 - Bank 2
- Name: "Eglo Remote - Bank 2 (Bedroom)"  
- Remote: Your AwoX remote
- Target Lights: Bedroom lights
- **Initially: DISABLED**

#### Automation 3 - Bank 3
- Name: "Eglo Remote - Bank 3 (Kitchen)"
- Remote: Your AwoX remote
- Target Lights: Kitchen lights
- **Initially: DISABLED**

### Step 2: Create Bank Switcher Automation (Optional but Recommended)

Create a helper automation that makes switching easier:

```yaml
automation:
  - alias: "Eglo Remote - Bank Switcher"
    trigger:
      - platform: state
        entity_id: input_select.eglo_bank_selector
    action:
      - choose:
          - conditions:
              - condition: state
                entity_id: input_select.eglo_bank_selector
                state: "Bank 1"
            sequence:
              - service: automation.turn_on
                entity_id: automation.eglo_remote_bank_1_living_room
              - service: automation.turn_off
                entity_id:
                  - automation.eglo_remote_bank_2_bedroom
                  - automation.eglo_remote_bank_3_kitchen
          
          - conditions:
              - condition: state
                entity_id: input_select.eglo_bank_selector
                state: "Bank 2"
            sequence:
              - service: automation.turn_on
                entity_id: automation.eglo_remote_bank_2_bedroom
              - service: automation.turn_off
                entity_id:
                  - automation.eglo_remote_bank_1_living_room
                  - automation.eglo_remote_bank_3_kitchen
          
          - conditions:
              - condition: state
                entity_id: input_select.eglo_bank_selector
                state: "Bank 3"
            sequence:
              - service: automation.turn_on
                entity_id: automation.eglo_remote_bank_3_kitchen
              - service: automation.turn_off
                entity_id:
                  - automation.eglo_remote_bank_1_living_room
                  - automation.eglo_remote_bank_2_bedroom
```

### Step 3: Create Input Select Helper

Create an input_select helper:

```yaml
input_select:
  eglo_bank_selector:
    name: Eglo Remote Bank
    options:
      - Bank 1
      - Bank 2
      - Bank 3
    initial: Bank 1
    icon: mdi:numeric-1-box
```

## Usage

### Manual Method (Without Helper)

1. **To control Bank 1 lights**: Go to Settings → Automations, enable "Bank 1", disable "Bank 2" and "Bank 3"
2. **To control Bank 2 lights**: Enable "Bank 2", disable "Bank 1" and "Bank 3"
3. **To control Bank 3 lights**: Enable "Bank 3", disable "Bank 1" and "Bank 2"

### With Helper Automation (Recommended)

1. **Press physical button 1 on remote**
2. **In Home Assistant**: Select "Bank 1" in the dropdown
3. The helper automation automatically enables/disables the correct automations
4. Remote now controls Bank 1 lights

Repeat for banks 2 and 3.

## Alternative: Dashboard Button Method

Add buttons to your dashboard for quick bank switching:

```yaml
type: horizontal-stack
cards:
  - type: button
    name: Bank 1
    icon: mdi:numeric-1-box
    tap_action:
      action: call-service
      service: input_select.select_option
      data:
        entity_id: input_select.eglo_bank_selector
        option: Bank 1
  
  - type: button
    name: Bank 2
    icon: mdi:numeric-2-box
    tap_action:
      action: call-service
      service: input_select.select_option
      data:
        entity_id: input_select.eglo_bank_selector
        option: Bank 2
  
  - type: button
    name: Bank 3
    icon: mdi:numeric-3-box
    tap_action:
      action: call-service
      service: input_select.select_option
      data:
        entity_id: input_select.eglo_bank_selector
        option: Bank 3
```

## Why This Approach?

**Pros**:
- ✅ Full 3-bank functionality
- ✅ Independent control of 3 light groups
- ✅ No Touchlink setup required
- ✅ Works with ANY Home Assistant devices
- ✅ Simple to understand and maintain

**Cons**:
- ⚠️ Requires manual synchronization (one click/tap in HA when you press physical bank button)
- ⚠️ Not truly automatic

## Technical Explanation

The remote's bank buttons operate at the firmware level and change internal state without sending Zigbee commands visible to the coordinator. This is why:

1. **We can't detect** when you press buttons 1/2/3
2. **We can still control** 3 banks by having 3 separate automations
3. **You manually sync** which automation is active to match the physical bank

This workaround gives you the full 3-bank experience with one minor manual step.

## Troubleshooting

### Wrong lights respond
- Check that only ONE bank automation is enabled
- Verify the helper automation is working correctly
- Make sure you've synced Home Assistant with the physical bank button press

### Lights don't respond at all
- Check that at least ONE bank automation is enabled
- Verify the automation is configured with the correct remote device
- Test that the basic remote triggers are working (check ZHA events)

### Helper automation doesn't work
- Verify entity_id names match your actual automation names
- Check that the input_select exists and has the correct options
- Look for errors in Home Assistant logs

## Future Improvements

If a method is discovered to detect bank button presses (e.g., via proprietary cluster commands), this manual synchronization could be automated. For now, this workaround provides full 3-bank functionality with minimal inconvenience.
