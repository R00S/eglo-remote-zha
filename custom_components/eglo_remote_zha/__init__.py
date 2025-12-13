"""Eglo remote ZHA custom quirk package."""

from .eglo_ercu_3groups import EgloERCU3Groups
from .eglo_ercu_awox import Awox99099Remote
from .eglo_ercu_awox_3banks import Awox99099Remote3Banks

__all__ = ["EgloERCU3Groups", "Awox99099Remote", "Awox99099Remote3Banks"]

# Integration setup for Home Assistant
async def async_setup(hass, config):
    """Set up the Eglo Remote ZHA component."""
    return True

async def async_setup_entry(hass, entry):
    """Set up Eglo Remote ZHA from a config entry."""
    return True

