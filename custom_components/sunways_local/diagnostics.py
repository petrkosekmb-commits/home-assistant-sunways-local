"""Diagnostics for Sunways Local."""

from homeassistant.components.diagnostics import async_redact_data

TO_REDACT = {"host", "serial_number"}


async def async_get_config_entry_diagnostics(hass, entry):
    coordinator = entry.runtime_data.coordinator
    inverter = coordinator.inverter
    return {
        "config_entry": async_redact_data(dict(entry.data), TO_REDACT),
        "device": async_redact_data({
            "model": inverter.model,
            "serial_number": inverter.serial_number,
            "category": str(inverter.category),
            "master_firmware": inverter.master_firmware_version,
            "slave_firmware": inverter.slave_firmware_version,
        }, TO_REDACT),
        "available_sensor_ids": sorted(coordinator.data),
        "last_update_success": coordinator.last_update_success,
        "read_only": True,
    }
