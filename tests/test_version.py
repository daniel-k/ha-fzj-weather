import ha_fzj_weather


def test_version_exists():
    assert hasattr(ha_fzj_weather, "__version__")
    assert isinstance(ha_fzj_weather.__version__, str)
    assert ha_fzj_weather.__version__ != ""
