"""Sunways Local integration."""

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from sunways.exceptions import InverterError

from .config_flow import async_connect_inverter
from .coordinator import SunwaysLocalCoordinator

PLATFORMS = [Platform.SENSOR]


@dataclass(slots=True)
class SunwaysLocalRuntimeData:
    coordinator: SunwaysLocalCoordinator


type SunwaysLocalConfigEntry = ConfigEntry[SunwaysLocalRuntimeData]


async def async_setup_entry(hass: HomeAssistant, entry: SunwaysLocalConfigEntry) -> bool:
    try:
        inverter = await async_connect_inverter(dict(entry.data))
    except (InverterError, TimeoutError, OSError, ValueError, TypeError) as err:
        raise ConfigEntryNotReady(f"Local Sunways inverter is not reachable: {err}") from err
    coordinator = SunwaysLocalCoordinator(hass, entry, inverter)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = SunwaysLocalRuntimeData(coordinator)
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: SunwaysLocalConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def _async_update_listener(hass: HomeAssistant, entry: SunwaysLocalConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)
