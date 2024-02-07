import urllib.request, json
from decouple import config

from ...models import Route
from ....weather.main import RetrieveWeather
from ....location.main import GetLocation
from ..get_zip import PostcodeDatabase
from .__init__ import *
from .requestError import handle_errors

class GetWeatherOnRoute:
    def __init__(self):    
        self.route = None
        self.routeStart = None
        self.routeEnd = None
        self.routeMode = None
        
        self.coord_list = []
        
        self.weatherData = ROUTE_LIST
        
        self.warning_list = self.weatherData[0]['results'][0]['warnings']
        self.rain_forecast_list = self.weatherData[0]['results'][0]['rain_forecast']
        
        
    def does_route_exist(self):
        ip = GetLocation().get_ip_address()
        if Route.objects.filter(ip=Route.hash_ip(ip)).exists():
            route = Route.objects.filter(ip=Route.hash_ip(ip)).last()
            self.route = route.route
            self.routeStart = route.start
            self.routeEnd = route.end
            self.routeMode = route.mode
            return True
        return False
    
    @handle_errors(None)
    def get_route(self):
        url = f'https://api.mapbox.com/directions/v5/mapbox/{ self.routeMode }/{ str(self.routeStart[0]) }%2C{ str(self.routeStart[1]) }%3B{ str(self.routeEnd[0]) }%2C{ str(self.routeEnd[1]) }?alternatives=false&geometries=geojson&language=en&overview=simplified&steps=false&notifications=none&access_token={config("MAPBOX_ACCESS_TOKEN")}'
        with urllib.request.urlopen(url) as url:
            data = json.load(url)
        return list(data['routes'][0]['geometry']['coordinates'])
        
    @handle_errors("Failed to get weather on route")
    def get_weather_on_route(self, startLocation, endLocation, mode):
        if startLocation is None:
            startLocation = (lambda location: [location.lat, location.lon])(GetLocation().get_location())
        if not self.does_route_exist():
            self.routeStart = str(startLocation).replace(' ', '+')
            self.routeEnd = str(endLocation).replace(' ', '+')
            self.routeMode = mode
            self.route = self.get_route()[0]
        
        for coordinate in self.route.strip('[]],').split('],'):
            coordinates = coordinate.strip(' [')
            self.coord_list.append(list([float(cord.strip("'")) for cord in coordinates.split(', ')]))
            
        for coordinates in self.coord_list: 
            
            forecast_rain, warning = self.get_weather_data(PostcodeDatabase(coordinates[1], coordinates[0]))
            
            if warning and warning[0] not in self.warning_list:
                self.warning_list.append(warning[0])
            if forecast_rain:
                self.rain_forecast_list.append({'lat': coordinates[1], 'lon': coordinates[0], 'amount': forecast_rain['amount'], 'chance': forecast_rain['chance']})
        return json.dumps(self.weatherData)
    
    def get_weather_data(self, postcode):
        model = RetrieveWeather(postcode.get_postcode())
        
        return model.Forecast(model.request).get_rain(), model.Warnings(model.request).get_warnings()