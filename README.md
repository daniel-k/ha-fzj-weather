# fzj-weather

A Python library for scraping weather data from FZJ

## Project Structure

fzj-weather/
│
├── pyproject.toml                 # Project metadata and packaging configuration
├── README.md                      # Project documentation (this file)
├── src/
│   └── fzj_weather/               # Library source code
│       ├── __init__.py
│       └── weather.py
└── tests/
    ├── __init__.py                # Test suite init
    ├── test_weather.py            # Tests for weather scraping
    └── data.html                  # Sample HTML fixture for tests

## Installation

This project uses [PEP 517/518](https://www.python.org/dev/peps/pep-0517/) packaging with [setuptools]. To install locally for development:

```bash
pip install --editable .
```

## Usage

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
