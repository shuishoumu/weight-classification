"""Constants for the Weight Classification integration."""

DOMAIN = "weight_classification"

# Configuration keys
CONF_SOURCE_SENSOR = "source_sensor"
CONF_PERSONS = "persons"
CONF_PERSON_NAME = "name"
CONF_MIN_WEIGHT = "min_weight"
CONF_MAX_WEIGHT = "max_weight"

# Defaults
DEFAULT_NAME = "Weight Classification"

# Attributes
ATTR_PERSON_NAME = "person_name"
ATTR_WEIGHT_RANGE = "weight_range"
ATTR_LAST_MEASURED = "last_measured"
ATTR_MIN_WEIGHT = "min_weight"
ATTR_MAX_WEIGHT = "max_weight"

# Entity naming
ENTITY_ID_FORMAT = "sensor.weight_{}"
