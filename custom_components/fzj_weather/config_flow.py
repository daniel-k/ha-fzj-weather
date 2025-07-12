"""Config flow for FZJ Weather integration."""

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from . import DOMAIN


class FZJWeatherConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for FZJ Weather."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Only allow one instance.
            await self.async_set_unique_id(DOMAIN)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title="FZJ Weather (Jülich)", data={})

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
            description_placeholders={},
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return FZJWeatherOptionsFlowHandler(config_entry)


class FZJWeatherOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for FZJ Weather."""

    def __init__(self, config_entry):
        """Initialize FZJ Weather options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage FZJ Weather options (currently none)."""
        return self.async_create_entry(title="title", data={})
