import pathlib

import pytest

from fzj_weather.weather import get_current_weather_metrics


@pytest.fixture
def data_html():
    return pathlib.Path(__file__).parent.joinpath("data.html").read_text()


def test_get_current_weather_metrics(monkeypatch, data_html):
    monkeypatch.setattr("fzj_weather.weather.fetch_weather_html", lambda: data_html)
    metrics = get_current_weather_metrics()
    assert metrics.as_dict() == {
        "humidity_percent": 97.0,
        "pressure_hpa": 1006.4,
        "temperature_c": 16.1,
        "timestamp": "11.07.2025 22:20 Uhr MEZ",
        "wind_direction_deg": 345.0,
        "wind_speed_ms": 0.1,
    }
