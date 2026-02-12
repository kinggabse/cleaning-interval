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
                        {
                            "value": DEVICE_DRYER,
                            "label": "Dryer",
                        },
                        {
                            "value": DEVICE_DISHWASHER,
                            "label": "Dishwasher",
                        },
                        {
                            "value": DEVICE_WASHER,
                            "label": "Washer",
                        },
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
