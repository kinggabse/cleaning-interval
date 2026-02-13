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

            data = {
                CONF_DEVICE_TYPE: device_type,
                CONF_SENSOR: user_input[CONF_SENSOR],
                CONF_INTERVALS: DEFAULT_INTERVALS[device_type],
            }

            return self.async_create_entry(
                title=user_input["name"],
                data=data,
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

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        return CleaningIntervalOptionsFlow(config_entry)


class CleaningIntervalOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        device_type = self.config_entry.data[CONF_DEVICE_TYPE]
        current_intervals = self.config_entry.options.get(
            CONF_INTERVALS,
            self.config_entry.data[CONF_INTERVALS],
        )

        if user_input is not None:
            return self.async_create_entry(
                title="",
                data={CONF_INTERVALS: user_input},
            )

        if device_type == DEVICE_WASHER:
            schema = vol.Schema({
                vol.Required(
                    "drum",
                    default=current_intervals.get("drum", 40),
                ): vol.All(int, vol.Range(min=1, max=500)),
                vol.Required(
                    "filter",
                    default=current_intervals.get("filter", 60),
                ): vol.All(int, vol.Range(min=1, max=500)),
            })
        else:
            schema = vol.Schema({
                vol.Required(
                    "maintenance",
                    default=current_intervals.get("maintenance", 30),
                ): vol.All(int, vol.Range(min=1, max=500)),
            })

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
        )