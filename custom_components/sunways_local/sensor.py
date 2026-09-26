"""Dynamic local Sunways sensors."""

from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfTemperature,
)
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import SunwaysLocalConfigEntry
from .const import DOMAIN, MANUFACTURER
from .coordinator import SunwaysLocalCoordinator

UNIT_MAP = {
    "%": PERCENTAGE,
    "A": UnitOfElectricCurrent.AMPERE,
    "V": UnitOfElectricPotential.VOLT,
    "W": UnitOfPower.WATT,
    "kW": UnitOfPower.KILO_WATT,
    "Hz": UnitOfFrequency.HERTZ,
    "kWh": UnitOfEnergy.KILO_WATT_HOUR,
    "C": UnitOfTemperature.CELSIUS,
    "°C": UnitOfTemperature.CELSIUS,
}
DEVICE_CLASS_MAP = {
    "A": SensorDeviceClass.CURRENT,
    "V": SensorDeviceClass.VOLTAGE,
    "W": SensorDeviceClass.POWER,
    "kW": SensorDeviceClass.POWER,
    "Hz": SensorDeviceClass.FREQUENCY,
    "kWh": SensorDeviceClass.ENERGY,
    "C": SensorDeviceClass.TEMPERATURE,
    "°C": SensorDeviceClass.TEMPERATURE,
}
CORE_ENABLED = {
    "timestamp",
    "work_status",
    "ppv",
    "pac",
    "pload",
    "pmeter",
    "battery_soc",
    "battery_soh",
    "e_day",
    "e_total",
    "temperature",
}


async def async_setup_entry(hass: Any, entry: SunwaysLocalConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        SunwaysLocalSensor(coordinator, entry, definition) for definition in coordinator.sensor_definitions
    )


class SunwaysLocalSensor(CoordinatorEntity[SunwaysLocalCoordinator], SensorEntity):
    """One runtime value described by the upstream library."""

    _attr_has_entity_name = True

    def __init__(self, coordinator, entry, definition) -> None:
        super().__init__(coordinator, context=definition.id_)
        self._definition = definition
        self._attr_name = definition.name
        serial = coordinator.inverter.serial_number or entry.data["host"]
        self._attr_unique_id = f"{serial}_{definition.id_}"
        self._attr_native_unit_of_measurement = UNIT_MAP.get(definition.unit)
        self._attr_device_class = DEVICE_CLASS_MAP.get(definition.unit)
        if definition.id_ == "timestamp":
            self._attr_device_class = SensorDeviceClass.TIMESTAMP
        elif definition.unit == "kWh":
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        elif self._attr_native_unit_of_measurement:
            self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_entity_registry_enabled_default = definition.id_ in CORE_ENABLED
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, serial)},
            manufacturer=MANUFACTURER,
            name=entry.title,
            model=coordinator.inverter.model,
            serial_number=coordinator.inverter.serial_number,
            sw_version=" / ".join(
                value
                for value in (
                    coordinator.inverter.master_firmware_version,
                    coordinator.inverter.slave_firmware_version,
                )
                if value
            )
            or None,
        )

    @property
    def native_value(self) -> Any:
        return self.coordinator.data.get(self._definition.id_)
