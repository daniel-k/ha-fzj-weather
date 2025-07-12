from fzj_weather.weather import get_current_weather_metrics

weather = get_current_weather_metrics()
print(weather.as_dict())
