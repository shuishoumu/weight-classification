"""Sensor platform for Weight Classification integration."""
from __future__ import annotations

from datetime import datetime
import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfMass
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.restore_state import RestoreEntity

from .const import (
    DOMAIN,
    CONF_SOURCE_SENSOR,
    CONF_PERSONS,
    CONF_PERSON_NAME,
    CONF_MIN_WEIGHT,
    CONF_MAX_WEIGHT,
    ATTR_PERSON_NAME,
    ATTR_WEIGHT_RANGE,
    ATTR_LAST_MEASURED,
    ATTR_MIN_WEIGHT,
    ATTR_MAX_WEIGHT,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Weight Classification sensors based on a config entry."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    source_sensor = config[CONF_SOURCE_SENSOR]
    persons = config[CONF_PERSONS]

    # Create a sensor for each person
    sensors = []
    for person in persons:
        sensors.append(
            WeightClassificationSensor(
                hass,
                source_sensor,
                person[CONF_PERSON_NAME],
                person[CONF_MIN_WEIGHT],
                person[CONF_MAX_WEIGHT],
            )
        )

    async_add_entities(sensors, True)


class WeightClassificationSensor(RestoreEntity, SensorEntity):
    """Representation of a Weight Classification Sensor."""

    _attr_device_class = SensorDeviceClass.WEIGHT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfMass.KILOGRAMS
    _attr_should_poll = False

    def __init__(
        self,
        hass: HomeAssistant,
        source_sensor: str,
        person_name: str,
        min_weight: float,
        max_weight: float,
    ) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self._source_sensor = source_sensor
        self._person_name = person_name
        self._min_weight = min_weight
        self._max_weight = max_weight
        self._attr_name = f"Weight {person_name}"
        self._attr_unique_id = f"weight_classification_{person_name.lower().replace(' ', '_')}"
        self._attr_native_value = None
        self._last_measured = None
        self._remove_listener = None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        attributes = {
            ATTR_PERSON_NAME: self._person_name,
            ATTR_MIN_WEIGHT: self._min_weight,
            ATTR_MAX_WEIGHT: self._max_weight,
            ATTR_WEIGHT_RANGE: f"{self._min_weight}-{self._max_weight} kg",
        }
        
        if self._last_measured:
            attributes[ATTR_LAST_MEASURED] = self._last_measured
            
        return attributes

    async def async_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        await super().async_added_to_hass()
        
        # Restore previous state
        if (last_state := await self.async_get_last_state()) is not None:
            if last_state.state not in ("unknown", "unavailable"):
                try:
                    self._attr_native_value = float(last_state.state)
                except ValueError:
                    _LOGGER.warning(
                        "Could not restore state for %s: %s",
                        self.entity_id,
                        last_state.state,
                    )
            
            if ATTR_LAST_MEASURED in last_state.attributes:
                self._last_measured = last_state.attributes[ATTR_LAST_MEASURED]

        # Listen to source sensor state changes
        self._remove_listener = async_track_state_change_event(
            self.hass, [self._source_sensor], self._async_sensor_changed
        )

    async def async_will_remove_from_hass(self) -> None:
        """Handle entity removal."""
        if self._remove_listener:
            self._remove_listener()

    @callback
    def _async_sensor_changed(self, event) -> None:
        """Handle source sensor state changes."""
        new_state = event.data.get("new_state")
        
        if new_state is None or new_state.state in ("unknown", "unavailable"):
            return

        try:
            weight = float(new_state.state)
        except (ValueError, TypeError):
            _LOGGER.warning(
                "Could not convert state %s to float for %s",
                new_state.state,
                self._source_sensor,
            )
            return

        # Check if weight is within this person's range
        if self._min_weight <= weight <= self._max_weight:
            _LOGGER.info(
                "Weight %.2f kg matched person %s (range: %.1f-%.1f kg)",
                weight,
                self._person_name,
                self._min_weight,
                self._max_weight,
            )
            self._attr_native_value = weight
            self._last_measured = datetime.now().isoformat()
            self.async_write_ha_state()
