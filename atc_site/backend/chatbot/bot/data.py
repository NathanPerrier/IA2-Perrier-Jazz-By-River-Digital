import requests
from decouple import config
from django.db import models
import json

from ...location.main import GetLocation
from .botWeather.route import GetWeatherOnRoute
from .botWeather.forecast import GetWeatherForecast
from .botWeather.history import GetWeatherHistory
from .botWeather.ATCWeather import ATCWeather

class BotData(models.Model):

    def get_city_from_ip(self):
        try:
            return GetLocation().get_location().city
        except Exception as e:
            print('error:', e)
            return None
    
    class WeatherRoute(GetWeatherOnRoute):
        def __init__(self):
            super().__init__()
        
        def get_weather_on_route(self, startLocation=None, endLocation=None, mode='driving'):
            return super().get_weather_on_route(startLocation, endLocation, mode)
            
        def does_route_exist(self):
            return super().does_route_exist()

    class WeatherForecast(GetWeatherForecast):
        def __init__(self):
            super().__init__(BotData().get_city_from_ip())
            
        def get_current_forecast(self, fields, location=None, unit="metric"):
            return super().get_current_weather(fields, location, unit)
            
        def get_hourly_forecast(self, fields, location=None, unit="metric"):
            return super().get_hourly_weather_forecast(fields, location, unit)
            
        def get_daily_forecast(self, fields, location=None, unit="metric"):
            return super().get_daily_weather_forecast(fields, location, unit)
        
    class WeatherHistory(GetWeatherHistory):
        def __init__(self):
            super().__init__(BotData().get_city_from_ip())
            
        def get_weather_history(self, location=None, unit="metric", timestep='1d'):
            return super().get_recent_weather_history(location, unit, timestep)
        
    ATCWeather = ATCWeather()