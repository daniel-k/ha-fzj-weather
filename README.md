# ha-fzj-weather

A Python library for FZJ weather integration with Home Assistant.

## Project Structure

```
ha-fzj-weather/
│
├── pyproject.toml           # Project metadata and packaging configuration
├── README.md                # Project documentation (this file)
├── src/
│   └── ha_fzj_weather/      # Library source code
│       └── __init__.py
└── tests/
    └── __init__.py          # Test suite init
```

## Installation

This project uses [PEP 517/518](https://www.python.org/dev/peps/pep-0517/) packaging with [setuptools]. To install locally for development:

```bash
pip install --editable .
```

## Usage

After installation, you can import the package in your Python code:

```python
import ha_fzj_weather
print(ha_fzj_weather.__version__)
```

## Development

- Source code lives in the `src/ha_fzj_weather/` directory.
- Tests go in the `tests/` directory, to be run with your preferred Python testing tool (e.g., pytest, unittest).
- Project metadata is stored in `pyproject.toml`.

## License

This project is licensed under the MIT License.

## Author

Your Name - [@yourusername](https://github.com/yourusername)

---
*Replace "Your Name" and URLs with your actual information as appropriate.*