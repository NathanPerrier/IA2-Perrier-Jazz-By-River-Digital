from ..__init__ import *

class RetrievePlace():
    def __init__(self, request):
        self.request = request
        self.location = api.WeatherApi(q=api.WeatherApi().search(self.request.zip)[0]['name'].replace(' ', '%20')).location()
        self.model = place.Place(self.location['state'].lower(), self.location['name'].replace(' ', '-').lower())
        self.station_id = self.model.station_id()
        
    def get_forecast(self):
        return self.model.forecast()
    
    def get_air_temperature(self):
        return self.model.air_temperature()
    
    # Location info
    
    def get_place(self):
        return self.location
    
    def get_place_state(self):
        return self.location['state']
    
    def get_place_name(self):
        return self.location['name']
    
    def get_place_country(self):
        return self.get_place_timezone().split('/')
    
    def get_place_timezone(self):
        return self.location['timezone']

    