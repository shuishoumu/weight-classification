"""Config flow for Weight Classification integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import selector
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_SOURCE_SENSOR,
    CONF_PERSONS,
    CONF_PERSON_NAME,
    CONF_MIN_WEIGHT,
    CONF_MAX_WEIGHT,
)

_LOGGER = logging.getLogger(__name__)


class WeightClassificationConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Weight Classification."""

    VERSION = 1

    def __init__(self):
        """Initialize the config flow."""
        self._source_sensor = None
        self._persons = []

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            self._source_sensor = user_input[CONF_SOURCE_SENSOR]
            return await self.async_step_persons()

        # Get all sensor entities
        entity_registry = async_get_entity_registry(self.hass)
        sensor_entities = [
            entry.entity_id
            for entry in entity_registry.entities.values()
            if entry.entity_id.startswith("sensor.")
        ]

        data_schema = vol.Schema(
            {
                vol.Required(CONF_SOURCE_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_persons(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Handle the persons configuration step."""
        errors = {}

        if user_input is not None:
            person_name = user_input[CONF_PERSON_NAME]
            min_weight = user_input[CONF_MIN_WEIGHT]
            max_weight = user_input[CONF_MAX_WEIGHT]

            # Validate weight range
            if min_weight >= max_weight:
                errors["base"] = "invalid_weight_range"
            else:
                # Add person to the list
                self._persons.append(
                    {
                        CONF_PERSON_NAME: person_name,
                        CONF_MIN_WEIGHT: min_weight,
                        CONF_MAX_WEIGHT: max_weight,
                    }
                )

                # Check if user wants to add more persons
                if user_input.get("add_another", False):
                    return await self.async_step_persons()

                # Create the config entry
                return self.async_create_entry(
                    title="Weight Classification",
                    data={
                        CONF_SOURCE_SENSOR: self._source_sensor,
                        CONF_PERSONS: self._persons,
                    },
                )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_PERSON_NAME): cv.string,
                vol.Required(CONF_MIN_WEIGHT, default=30): vol.All(
                    vol.Coerce(float), vol.Range(min=0, max=500)
                ),
                vol.Required(CONF_MAX_WEIGHT, default=100): vol.All(
                    vol.Coerce(float), vol.Range(min=0, max=500)
                ),
                vol.Optional("add_another", default=False): cv.boolean,
            }
        )

        description_placeholders = {
            "persons_count": str(len(self._persons)),
        }

        return self.async_show_form(
            step_id="persons",
            data_schema=data_schema,
            errors=errors,
            description_placeholders=description_placeholders,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Weight Classification."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Handle options step."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
        )
