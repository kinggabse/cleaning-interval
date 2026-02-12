from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN, ICONS


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    for key in coordinator.counts:
        entities.append(CleaningStatusSensor(coordinator, key))

    async_add_entities(entities)


class CleaningStatusSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, key):
        super().__init__(coordinator)
        self.key = key
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{key}_status"
        self._attr_name = f"{coordinator.entry.title} {key} Status"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.entry.entry_id)},
            name=coordinator.entry.title,
            manufacturer="Custom",
            model="Cleaning Monitor",
        )

    @property
    def icon(self):
        if self.coordinator.counts[self.key] >= self.coordinator.intervals[self.key]:
            return ICONS[self.coordinator.device_type]["alert"]
        return ICONS[self.coordinator.device_type]["normal"]

    @property
    def native_value(self):
        count = self.coordinator.counts[self.key]
        interval = self.coordinator.intervals[self.key]

        remaining = interval - count
        if remaining <= 0:
            return "Maschinenpflege überfällig"

        return f"Maschinenpflege in {remaining} Gängen fällig"
