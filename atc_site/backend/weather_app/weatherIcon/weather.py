import requests
from requests import get
from decouple import config
import datetime
import pytz
import json

from ..location.main import GetLocation

class GetWeatherCode:
    def __init__(self):
        pass
    
    def get_time_of_day(self):
        try:
            ''' returns 'day' or 'night' '''
            locationData = GetLocation().get_location()
            timezone = pytz.timezone(locationData.timezone)
            print('time: ', datetime.datetime.now(timezone))
            current_time = datetime.datetime.now(timezone)
            if current_time.hour >= 6 and current_time.hour < 18:
                return 'day'
            return 'night'
        except: return 'day'
    
    def get_weather_code(self):
        try:
            ''' returns a weather code '''
            location = GetLocation().get_location()
            url = f'https://api.tomorrow.io/v4/timelines?apikey={config("TOMORROWIO_API_KEY")}'
            headers = {
                'Accept-Encoding': 'gzip',
                'accept': 'application/json',
                'content-type': 'application/json',
            }
            data = {
                "location": location.city,
                "fields": ['weatherCode'],
                "units": 'metric',
                "timesteps": ['current'],
                "timezone": location.timezone
            }

            response = requests.post(url, headers=headers, data=json.dumps(data)).json()
            return response['data']['timelines'][0]['intervals'][0]['values']['weatherCode']
        except: return '1000'
        