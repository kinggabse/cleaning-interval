from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN, ICONS
from .coordinator import CleaningCoordinator


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: CleaningCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        CleaningResetButton(coordinator, key)
        for key in coordinator.counts.keys()
    ]
    async_add_entities(entities)


class CleaningResetButton(CoordinatorEntity, ButtonEntity):
    def __init__(self, coordinator: CleaningCoordinator, key: str):
        super().__init__(coordinator)
        self.key = key

        self._attr_unique_id = f"{coordinator.entry.entry_id}_{key}_reset"
        self._attr_name = key + " durchgeführt"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.entry.entry_id)},
            name=coordinator.entry.title,
            manufacturer="Cleaning Interval Monitor",
            model="Cleaning Monitor",
        )
        self._attr_icon = ICONS["reset"]

    async def async_press(self):
        await self.coordinator.async_reset(self.key)
