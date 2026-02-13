DOMAIN = "cleaning_interval"


CONF_DEVICE_TYPE = "device_type"
CONF_INTERVALS = "intervals"
CONF_SENSOR = "cycle_sensor"

DEVICE_DRYER = "Trockner"
DEVICE_DISHWASHER = "Geschirrspüler"
DEVICE_WASHER = "Waschmaschine"

DEFAULT_INTERVALS = {
    DEVICE_DRYER: {"Maschinenpflege": 15},
    DEVICE_DISHWASHER: {"Maschinenpflege": 30},
    DEVICE_WASHER: {
        "Trommelreinigung": 40,
        "Filterreinigung": 60,
    },
}

MANUFACTURER = "Cleaning Interval"
MODEL = "Cleaning Monitor"

ICONS = {
    DEVICE_WASHER: {
        "normal": "mdi:washing-machine",
        "alert": "mdi:washing-machine-alert",
    },
    DEVICE_DRYER: {
        "normal": "mdi:tumble-dryer",
        "alert": "mdi:tumble-dryer-alert",
    },
    DEVICE_DISHWASHER: {
        "normal": "mdi:dishwasher",
        "alert": "mdi:dishwasher-alert",
    },
    "reset": "mdi:refresh",
}
