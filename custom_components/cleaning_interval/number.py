from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.number import NumberEntity
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN, CONF_INTERVALS


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up number entities for cleaning intervals."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    for key in coordinator.intervals:
        entities.append(CleaningIntervalNumber(coordinator, entry, key))

    async_add_entities(entities)


class CleaningIntervalNumber(CoordinatorEntity, NumberEntity):
    """Number-Entity zum Anpassen von Wartungsintervallen (persistent)."""

    _attr_mode = "box"  # ← sorgt für Eingabefeld statt Slider

    def __init__(self, coordinator, entry, key):
        super().__init__(coordinator)
        self._key = key
        self._entry = entry

        self._attr_unique_id = f"{entry.entry_id}_{key}_interval"
        self._attr_name = f"{coordinator.entry.title} {key} Intervall"
        self._attr_min_value = 1
        self._attr_max_value = 500
        self._attr_step = 1

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
            manufacturer="Cleaning Interval",
            model="Cleaning Monitor",
        )

    @property
    def native_value(self):
        """Return current interval value."""
        return self.coordinator.intervals.get(self._key)

    async def async_set_native_value(self, value: float):
        """Handle value update from UI and persist it."""
        new_value = int(value)

        # 1️⃣ Coordinator aktualisieren
        self.coordinator.intervals[self._key] = new_value

        # 2️⃣ Bestehende Options kopieren
        options = dict(self._entry.options)
        intervals = dict(
            options.get(
                CONF_INTERVALS,
                self.coordinator.intervals,
            )
        )

        # 3️⃣ Neuen Wert setzen
        intervals[self._key] = new_value
        options[CONF_INTERVALS] = intervals

        # 4️⃣ Persistent speichern
        self.hass.config_entries.async_update_entry(
            self._entry,
            options=options,
        )

        # 5️⃣ UI + abhängige Sensoren aktualisieren
        self.async_write_ha_state()
        self.coordinator.async_set_updated_data(self.coordinator.counts)
