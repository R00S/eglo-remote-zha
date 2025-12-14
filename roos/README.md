# Using the Eglo/AwoX 3-Bank Blueprints

## Important: How the 3-Bank System Works

The Eglo/AwoX ERCU_3groups_Zm remote has a unique 3-bank design:

1. **Physical Bank Selection**: Press buttons **1**, **2**, or **3** on the remote to select which bank is active
2. **Per-Bank Triggers**: The remote sends different Zigbee commands for each bank (e.g., `turn_on_1`, `turn_on_2`, `turn_on_3`)
3. **Home Assistant Automation**: You need to create **3 separate automations** - one for each bank

## Setup Instructions

### Step 1: Import the Blueprint

Import either:
- `blueprints/eglo_awox_3banks.yaml` (recommended)
- `roos/eglo99099-blueprint.yaml` (same functionality, different name)

### Step 2: Create 3 Automations

Create **3 separate automations** from the blueprint:

#### Automation 1 - Bank 1
- Name: "Eglo Remote - Bank 1 (Living Room)"
- Select your remote device
- **Bank Number: 1**
- Select lights for Bank 1

#### Automation 2 - Bank 2
- Name: "Eglo Remote - Bank 2 (Bedroom)"
- Select your remote device
- **Bank Number: 2**
- Select lights for Bank 2

#### Automation 3 - Bank 3
- Name: "Eglo Remote - Bank 3 (Kitchen)"
- Select your remote device
- **Bank Number: 3**
- Select lights for Bank 3

### Step 3: Use the Remote

1. **Press button 1, 2, or 3** on the remote to select which bank to control
2. Use the control buttons (on/off, brightness, colors, etc.) to control the selected bank's lights

## How It Works Technically

The 3-bank quirk (`Awox99099Remote3Banks`) exposes **66 separate triggers**:
- 22 actions (on, off, dim up/down, red/green/blue, warm/cold, etc.)
- × 3 banks
- = 66 unique triggers

Each trigger has a bank suffix:
- Bank 1: `turn_on_1`, `dim_up_1`, `red_1`, etc.
- Bank 2: `turn_on_2`, `dim_up_2`, `red_2`, etc.
- Bank 3: `turn_on_3`, `dim_up_3`, `red_3`, etc.

The blueprint uses `enabled` conditions to only listen to triggers matching the selected bank.

## Troubleshooting

### Error: "device does not have trigger"
This means the remote is not using the 3-bank quirk. Check:
1. Device info shows quirk: `custom_components.eglo_remote_zha.eglo_ercu_awox_3banks.Awox99099Remote3Banks`
2. If not, remove and re-pair the device

### Buttons don't respond
1. Make sure you've created an automation for the bank you're trying to use
2. Press the bank button (1, 2, or 3) before using control buttons
3. Check the automation is enabled

### Wrong lights respond
Make sure you selected the correct bank number in each automation configuration.
