from homeassistant import config_entries
from homeassistant.helpers.selector import selector
import voluptuous as vol

from .const import (
    DOMAIN,
    CONF_DEVICE_TYPE,
    CONF_SENSOR,
    CONF_INTERVALS,
    DEVICE_DRYER,
    DEVICE_DISHWASHER,
    DEVICE_WASHER,
    DEFAULT_INTERVALS,
)


class CleaningIntervalConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            device_type = user_input[CONF_DEVICE_TYPE]

            return self.async_create_entry(
                title=user_input["name"],
                data={
                    CONF_DEVICE_TYPE: device_type,
                    CONF_SENSOR: user_input[CONF_SENSOR],
                    CONF_INTERVALS: DEFAULT_INTERVALS[device_type],
                },
            )

        schema = vol.Schema({
            vol.Required("name"): str,
            vol.Required(CONF_DEVICE_TYPE): selector({
                "select": {
                    "options": [
                        DEVICE_DRYER,
                        DEVICE_DISHWASHER,
                        DEVICE_WASHER,
                    ]
                }
            }),
            vol.Required(CONF_SENSOR): selector({
                "entity": {
                    "domain": "binary_sensor",
                    "device_class": "running",
                }
            }),
        })

        return self.async_show_form(step_id="user", data_schema=schema)

    @staticmethod
    def async_get_options_flow(config_entry):
        return CleaningIntervalOptionsFlow(config_entry)


class CleaningIntervalOptionsFlow(config_entries.OptionsFlow):
    """OptionsFlow für nachträgliche Anpassung der Wartungsintervalle"""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        device_type = self.config_entry.data[CONF_DEVICE_TYPE]
        current_intervals = self.config_entry.options.get(
            CONF_INTERVALS,
            self.config_entry.data[CONF_INTERVALS],
        )

        if user_input is not None:
            # Optionen nur speichern – Sensoren lesen automatisch die neuen Werte
            await self.config_entry.async_set_options({CONF_INTERVALS: user_input})
            return self.async_create_entry(title="", data=user_input)

        # Formular für UI
        if device_type == DEVICE_WASHER:
            schema = vol.Schema({
                vol.Required(
                    "Trommelreinigung",
                    default=current_intervals.get("Trommelreinigung", 40),
                ): vol.All(int, vol.Range(min=1, max=500)),
                vol.Required(
                    "Filterreinigung",
                    default=current_intervals.get("Filterreinigung", 60),
                ): vol.All(int, vol.Range(min=1, max=500)),
            })
        else:
            schema = vol.Schema({
                vol.Required(
                    "Maschinenpflege",
                    default=current_intervals.get("Maschinenpflege", 30),
                ): vol.All(int, vol.Range(min=1, max=500)),
            })

        return self.async_show_form(step_id="init", data_schema=schema)
