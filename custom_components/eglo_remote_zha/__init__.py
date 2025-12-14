"""Eglo Remote ZHA - Custom quirks for AwoX ERCU_3groups_Zm remote.

This integration provides ZHA device handlers (quirks) for the Eglo/AwoX
ERCU_3groups_Zm remote control, enabling:
- 3-bank control (buttons 1/2/3 for group selection)
- 66 unique automation triggers (22 actions × 3 banks)
- Universal device control (any HA protocol: Zigbee, WiFi, Thread, BLE, RF, etc.)
- Long press support for applicable buttons

The quirks are automatically registered with ZHA when this integration loads.
"""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

# Import quirk classes so they're registered with zigpy/ZHA
# These imports happen at module load time, before async_setup_entry is called
# When Python executes these imports, the CustomDevice classes are defined
# and automatically registered with zigpy's DEVICE_REGISTRY
try:
    from .eglo_ercu_3groups import EgloERCU3Groups
    # Import 3-bank quirk as default for AwoX ERCU_3groups_Zm
    # The basic Awox99099Remote quirk is kept in the codebase for reference
    # but not imported, so the 3-bank version is used by default
    # from .eglo_ercu_awox import Awox99099Remote
    from .eglo_ercu_awox_3banks import Awox99099Remote3Banks
    
    _LOGGER.debug(
        "Eglo Remote ZHA quirks imported successfully: "
        "Awox99099Remote3Banks (default for AwoX), EgloERCU3Groups"
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

__all__ = ["EgloERCU3Groups", "Awox99099Remote3Banks"]

DOMAIN = "eglo_remote_zha"


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Eglo Remote ZHA component from configuration.yaml."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Eglo Remote ZHA from a config entry."""
    _LOGGER.info(
        "Eglo Remote ZHA integration enabled - ZHA quirks are active for: "
        "AwoX ERCU_3groups_Zm (99099), Tuya TS004F (_TZ3000_4fjiwweb)"
    )
    _LOGGER.info(
        "When you pair an Eglo remote via ZHA, the custom quirk will be "
        "automatically applied based on the device signature"
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info("Eglo Remote ZHA integration disabled")
    return True


