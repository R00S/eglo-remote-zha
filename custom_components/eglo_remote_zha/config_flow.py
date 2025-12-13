"""Config flow for Eglo Remote ZHA integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

_LOGGER = logging.getLogger(__name__)

DOMAIN = "eglo_remote_zha"


class EgloRemoteZHAConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Eglo Remote ZHA."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        # Only allow a single instance
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(
                title="Eglo Remote ZHA",
                data={},
            )

        return self.async_show_form(step_id="user")

    async def async_step_import(self, import_data: dict[str, Any]) -> FlowResult:
        """Handle import from configuration.yaml."""
        return await self.async_step_user(user_input={})
