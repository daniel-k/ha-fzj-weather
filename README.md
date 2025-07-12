# fzj-weather

A Python library for scraping weather data from FZJ

---

## Home Assistant Integration

You can use this as a Home Assistant custom integration, installable via HACS or directly.

### HACS Installation

1. Go to HACS > Integrations > Custom repositories.
2. Add the URL to this repository and set Category to "Integration".
3. Search for "FZJ Weather" and install it.
4. Restart Home Assistant.

### Manual Installation

1. Copy the entire `custom_components/fzj_weather` folder into your Home Assistant `/config/custom_components/` directory.
2. Restart Home Assistant.

### Configuration

No options are required. After installation and restart, Home Assistant should auto-discover sensors named like:
- `sensor.fzj_pressure`
- `sensor.fzj_temperature`
- `sensor.fzj_humidity`
- `sensor.fzj_wind_speed`
- `sensor.fzj_wind_direction`

All values are polled from the live FZJ site every 10 minutes.

---


## Project Structure

```
fzj-weather/
│
├── custom_components/
│   └── fzj_weather/          # Home Assistant custom integration code
│
├── pyproject.toml            # Project metadata and packaging configuration (library)
├── README.md                 # Project documentation (this file)
├── src/
│   └── fzj_weather/          # Library source code (standalone use)
├── hacs.json                 # HACS metadata
└── tests/
    └── __init__.py           # Test suite init
```

## Library Installation & Usage

If you just want the Python scraping library for local development:

```bash
pip install --editable .
```

### Python Usage

After installation, you can import the package in your Python code:

```python
from fzj_weather.weather import get_current_weather_metrics

weather = get_current_weather_metrics()
print(weather.as_dict())
```

The output from `as_dict()` will look like this:

```python
{
    "timestamp": datetime.datetime(2025, 7, 11, 22, 30, tzinfo=datetime.timezone(datetime.timedelta(seconds=7200), 'MESZ')),
    "pressure_hpa": 1006.4,
    "temperature_c": 16.3,
    "humidity_percent": 97.0,
    "wind_speed_ms": 0.2,
    "wind_direction_deg": 0.0
}
```

## Development

- Source code lives in the `src/fzj_weather/` directory.
- Tests go in the `tests/` directory, to be run with your preferred Python testing tool (e.g., pytest, unittest).
- Project metadata is stored in `pyproject.toml`.

### Dependencies

- Requires Python 3.9+ (for timezone support).
- Install dependencies:

```bash
pip install .
```

### Testing

You can write and run tests in the `tests/` directory, for example with `pytest`.

## License

This project is licensed under the MIT License.

## Author

Your Name - [@yourusername](https://github.com/yourusername)
