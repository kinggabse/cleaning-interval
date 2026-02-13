from __future__ import annotations
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN, ICONS
from .coordinator import CleaningCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: CleaningCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []

    for key in coordinator.counts.keys():
        # Counter-Sensor
        entities.append(CleaningIntervalSensor(coordinator, entry, key))
        # Status-Text-Sensor
        entities.append(CleaningStatusSensor(coordinator, entry, key))

    async_add_entities(entities)


class CleaningIntervalSensor(CoordinatorEntity, SensorEntity):
    """Zähler-Sensor für Wartungszyklen"""

    _attr_has_entity_name = True

    def __init__(self, coordinator: CleaningCoordinator, entry: ConfigEntry, key: str):
        super().__init__(coordinator)
        self._key = key
        self._entry = entry

        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_native_unit_of_measurement = "cycles"
        self._attr_icon = "mdi:counter"
        self._attr_name = key

    @property
    def native_value(self):
        return self.coordinator.counts.get(self._key, 0)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": self._entry.title,
            "manufacturer": "Cleaning Interval Monitor",
        }


class CleaningStatusSensor(CoordinatorEntity, SensorEntity):
    """Text-Sensor für Status der Wartung"""

    def __init__(self, coordinator: CleaningCoordinator, entry: ConfigEntry, key: str):
        super().__init__(coordinator)
        self._key = key
        self._entry = entry

        self._attr_unique_id = f"{entry.entry_id}_{key}_status"
        self._attr_name = f"{key} Status"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name=self._entry.title,
            manufacturer="Cleaning Interval Monitor",
            model="Cleaning Monitor",
        )

    @property
    def icon(self):
        # Direkter Zugriff auf Coordinator.intervals
        if self.coordinator.counts.get(self._key, 0) >= self.coordinator.intervals.get(self._key, 0):
            return ICONS[self.coordinator.device_type]["alert"]
        return ICONS[self.coordinator.device_type]["normal"]

    @property
    def native_value(self):
        count = self.coordinator.counts.get(self._key, 0)
        interval = self.coordinator.intervals.get(self._key, 0)
        remaining = interval - count

        task_name = self._key  # Dynamisch aus Key

        if remaining <= 0:
            return f"{task_name} überfällig"
        return f"{task_name} in {remaining} Gängen fällig"
