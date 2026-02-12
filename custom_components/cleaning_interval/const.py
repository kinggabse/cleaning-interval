DOMAIN = "cleaning_interval"

CONF_DEVICE_TYPE = "Gerätetyp"
CONF_INTERVALS = "Intervalle"
CONF_SENSOR = "Status Sensor (in Betrieb/Außer Betrieb)"

DEVICE_DRYER = "Trockner"
DEVICE_DISHWASHER = "Geschirspüler"
DEVICE_WASHER = "Waschmaschine"

DEFAULT_INTERVALS = {
    DEVICE_DRYER: {"cleaning": 30},
    DEVICE_DISHWASHER: {"cleaning": 30},
    DEVICE_WASHER: {
        "drum": 40,
        "filter": 80,
    },
}

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
