"""Eglo Remote ZHA - Custom quirks and helper management for AwoX ERCU_3groups_Zm remote.

This integration provides:
- ZHA device handlers (quirks) for the Eglo/AwoX ERCU_3groups_Zm remote control
- Automatic helper entity creation for area/light selection system
- 22 unique automation triggers (all buttons with long press support)
- Universal device control (any HA protocol: Zigbee, WiFi, Thread, BLE, RF, etc.)

The quirks are automatically registered with ZHA when this integration loads.
Helper entities are auto-created when a remote is paired.
"""

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_COMPONENT_LOADED, Platform
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.helpers.entity_platform import AddEntitiesCallback

_LOGGER = logging.getLogger(__name__)

# Import quirk classes so they're registered with zigpy/ZHA
try:
    from .eglo_ercu_3groups import EgloERCU3Groups
    from .eglo_ercu_awox import Awox99099Remote
    
    _LOGGER.debug(
        "Eglo Remote ZHA quirks imported successfully: "
        "Awox99099Remote (simplified), EgloERCU3Groups"
    )
except ImportError as err:
    _LOGGER.error(
        "Failed to import Eglo Remote ZHA quirks. This usually means zigpy is not "
        "installed or ZHA is not enabled. Error: %s", err
    )
    raise
except Exception as err:
    _LOGGER.error(
        "Unexpected error loading Eglo Remote ZHA quirks: %s", err
    )
    raise

__all__ = ["EgloERCU3Groups", "Awox99099Remote"]

DOMAIN = "eglo_remote_zha"
PLATFORMS = [Platform.INPUT_SELECT, Platform.INPUT_TEXT, Platform.INPUT_DATETIME]

# Device identifiers for Eglo remotes
EGLO_MANUFACTURER = "AwoX"
EGLO_MODEL = "ERCU_3groups_Zm"


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Eglo Remote ZHA component from configuration.yaml."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Eglo Remote ZHA from a config entry."""
    _LOGGER.info(
        "Eglo Remote ZHA integration enabled - ZHA quirks are active for: "
        "AwoX ERCU_3groups_Zm (99099)"
    )
    
    # Store integration data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {}
    
    # Set up entity platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Listen for ZHA devices to create helpers
    async def handle_zha_device_joined(event: Event) -> None:
        """Handle ZHA device joined event to create helpers."""
        device_ieee = event.data.get("ieee")
        if not device_ieee:
            return
            
        # Get device from registry
        device_registry = dr.async_get(hass)
        device = None
        for dev in device_registry.devices.values():
            for identifier in dev.identifiers:
                if identifier[1] == device_ieee:
                    device = dev
                    break
            if device:
                break
        
        if not device:
            return
            
        # Check if it's an Eglo remote
        if device.manufacturer != EGLO_MANUFACTURER or device.model != EGLO_MODEL:
            return
            
        _LOGGER.info(f"Eglo remote detected: {device.name} ({device_ieee})")
        
        # Create helpers for this remote
        await create_helpers_for_device(hass, device)
    
    # Listen for ZHA device joins
    hass.bus.async_listen("zha_event", handle_zha_device_joined)
    
    # Also check for existing devices on startup
    async def check_existing_devices(event: Event) -> None:
        """Check for existing Eglo remotes and create helpers if needed."""
        if event.data.get("domain") != "zha":
            return
            
        device_registry = dr.async_get(hass)
        for device in device_registry.devices.values():
            if device.manufacturer == EGLO_MANUFACTURER and device.model == EGLO_MODEL:
                await create_helpers_for_device(hass, device)
    
    hass.bus.async_listen_once(EVENT_COMPONENT_LOADED, check_existing_devices)
    
    return True


async def create_helpers_for_device(hass: HomeAssistant, device: dr.DeviceEntry) -> None:
    """Create helper entities for an Eglo remote device."""
    entity_registry = er.async_get(hass)
    
    # Use device IEEE as unique identifier for helpers
    device_ieee = None
    for identifier in device.identifiers:
        if identifier[0] == "zha":
            device_ieee = identifier[1]
            break
    
    if not device_ieee:
        _LOGGER.error(f"Could not get IEEE for device {device.name}")
        return
    
    # Sanitize IEEE for entity ID (remove colons)
    ieee_clean = device_ieee.replace(":", "")
    
    # Get device area if assigned
    device_area_id = device.area_id
    device_area_name = ""
    if device_area_id:
        from homeassistant.helpers import area_registry as ar
        area_registry = ar.async_get(hass)
        area = area_registry.async_get_area(device_area_id)
        if area:
            device_area_name = area.name
    
    # Define helpers to create
    helpers = [
        {
            "domain": "input_select",
            "unique_id": f"eglo_remote_{ieee_clean}_current_area",
            "name": f"Eglo Remote {device.name} Current Area",
            "options": ["all"],
            "initial": device_area_name or "all",
        },
        {
            "domain": "input_select",
            "unique_id": f"eglo_remote_{ieee_clean}_current_light",
            "name": f"Eglo Remote {device.name} Current Light",
            "options": ["all"],
            "initial": "all",
        },
        {
            "domain": "input_text",
            "unique_id": f"eglo_remote_{ieee_clean}_default_area",
            "name": f"Eglo Remote {device.name} Default Area",
            "initial": device_area_name or "",
        },
        {
            "domain": "input_datetime",
            "unique_id": f"eglo_remote_{ieee_clean}_last_activity",
            "name": f"Eglo Remote {device.name} Last Activity",
            "has_date": True,
            "has_time": True,
        },
    ]
    
    # Create each helper if it doesn't exist
    for helper in helpers:
        entity_id = f"{helper['domain']}.{helper['unique_id']}"
        
        # Check if already exists
        if entity_registry.async_get(entity_id):
            _LOGGER.debug(f"Helper already exists: {entity_id}")
            continue
        
        # Create the helper entity
        _LOGGER.info(f"Creating helper entity: {entity_id}")
        
        # Call the appropriate service to create the helper
        service_data = {
            "name": helper["name"],
        }
        
        if helper["domain"] == "input_select":
            service_data["options"] = helper["options"]
        elif helper["domain"] == "input_datetime":
            service_data["has_date"] = helper["has_date"]
            service_data["has_time"] = helper["has_time"]
        
        try:
            # Note: We need to use the config entry service calls, not direct entity creation
            # This will be handled by the entity platforms we're setting up
            pass  # Platform entities will be created via entity platforms
        except Exception as err:
            _LOGGER.error(f"Failed to create helper {entity_id}: {err}")


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
        _LOGGER.info("Eglo Remote ZHA integration disabled")
    
    return unload_ok


