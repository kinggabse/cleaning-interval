from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN, ICONS
from .coordinator import CleaningCoordinator


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: CleaningCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        CleaningProblemSensor(coordinator, key)
        for key in coordinator.counts.keys()
    ]
    async_add_entities(entities)


class CleaningProblemSensor(CoordinatorEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.PROBLEM

    def __init__(self, coordinator: CleaningCoordinator, key: str):
        super().__init__(coordinator)
        self.key = key

        self._attr_unique_id = f"{coordinator.entry.entry_id}_{key}_problem"
        self._attr_name =  f"{coordinator.entry.title} {key} überfällig"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.entry.entry_id)},
            name=coordinator.entry.title,
            manufacturer="Cleaning Interval Monitor",
            model="Cleaning Monitor",
        )

    @property
    def icon(self):
        if self.is_on:
            return ICONS[self.coordinator.device_type]["alert"]
        return ICONS[self.coordinator.device_type]["normal"]

    @property
    def is_on(self):
        return self.coordinator.counts.get(self.key, 0) >= self.coordinator.intervals.get(self.key, 0)
