"""Input DateTime entities for Eglo Remote ZHA."""
from __future__ import annotations

from datetime import datetime
import logging
from typing import Any

from homeassistant.components.input_datetime import InputDatetime
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from . import DOMAIN, EGLO_MANUFACTURER, EGLO_MODEL

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up input datetime entities for Eglo remotes."""
    device_registry = dr.async_get(hass)
    entities = []
    
    # Find all Eglo remote devices
    for device in device_registry.devices.values():
        if device.manufacturer != EGLO_MANUFACTURER or device.model != EGLO_MODEL:
            continue
        
        # Get device IEEE
        device_ieee = None
        for identifier in device.identifiers:
            if identifier[0] == "zha":
                device_ieee = identifier[1]
                break
        
        if not device_ieee:
            continue
        
        ieee_clean = device_ieee.replace(":", "")
        
        # Create last activity datetime input
        entities.append(
            EgloRemoteInputDatetime(
                unique_id=f"eglo_remote_{ieee_clean}_last_activity",
                name=f"Eglo Remote {device.name} Last Activity",
                has_date=True,
                has_time=True,
                device=device,
            )
        )
    
    if entities:
        async_add_entities(entities)
        _LOGGER.info(f"Created {len(entities)} input_datetime entities for Eglo remotes")


class EgloRemoteInputDatetime(InputDatetime):
    """Input DateTime entity for Eglo Remote."""
    
    def __init__(
        self,
        unique_id: str,
        name: str,
        has_date: bool,
        has_time: bool,
        device: dr.DeviceEntry,
    ) -> None:
        """Initialize the input datetime."""
        self._attr_unique_id = unique_id
        self._attr_name = name
        self._attr_has_date = has_date
        self._attr_has_time = has_time
        self._attr_native_value = dt_util.now()
        self._device = device
    
    @property
    def device_info(self) -> dict[str, Any]:
        """Return device info to link entity to device."""
        return {
            "identifiers": self._device.identifiers,
            "name": self._device.name,
            "manufacturer": self._device.manufacturer,
            "model": self._device.model,
        }
    
    async def async_set_value(self, value: datetime) -> None:
        """Set new value."""
        self._attr_native_value = value
        self.async_write_ha_state()
