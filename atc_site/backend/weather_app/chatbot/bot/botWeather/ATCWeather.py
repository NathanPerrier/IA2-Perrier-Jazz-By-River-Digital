from ....weather.main import RetrieveWeather
from .requestError import handle_errors
import json

class ATCWeather:
    def __init__(self):
        self.model = RetrieveWeather('indooroopilly')

    class Forecast():
        def __init__(self):
            self.model = ATCWeather().model.Forecast(ATCWeather().model.request)
            
        @handle_errors("Failed to get daily forecast")
        def get_daily_forecast(self):
            return json.dumps(self.model.get_daily())
        
        @handle_errors("Failed to get hourly forecast")
        def get_hourly_forecast(self):
            return json.dumps(self.model.get_hourly())
        
        @handle_errors("Failed to get current forecast")
        def get_current_forecast(self):
            return json.dumps(self.model.get_hourly()[0])
        
        @handle_errors("Failed to get rain forecast")
        def get_rain_forecast(self):
            return json.dumps(self.model.get_rain())
        
    class Warning():
        def __init__(self):
            self.model = ATCWeather().model.Warnings(ATCWeather().model.request)
           
        @handle_errors("Failed to get warnings") 
        def get_warnings(self):
            return json.dumps(self.model.get_warnings())
        
    class UVIndex():
        def __init__(self):
            self.model = ATCWeather().model.UvData(ATCWeather().model.request)
            
        @handle_errors("Failed to get UV messsage")
        def get_uv_index(self):
            return json.dumps(self.model.get_uv_message())
        
