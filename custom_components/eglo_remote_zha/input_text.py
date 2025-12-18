"""Input Text entities for Eglo Remote ZHA."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.input_text import InputText
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DOMAIN, EGLO_MANUFACTURER, EGLO_MODEL

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up input text entities for Eglo remotes."""
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
        
        # Get device area
        device_area_name = ""
        if device.area_id:
            from homeassistant.helpers import area_registry as ar
            area_registry = ar.async_get(hass)
            area = area_registry.async_get_area(device.area_id)
            if area:
                device_area_name = area.name
        
        # Create default area text input
        entities.append(
            EgloRemoteInputText(
                unique_id=f"eglo_remote_{ieee_clean}_default_area",
                name=f"Eglo Remote {device.name} Default Area",
                initial=device_area_name or "",
                device=device,
            )
        )
    
    if entities:
        async_add_entities(entities)
        _LOGGER.info(f"Created {len(entities)} input_text entities for Eglo remotes")


class EgloRemoteInputText(InputText):
    """Input Text entity for Eglo Remote."""
    
    def __init__(
        self,
        unique_id: str,
        name: str,
        initial: str,
        device: dr.DeviceEntry,
    ) -> None:
        """Initialize the input text."""
        self._attr_unique_id = unique_id
        self._attr_name = name
        self._attr_native_value = initial
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
    
    async def async_set_value(self, value: str) -> None:
        """Set new value."""
        self._attr_native_value = value
        self.async_write_ha_state()
