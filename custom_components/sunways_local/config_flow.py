"""Config flow for Sunways Local."""

import asyncio
from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.helpers.selector import NumberSelector, NumberSelectorConfig, NumberSelectorMode
from sunways import connect
from sunways.exceptions import InverterError

from .const import (
    CONF_SCAN_INTERVAL,
    CONNECT_TIMEOUT,
    DEFAULT_PORT,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    MAX_SCAN_INTERVAL,
    MIN_SCAN_INTERVAL,
)


async def async_connect_inverter(data: dict[str, Any]):
    """Connect and identify one inverter."""
    async with asyncio.timeout(CONNECT_TIMEOUT * 4):
        return await connect(
            data[CONF_HOST],
            port=data.get(CONF_PORT, DEFAULT_PORT),
            timeout=CONNECT_TIMEOUT,
            retries=2,
        )


class SunwaysLocalConfigFlow(ConfigFlow, domain=DOMAIN):
    """Configure a local Sunways inverter."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                inverter = await async_connect_inverter(user_input)
                serial = inverter.serial_number
                await self.async_set_unique_id(serial or user_input[CONF_HOST])
                self._abort_if_unique_id_configured(updates={CONF_HOST: user_input[CONF_HOST]})
                title = " ".join(part for part in (inverter.model, serial) if part) or user_input[CONF_HOST]
                return self.async_create_entry(title=title, data=user_input)
            except (InverterError, TimeoutError, OSError, ValueError, TypeError):
                errors["base"] = "cannot_connect"
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Optional(CONF_PORT, default=DEFAULT_PORT): vol.All(
                        vol.Coerce(int), vol.Range(min=1, max=65535)
                    ),
                }
            ),
            errors=errors,
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        return SunwaysLocalOptionsFlow()


class SunwaysLocalOptionsFlow(OptionsFlow):
    """Configure polling without reconnecting the inverter."""

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        selector = NumberSelector(
            NumberSelectorConfig(
                min=MIN_SCAN_INTERVAL,
                max=MAX_SCAN_INTERVAL,
                step=5,
                mode=NumberSelectorMode.BOX,
                unit_of_measurement="s",
            )
        )
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SCAN_INTERVAL,
                        default=self.config_entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
                    ): selector
                }
            ),
        )
