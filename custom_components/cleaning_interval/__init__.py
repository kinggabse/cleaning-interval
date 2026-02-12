from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN
from .coordinator import CleaningCoordinator

PLATFORMS = ["sensor", "binary_sensor", "button"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    coordinator = CleaningCoordinator(hass, entry)
    await coordinator.async_load()
    await coordinator.async_start_listening()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
