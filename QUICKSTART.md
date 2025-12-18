# Quick Start: Area & Light Selection Blueprint

## Blueprint Import URL

Copy this URL and paste it in Home Assistant Blueprints → Import Blueprint:

```
https://github.com/R00S/eglo-remote-zha/blob/main/blueprints/eglo_awox_area_selection.yaml
```

## Quick Setup (Automatic Helper Creation!)

The integration **automatically creates all required helper entities** when you pair your remote!

### Step 1: Install Integration & Pair Remote

1. Install the Eglo Remote ZHA integration via HACS
2. Restart Home Assistant
3. Go to **Settings** → **Devices & Services** → **ZHA**
4. Pair your Eglo remote
5. **Helpers are auto-created immediately!**

### Step 2: Assign Remote to an Area

1. Go to **Settings** → **Devices & Services** → **Devices**
2. Find your Eglo remote
3. Click on it and assign it to an area (e.g., "Living Room")
4. This area will be used as the default area

### Step 3: Import Blueprint

1. Go to **Settings** → **Automations & Scenes** → **Blueprints**
2. Click **Import Blueprint**
3. Paste the URL above
4. Click **Preview** then **Import**

### Step 4: Create Automation

1. Go to **Settings** → **Automations & Scenes**
2. Click **Create Automation** → **Use Blueprint**
3. Select **"Eglo Remote - Area & Light Selection"**
4. Configure:
   - **Eglo Remote**: Select your paired remote
   - **Current Area Helper**: Select `input_select.eglo_remote_..._current_area`
   - **Current Light Helper**: Select `input_select.eglo_remote_..._current_light`
   - **Default Area Helper**: Select `input_text.eglo_remote_..._default_area`
   - **Last Activity Helper**: Select `input_datetime.eglo_remote_..._last_activity`
   - **Excluded Areas**: Optional - select areas to skip
   - **Power Left Entity**: Optional - entity to toggle
   - **Timeout**: 5 minutes (default)
5. Save with name: "Eglo Remote Control"

### Step 5: Use Your Remote!

The auto-created helpers are already initialized with:
- Current area: Set to your device's assigned area
- Current light: Set to "all" (entire area)
- Default area: Set to your device's assigned area
- Last activity: Set to current time

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
