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

# Import quirk classes so they're registered with zigpy/ZHA
from .eglo_ercu_3groups import EgloERCU3Groups
from .eglo_ercu_awox import Awox99099Remote
from .eglo_ercu_awox_3banks import Awox99099Remote3Banks

_LOGGER = logging.getLogger(__name__)

__all__ = ["EgloERCU3Groups", "Awox99099Remote", "Awox99099Remote3Banks"]

DOMAIN = "eglo_remote_zha"


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Eglo Remote ZHA component from configuration.yaml."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Eglo Remote ZHA from a config entry."""
    _LOGGER.info(
        "Eglo Remote ZHA quirks loaded - quirks registered with ZHA: "
        "Awox99099Remote, Awox99099Remote3Banks, EgloERCU3Groups"
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True


