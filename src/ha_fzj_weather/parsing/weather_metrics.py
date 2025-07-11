import re
from typing import Any, Dict, Optional

import requests
from bs4 import BeautifulSoup

FZJ_WEATHER_URL = (
    "https://www.fz-juelich.de/de/gs/ueber-uns/meteo/aktuelle-wetterdaten/wetterdaten"
)


class WeatherMetrics:
    """
    Data class to hold the parsed weather metrics.
    """

    def __init__(
        self,
        timestamp: Optional[str],
        pressure_hpa: Optional[float],
        temperature_c: Optional[float],
        humidity_percent: Optional[float],
        wind_speed_ms: Optional[float],
        wind_direction_deg: Optional[float],
    ):
        self.timestamp = timestamp
        self.pressure_hpa = pressure_hpa
        self.temperature_c = temperature_c
        self.humidity_percent = humidity_percent
        self.wind_speed_ms = wind_speed_ms
        self.wind_direction_deg = wind_direction_deg

    def as_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "pressure_hpa": self.pressure_hpa,
            "temperature_c": self.temperature_c,
            "humidity_percent": self.humidity_percent,
            "wind_speed_ms": self.wind_speed_ms,
            "wind_direction_deg": self.wind_direction_deg,
        }


def fetch_weather_html(url: str = FZJ_WEATHER_URL) -> str:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.text


def parse_weather_metrics(html: str) -> WeatherMetrics:
    """
    Parse HTML content returned from FZJ weather page.
    Returns a WeatherMetrics instance with current readings.
    """
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
                    # Extract just the number part (handles comma/point)
                    number = "".join(c for c in val if (c.isdigit() or c in ",.-"))
                    # Fix comma decimal for European numbers
                    number = number.replace(",", ".")
                    try:
                        metrics[field] = float(number)
                    except ValueError:
                        metrics[field] = None

    ts_match = re.search(r"Aktuelle Messwerte vom ([^<]+)", html)
    timestamp = ts_match.group(1).strip() if ts_match else None

    return WeatherMetrics(
        timestamp=timestamp,
        pressure_hpa=metrics["pressure_hpa"],
        temperature_c=metrics["temperature_c"],
        humidity_percent=metrics["humidity_percent"],
        wind_speed_ms=metrics["wind_speed_ms"],
        wind_direction_deg=metrics["wind_direction_deg"],
    )


def get_current_weather_metrics() -> WeatherMetrics:
    html = fetch_weather_html()
    return parse_weather_metrics(html)
