"""Input Select entities for Eglo Remote ZHA."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.input_select import InputSelect
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
    """Set up input select entities for Eglo remotes."""
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
        
        # Create current area selector
        entities.append(
            EgloRemoteInputSelect(
                unique_id=f"eglo_remote_{ieee_clean}_current_area",
                name=f"Eglo Remote {device.name} Current Area",
                options=["all"],
                initial=device_area_name or "all",
                device=device,
            )
        )
        
        # Create current light selector
        entities.append(
            EgloRemoteInputSelect(
                unique_id=f"eglo_remote_{ieee_clean}_current_light",
                name=f"Eglo Remote {device.name} Current Light",
                options=["all"],
                initial="all",
                device=device,
            )
        )
    
    if entities:
        async_add_entities(entities)
        _LOGGER.info(f"Created {len(entities)} input_select entities for Eglo remotes")


class EgloRemoteInputSelect(InputSelect):
    """Input Select entity for Eglo Remote."""
    
    def __init__(
        self,
        unique_id: str,
        name: str,
        options: list[str],
        initial: str,
        device: dr.DeviceEntry,
    ) -> None:
        """Initialize the input select."""
        self._attr_unique_id = unique_id
        self._attr_name = name
        self._attr_options = options
        self._attr_current_option = initial
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
    
    async def async_select_option(self, option: str) -> None:
        """Select new option."""
        if option in self._attr_options:
            self._attr_current_option = option
            self.async_write_ha_state()
    
    async def async_set_options(self, options: list[str]) -> None:
        """Set options."""
        self._attr_options = options
        if self._attr_current_option not in options:
            self._attr_current_option = options[0] if options else None
        self.async_write_ha_state()
