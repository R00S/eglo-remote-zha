# Quick Start: Area & Light Selection Blueprint

## Blueprint Import URL

Copy this URL and paste it in Home Assistant Blueprints → Import Blueprint:

```
https://github.com/R00S/eglo-remote-zha/blob/main/blueprints/eglo_awox_area_selection.yaml
```

## Step-by-Step Setup

### Step 1: Create Helper Entities

Go to **Settings** → **Devices & Services** → **Helpers** and create:

1. **Dropdown**: `Eglo Remote Current Area`
   - Entity ID: `input_select.eglo_remote_current_area`
   - Icon: `mdi:floor-plan`
   - Options: Leave empty

2. **Dropdown**: `Eglo Remote Current Light`
   - Entity ID: `input_select.eglo_remote_current_light`
   - Icon: `mdi:lightbulb`
   - Options: `all`

3. **Text**: `Eglo Remote Default Area`
   - Entity ID: `input_text.eglo_remote_default_area`
   - Icon: `mdi:home-floor-0`

4. **Date/Time**: `Eglo Remote Last Activity`
   - Entity ID: `input_datetime.eglo_remote_last_activity`
   - Icon: `mdi:clock-outline`
   - Enable both date and time

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
   - **Default Area**: Select your primary area (e.g., Living Room)
   - **Excluded Areas**: Optional - select areas to skip
   - **Power Left Entity**: Optional - entity to toggle
   - **Helper Entities**: Select the 4 helpers you created
   - **Timeout**: 5 minutes (default)
5. Save with name: "Eglo Remote Control"

### Step 4: Use Your Remote!

**Button Functions:**
- **Candle Mode**: Cycle through areas (lights blink to confirm)
- **Colour Middle (short)**: Cycle through lights in current area
- **Colour Middle (long)**: Save current state as favorite
- **Power Right**: Toggle selected area/light
- **Power Left**: Toggle configured entity
- **Favourites (Fav 1/2)**: Recall saved states

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
- Verify all helper entities are created
- Check automation is enabled
- Test in Home Assistant Developer Tools → Events

## Need Help?

See full documentation:
- [Migration Guide](../docs/MIGRATION_FROM_3BANK.md)
- [User Guide](../docs/AREA_LIGHT_SELECTION_USER_GUIDE.md)
- [Installation Guide](../docs/INSTALLATION.md)
