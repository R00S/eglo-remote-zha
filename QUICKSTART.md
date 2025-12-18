# Quick Start: Area & Light Selection Blueprint

## Blueprint Import URL

Copy this URL and paste it in Home Assistant Blueprints → Import Blueprint:

```
https://github.com/R00S/eglo-remote-zha/blob/main/blueprints/eglo_awox_area_selection.yaml
```

## Quick Setup (No Manual Helper Creation Needed!)

The blueprint now **automatically creates all required helper entities** on first use!

### Step 1: Assign Remote to an Area

1. Go to **Settings** → **Devices & Services** → **Devices**
2. Find your Eglo remote
3. Click on it and assign it to an area (e.g., "Living Room")
4. This area will be used as the default area

### Step 2: Import Blueprint

1. Go to **Settings** → **Automations & Scenes** → **Blueprints**
2. Click **Import Blueprint**
3. Paste the URL above
4. Click **Preview** then **Import**

### Step 3: Create Automation

1. Go to **Settings** → **Automations & Scenes**
2. Click **Create Automation** → **Use Blueprint**
3. Select **"Eglo Remote - Area & Light Selection"**
4. Configure:
   - **Eglo Remote**: Select your paired remote
   - **Excluded Areas**: Optional - select areas to skip
   - **Power Left Entity**: Optional - entity to toggle
   - **Timeout**: 5 minutes (default)
5. Save with name: "Eglo Remote Control"

### Step 4: Use Your Remote!

On first button press, the blueprint will automatically create:
- `input_select.eglo_remote_<device_name>_current_area`
- `input_select.eglo_remote_<device_name>_current_light`
- `input_text.eglo_remote_<device_name>_default_area`
- `input_datetime.eglo_remote_<device_name>_last_activity`

**Button Functions:**
- **Candle Mode**: Cycle through areas (lights blink to confirm)
- **Colour Middle (short)**: Cycle through lights in current area
- **Colour Middle (long)**: Save current state as favorite
- **Power Right**: Toggle selected area/light
- **Power Left**: Toggle configured entity
- **Favourites (Fav 1/2)**: Recall saved states

## Multiple Remotes

Each remote gets its own set of helper entities automatically based on the device name. You can have as many remotes as you want!

Example:
- Remote "Living Room" → helpers named `eglo_remote_living_room_*`
- Remote "Bedroom" → helpers named `eglo_remote_bedroom_*`

## Troubleshooting

**Can't find remote in ZHA?**
- Make sure ZHA integration is enabled
- Check that the remote is paired (ZHA → Devices)
- Restart Home Assistant

**Blueprint not appearing?**
- Double-check the URL is correct
- Ensure you clicked "Import" after preview
- Check Home Assistant logs for errors

**Automation not triggering?**
- Verify automation is enabled
- Press any button - helpers will be created automatically
- Check Home Assistant logs for helper creation confirmation

**Want to reset to default area?**
- Just wait for the timeout period (default 5 minutes)
- Or reassign the remote device to a different area

## Need Help?

See full documentation:
- [Migration Guide](../docs/MIGRATION_FROM_3BANK.md)
- [User Guide](../docs/AREA_LIGHT_SELECTION_USER_GUIDE.md)
- [Installation Guide](../docs/INSTALLATION.md)
