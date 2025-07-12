"""FZJ Weather integration for Home Assistant."""

DOMAIN = "fzj_weather"

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up FZJ Weather from yaml (not used, needed for HA discovery)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up FZJ Weather from a config entry (UI)."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    )
    return True
