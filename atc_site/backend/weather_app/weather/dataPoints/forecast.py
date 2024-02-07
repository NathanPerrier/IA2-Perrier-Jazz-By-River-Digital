from ..__init__ import *

class RetrieveForecast():
    def __init__(self, request):
        self.request = request
        
    def get_rain_data_fields(self):
        return self.request.api('forecast/rain') #? rain??  is there a current one?

    def get_daily_data_fields(self):
        return self.request.api('forecasts/daily')

    def get_hourly_data_fields(self):
        return self.request.api('forecasts/hourly')