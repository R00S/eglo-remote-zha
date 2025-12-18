"""Eglo Remote ZHA - Custom quirks for AwoX ERCU_3groups_Zm remote.

This integration provides ZHA device handlers (quirks) for the Eglo/AwoX
ERCU_3groups_Zm remote control, enabling:
- Area/light selection system with persistent state storage
- 22 unique automation triggers (all buttons with long press support)
- Universal device control (any HA protocol: Zigbee, WiFi, Thread, BLE, RF, etc.)
- Long press support for applicable buttons

The quirks are automatically registered with ZHA when this integration loads.
Persistent state storage is handled via Home Assistant's Store class.
"""

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall, SupportsResponse
from homeassistant.helpers.storage import Store

_LOGGER = logging.getLogger(__name__)

# Import quirk classes so they're registered with zigpy/ZHA
# These imports happen at module load time, before async_setup_entry is called
# When Python executes these imports, the CustomDevice classes are defined
# and automatically registered with zigpy's DEVICE_REGISTRY
try:
    from .eglo_ercu_3groups import EgloERCU3Groups
    # Use basic Awox quirk - provides standard triggers without bank suffixes
    # Area/light selection is handled by blueprints with persistent storage
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
STORAGE_VERSION = 1
STORAGE_KEY = "eglo_remote_zha_state"

# Service names
SERVICE_SET_STATE = "set_state"
SERVICE_GET_STATE = "get_state"


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Eglo Remote ZHA component from configuration.yaml."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Eglo Remote ZHA from a config entry."""
    
    # Initialize persistent storage
    store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
    
    # Load existing state or initialize empty dict
    stored_data = await store.async_load() or {}
    
    # Store in hass.data for access by blueprints/automations
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["store"] = store
    hass.data[DOMAIN]["state"] = stored_data
    
    _LOGGER.info(
        "Eglo Remote ZHA integration enabled - ZHA quirks are active for: "
        "AwoX ERCU_3groups_Zm (99099), Tuya TS004F (_TZ3000_4fjiwweb)"
    )
    _LOGGER.info(
        "When you pair an Eglo remote via ZHA, the custom quirk will be "
        "automatically applied based on the device signature"
    )
    _LOGGER.info(
        "Persistent state storage initialized - %d remote(s) configured",
        len(stored_data)
    )
    
    # Register services for state management
    async def handle_set_state(call: ServiceCall) -> None:
        """Handle set_state service call."""
        device_id = call.data.get("device_id")
        key = call.data.get("key")
        value = call.data.get("value")
        
        if not device_id or not key:
            _LOGGER.error("set_state requires device_id and key parameters")
            return
        
        # Ensure device entry exists
        if device_id not in hass.data[DOMAIN]["state"]:
            hass.data[DOMAIN]["state"][device_id] = {}
        
        # Set the value
        hass.data[DOMAIN]["state"][device_id][key] = value
        
        # Persist to disk
        await hass.data[DOMAIN]["store"].async_save(hass.data[DOMAIN]["state"])
        
        _LOGGER.debug("State updated for %s: %s = %s", device_id, key, value)
    
    async def handle_get_state(call: ServiceCall) -> dict[str, Any]:
        """Handle get_state service call."""
        device_id = call.data.get("device_id")
        key = call.data.get("key")
        default = call.data.get("default")
        
        if not device_id:
            _LOGGER.error("get_state requires device_id parameter")
            return {"value": default}
        
        device_state = hass.data[DOMAIN]["state"].get(device_id, {})
        
        if key:
            value = device_state.get(key, default)
        else:
            value = device_state
        
        return {"value": value}
    
    hass.services.async_register(DOMAIN, SERVICE_SET_STATE, handle_set_state)
    hass.services.async_register(
        DOMAIN, 
        SERVICE_GET_STATE, 
        handle_get_state,
        supports_response=SupportsResponse.ONLY
    )
    
    _LOGGER.info("Registered services: %s.set_state, %s.get_state", DOMAIN, DOMAIN)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    
    # Unregister services
    hass.services.async_remove(DOMAIN, SERVICE_SET_STATE)
    hass.services.async_remove(DOMAIN, SERVICE_GET_STATE)
    
    # Clean up hass.data
    if DOMAIN in hass.data:
        hass.data.pop(DOMAIN)
    
    _LOGGER.info("Eglo Remote ZHA integration disabled")
    return True


