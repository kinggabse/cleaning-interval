import logging

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.storage import Store
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.const import STATE_ON
from homeassistant.core import callback

from .const import (
    DOMAIN,
    CONF_DEVICE_TYPE,
    CONF_SENSOR,
    CONF_INTERVALS,
)

_LOGGER = logging.getLogger(__name__)


class CleaningCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        super().__init__(hass, _LOGGER, name=entry.title)

        self.hass = hass
        self.entry = entry

        self.device_type = entry.data.get(CONF_DEVICE_TYPE)
        self.sensor_entity_id = entry.data.get(CONF_SENSOR)

        # 🔥 WICHTIG: Kopie erzeugen
        self.intervals = dict(
            entry.options.get(CONF_INTERVALS)
            or entry.data[CONF_INTERVALS]
        )

        self.counts = {key: 0 for key in self.intervals}
        self.store = Store(hass, 1, f"{DOMAIN}_{entry.entry_id}")
        self._remove_listener = None

        # 🔥 Listener für Options-Änderungen
        entry.add_update_listener(self._handle_entry_update)

    async def _handle_entry_update(self, hass, entry):
        """Wird aufgerufen wenn options geändert werden."""
        _LOGGER.debug("ConfigEntry options updated")

        self.entry = entry
        self.intervals = dict(
            entry.options.get(CONF_INTERVALS)
            or entry.data[CONF_INTERVALS]
        )

        # Falls neue Keys hinzugefügt wurden
        for key in self.intervals:
            if key not in self.counts:
                self.counts[key] = 0

        self.async_set_updated_data(self.counts)

    async def async_load(self):
        data = await self.store.async_load()
        if data:
            self.counts.update(data.get("counts", {}))

        self.async_set_updated_data(self.counts)

    async def async_save(self):
        await self.store.async_save({"counts": self.counts})

    async def async_start_listening(self):
        self._remove_listener = async_track_state_change_event(
            self.hass,
            [self.sensor_entity_id],
            self._handle_cycle_event,
        )

    @callback
    def _handle_cycle_event(self, event):
        old_state = event.data.get("old_state")
        new_state = event.data.get("new_state")

        if not old_state or not new_state:
            return

        if old_state.state == STATE_ON and new_state.state != STATE_ON:
            self.hass.async_create_task(self.async_increment())

    async def async_increment(self):
        for key in self.counts:
            self.counts[key] += 1

        await self.async_save()
        self.async_set_updated_data(self.counts)

    async def async_reset(self, key):
        self.counts[key] = 0
        await self.async_save()
        self.async_set_updated_data(self.counts)

    async def _async_update_data(self):
        return self.counts
