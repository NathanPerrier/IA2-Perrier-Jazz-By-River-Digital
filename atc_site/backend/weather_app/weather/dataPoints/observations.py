from ..__init__ import *

class RetrieveObservations():
    def __init__(self, request):
        self.request = request
        self.location = api.WeatherApi(q=api.WeatherApi().search(self.request.zip)[0]['name'].replace(' ', '%20')).location()
        self.model = observations.Observations(self.location)
        self.wmo_id = self.model.get_wmo_id(self.location)
        
        
    def get_observations(self):
        return self.request.api('observations')
        
    def get_predicted_air_temperature(self):
        return self.model.air_temperature(self.wmo_id)

    
    def get_predicted_rainfall(self):
        return self.model.rainfall(self.wmo_id)