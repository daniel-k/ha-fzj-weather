"""Sensor platform for FZJ Weather integration."""

import logging
from datetime import timedelta

import requests
from bs4 import BeautifulSoup
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    # PRESSURE_HPA,
    # SPEED_METERS_PER_SECOND,
    # TEMP_CELSIUS,
    DEGREE,
    PERCENTAGE,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
)
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

_LOGGER = logging.getLogger(__name__)

FZJ_WEATHER_URL = (
    "https://www.fz-juelich.de/de/gs/ueber-uns/meteo/aktuelle-wetterdaten/wetterdaten"
)
SCAN_INTERVAL = timedelta(minutes=10)
SENSOR_TYPES = {
    "pressure_hpa": {
        "name": "Pressure",
        "unit": UnitOfPressure.MBAR,
        "icon": "mdi:gauge",
    },
    "temperature_c": {
        "name": "Temperature",
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:thermometer",
    },
    "humidity_percent": {
        "name": "Humidity",
        "unit": PERCENTAGE,
        "icon": "mdi:water-percent",
    },
    "wind_speed_ms": {
        "name": "Wind Speed",
        "unit": UnitOfSpeed.METERS_PER_SECOND,
        "icon": "mdi:weather-windy",
    },
    "wind_direction_deg": {
        "name": "Wind Direction",
        "unit": DEGREE,
        "icon": "mdi:compass",
    },
}


def fetch_weather_html(url: str = FZJ_WEATHER_URL) -> str:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.text


def parse_weather_metrics(html: str):
    """
    Parse HTML content returned from FZJ weather page.
    Returns a dict with current readings.
    """
    import re
    from datetime import datetime, timedelta, timezone

    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"bgcolor": "#f0f0f0"})

    mapping = {
        "Luftdruck": "pressure_hpa",
        "Lufttemperatur": "temperature_c",
        "relative Feuchte": "humidity_percent",
        "Windstärke": "wind_speed_ms",
        "Windrichtung": "wind_direction_deg",
    }

    # Default values
    metrics = {
        "pressure_hpa": None,
        "temperature_c": None,
        "humidity_percent": None,
        "wind_speed_ms": None,
        "wind_direction_deg": None,
    }

    if table is not None:
        for row in table.find_all("tr"):
            tds = row.find_all("td")
            if len(tds) != 2:
                continue
            key = tds[0].get_text(strip=True)
            val = tds[1].get_text(strip=True)
            for de, field in mapping.items():
                if key.startswith(de):
                    number = "".join(c for c in val if (c.isdigit() or c in ",.-"))
                    number = number.replace(",", ".")
                    try:
                        metrics[field] = float(number)
                    except ValueError:
                        metrics[field] = None

    ts_match = re.search(r"Aktuelle Messwerte vom ([^<]+)", html)
    ts_str = ts_match.group(1).strip() if ts_match else None

    timestamp = None
    if ts_str:
        tz_offsets = {
            "MEZ": timedelta(hours=1),  # UTC+1
            "MESZ": timedelta(hours=2),  # UTC+2
        }
        match = re.match(
            r"(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}) Uhr ?([A-ZÄÖÜ]{2,4})?", ts_str
        )
        if match:
            dt_part = match.group(1)
            tz_abbr = match.group(2)
            try:
                dt_naive = datetime.strptime(dt_part, "%d.%m.%Y %H:%M")
                if tz_abbr in tz_offsets:
                    tzinfo = timezone(tz_offsets[tz_abbr], name=tz_abbr)
                else:
                    tzinfo = None
                ts_aware = dt_naive.replace(tzinfo=tzinfo)
                timestamp = ts_aware.astimezone()
            except Exception:
                timestamp = None

    metrics["timestamp"] = timestamp
    return metrics


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up FZJ Weather sensor platform from YAML (legacy)."""
    return True  # Not supported; use config flow via UI.


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up FZJ Weather sensors from a config entry (via UI)."""
    # Only allow a single entry
    if hass.data.get("fzj_weather_loaded_entry") is not None:
        return False

    coordinator = FZJWeatherDataUpdateCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    sensors = [
        FZJWeatherSensor(coordinator, sensor_type)
        for sensor_type in SENSOR_TYPES.keys()
    ]
    async_add_entities(sensors, update_before_add=True)
    hass.data["fzj_weather_loaded_entry"] = entry.entry_id


async def async_setup(hass, config):
    """Set up the integration via configuration.yaml (legacy)."""
    # Not supported with config flow enabled.
    return True


class FZJWeatherDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage data fetching from FZJ weather site."""

    def __init__(self, hass):
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name="FZJ Weather data",
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self):
        """Fetch data from FZJ weather."""
        try:
            html = await self.hass.async_add_executor_job(fetch_weather_html)
            data = await self.hass.async_add_executor_job(parse_weather_metrics, html)
            return data
        except Exception as err:
            raise UpdateFailed(f"Error fetching/parsing data: {err}") from err


class FZJWeatherSensor(CoordinatorEntity, SensorEntity):
    """Representation of a FZJ Weather sensor."""

    def __init__(self, coordinator, sensor_type):
        """Initialize."""
        super().__init__(coordinator)
        self.sensor_type = sensor_type
        self._attr_unique_id = f"fzj_weather_{sensor_type}"
        self._attr_name = f"FZJ {SENSOR_TYPES[sensor_type]['name']}"
        self._attr_icon = SENSOR_TYPES[sensor_type]["icon"]
        self._attr_native_unit_of_measurement = SENSOR_TYPES[sensor_type]["unit"]
        self._attr_entity_category = (
            EntityCategory.DIAGNOSTIC if sensor_type == "timestamp" else None
        )

    @property
    def native_value(self):
        return self.coordinator.data.get(self.sensor_type)

    @property
    def available(self):
        return (
            self.coordinator.last_update_success and self.coordinator.data is not None
        )

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data or {}
        if "timestamp" in data and self.sensor_type != "timestamp":
            ts = data["timestamp"]
            return {"fzj_reading_time": str(ts) if ts else None}
        return {}
