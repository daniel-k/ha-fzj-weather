"""FZJ Weather integration for Home Assistant."""

DOMAIN = "fzj_weather"

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up FZJ Weather from yaml (not used, needed for HA discovery)."""
    return True


from .sensor import FZJWeatherDataUpdateCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up FZJ Weather from a config entry (UI)."""
    # Create coordinator and do first refresh during SETUP_IN_PROGRESS
    coordinator = FZJWeatherDataUpdateCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True
