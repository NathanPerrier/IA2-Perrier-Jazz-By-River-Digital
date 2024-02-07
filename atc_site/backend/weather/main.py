from .__init__ import *

from .dataPoints.__init__ import *

class RetrieveWeather():
    '''
    
    Example:
    
        self.model = RetrieveWeather(GetLocation().get_location().zip)
        summary = self.model.Summary(self.model.request).get_summary()
    
    Data points:
    
        Forecast:
        
            self.model.Forecast(self.model.request).get_rain() ||| returns a dict with the keys 'amount', 'chance', 'start_time', 'period'
            self.model.Forecast(self.model.request).get_daily() ||| returns multiple dicts (each representing a day) with the keys 'rain' ('amount' ('min', 'max', 'lower_range', 'upper_range', 'units'), 'chance', 'chance_of_no_rain_category', 'precipitation_amount_25_percent_chance', 'precipitation_amount_50_percent_chance', 'precipitation_amount_75_percent_chance'), 'uv', 'astronomical', 'astronomical', 'date', 'temp_max', 'temp_min', 'extended_text', 'icon_descriptor', 'short_text', 'surf_danger', 'fire_danger', 'fire_danger_category', 'now'
            self.model.Forecast(self.model.request).get_hourly() ||| returns multiple dicts (each representing an hour) with the keys 'rain' ('amount' ('min', 'max', 'units'), 'chance', 'precipitation_amount_10_percent_chance', 'precipitation_amount_25_percent_chance', 'precipitation_amount_50_percent_chance'), 'temp', 'temp_feels_like', 'wind', 'relative_humidity', 'uv', 'icon_descriptor', 'next_three_hourly_forecast_period', 'time', 'is_night', 'next_forecast_period'
            
        UvData:

            self.model.UvData(self.model.request).get_uv_message() ||| returns the uv message for the location
        
        Warnings:
        
            self.model.Warnings(self.model.request).get_warnings() ||| returns a dict with the keys 'id', 'state', 'expiry_time', 'issue_time', 'type', 'short_title', 'warning_group_type', 'phase'
            self.model.Warnings(self.model.request).get_title() ||| returns the title of the warning
            self.model.Warnings(self.model.request).get_warning_description() ||| returns the description of the warning
            self.model.Warnings(self.model.request).get_warning_id() ||| returns the id of the warning
            
        Summary:
        
            self.model.Summary(self.model.request).get_summary() ||| returns a dict with the keys 'Location', 'Current Temp', 'Precis', 'Max', 'Overnight Min', 'Feels Like', 'Chance of any Rain', 'Possible Rainfall'
            self.model.Summary(self.model.request).get_summary_text() ||| returns a string with the summary of the weather
            
        Observations:
        
            self.model.Observations(self.model.request).get_observations() ||| returns a dict with the keys 'temp', 'temp_feels_like', 'wind' ('speed_kilometre', 'speed_knot', 'direction'), 'rain_since_9am', 'humidity', 'station' ('bom_id', 'name', 'distance')
            self.model.Observations(self.model.request).get_predicted_air_temperature() ||| returns the air_temperature in degress celcius (e.g 30.2) 
            self.model.Observations(self.model.request).get_predicted_rainfall() ||| returns the rainfall in mm (e.g 0.2)
            
        Place:
        
            self.model.Place(self.model.request).get_forecast() ||| !! keys change, not always present !! returns a dict 'issued', 'date', 'max', 'min', 'precis'
            self.model.Place(self.model.request).get_air_temperature() ||| returns the air_temperature in degress celcius (e.g 30.2)
            self.model.Place(self.model.request).get_place() ||| returns the place as a dict with the keys 'name', 'state', 'timezone', 'geohash', 'latitude', 'longitude', 'marine_area_id', 'tidal_point', 'has_wave', 'id'
            self.model.Place(self.model.request).get_place_state() ||| returns the state of the place
            self.model.Place(self.model.request).get_place_name() ||| returns the name of the place
            self.model.Place(self.model.request).get_place_country() ||| returns the country of the place
            self.model.Place(self.model.request).get_place_timezone() ||| returns the timezone of the place
            
    '''
    
    def __init__(self, location):
        self.locationOrg = location

        self.zip = location
        
        self.request = api.WeatherApi(q=f'{self.locationOrg}', debug=1)
        
        self.location = self.request.location()

        print('location:', self.location)
        
    class Forecast(RetrieveForecast):
        def __init__(self, request):
            super().__init__(request)

        def get_rain(self):  
            return super().get_rain_data_fields()  

        def get_daily(self): 
            return super().get_daily_data_fields()  

        def get_hourly(self):
            return super().get_hourly_data_fields()
        
    class UvData(RetrieveUvIndex):
        def __init__(self, request):
            super().__init__(request)

        # def get_uv_descriptions(self):
        #     return super().get_uv_descriptions()

        def get_uv_message(self):
            return super().get_uv_message()
        
    class Warnings(RetrieveWarnings):
        def __init__(self, request):
            super().__init__(request)
            
        def get_warnings(self):
            return super().get_warnings()

        def get_title(self):
            return super().get_warning_title()
        
        def get_warning_description(self):
            return super().get_warning_description()
        
        def get_warning_id(self):
            return super().get_warning_id()
    
    class Summary(RetrieveSummary):
        def __init__(self, request):
            super().__init__(request)

        def get_summary(self):
            return super().get_summary()
        
        def get_summary_text(self):
            return super().get_summary_text()
        
    class Observations(RetrieveObservations):
        def __init__(self, request):
            super().__init__(request)
            
        def get_observations(self):
            return super().get_observations()

        def get_predicted_air_temperature(self):
            return super().get_predicted_air_temperature()
        
        def get_predicted_rainfall(self):
            return super().get_predicted_rainfall()
        
    class Place(RetrievePlace):
        def __init__(self, request):
            super().__init__(request)
            
        def get_forecast(self):
            return super().get_forecast()
        
        def get_air_temperature(self):
            return super().get_air_temperature()
            
        def get_place(self):
            return super().get_place()
    
        def get_place_state(self):
            return super().get_place_state()
        
        def get_place_name(self):
            return super().get_place_name()
        
        def get_place_country(self):
            return super().get_place_country()
        
        def get_place_timezone(self):
            return super().get_place_timezone()
        
    
    