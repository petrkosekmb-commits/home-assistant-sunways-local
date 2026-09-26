"""Local polling coordinator."""

import asyncio
import logging
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from sunways.exceptions import InverterError

from .const import CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
from .quality import normalize_runtime

_LOGGER = logging.getLogger(__name__)


class SunwaysLocalCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Read runtime values in one coordinated request."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, inverter) -> None:
        super().__init__(
            hass,
            logger=_LOGGER,
            config_entry=entry,
            name=f"Sunways Local {entry.title}",
            update_interval=timedelta(seconds=entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)),
        )
        self.inverter = inverter
        self.sensor_definitions = tuple(inverter.sensors())
        self.sensor_by_id = {sensor.id_: sensor for sensor in self.sensor_definitions}

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            async with asyncio.timeout(15):
                raw = await self.inverter.read_runtime_data()
        except (InverterError, TimeoutError, OSError, ValueError, TypeError) as err:
            raise UpdateFailed(f"Sunways inverter unavailable or returned invalid data: {err}") from err
        return normalize_runtime(raw, set(self.sensor_by_id))
