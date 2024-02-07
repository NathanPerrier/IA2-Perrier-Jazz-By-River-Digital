import requests, json
from decouple import config
from .requestError import handle_errors

class GetWeatherForecast:
    def __init__(self, location):
        self.location = location
    
    @handle_errors("Failed to get current forecast")
    def get_current_weather(self, fields, location, unit): 
            
        print('current')
        print(list(fields.keys()))
        
        location = self.location if location is None else location
        
        timestep = '1d' if 'sunsetTime' or 'sunriseTime' in fields else 'current'
        
            
        url = f'https://api.tomorrow.io/v4/timelines?apikey={config("TOMORROWIO_API_KEY")}'
        headers = {
            'Accept-Encoding': 'gzip',
            'accept': 'application/json',
            'content-type': 'application/json',
        }
        data = {
            "location": location,
            "fields": list(fields.keys()),
            "units": unit,
            "timesteps": [
                timestep
            ],
            "timezone": 'auto'
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.text

    @handle_errors("Failed to get hourly forecast")
    def get_hourly_weather_forecast(self, fields, location, unit):
    
        print('location', location)
        print(list(fields.keys()))
        
        url = f'https://api.tomorrow.io/v4/timelines?apikey={config("TOMORROWIO_API_KEY")}'
        headers = {
            'Accept-Encoding': 'gzip',
            'accept': 'application/json',
            'content-type': 'application/json',
        }
        data = {
            "location": location,
            "fields": list(fields.keys()),
            "units": unit,
            "timesteps": [
                '1h'
            ],
            "timezone": "auto"
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        return self.format_response_forecast(json.loads(response.text), location, unit)


    @handle_errors("Failed to get daily forecast")  
    def get_daily_weather_forecast(self, fields, location, unit):
    
        print('daily')
        print(list(fields.keys()))
        print('location:', location)
        
        location = self.location if location is None else location
        
        url = f'https://api.tomorrow.io/v4/timelines?apikey={config("TOMORROWIO_API_KEY")}'
        headers = {
            'Accept-Encoding': 'gzip',
            'accept': 'application/json',
            'content-type': 'application/json',
        }
        data = {
            "location": location,
            "fields": list(fields.keys()),
            "units": unit,
            "timesteps": [
                '1d'
            ],
            "timezone": "auto"
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        return self.format_response_forecast(json.loads(response.text), location, unit)


    
    def format_response_forecast(self, json_data, location, unit):
        tool_results = [
            {
                "name": "weather_data",
                "results": [
                    {
                        "location": location,  
                        "unit": unit,
                        "fields": list(json_data["data"]["timelines"][0]["intervals"][0]["values"].keys()),
                        "data": [
                            {
                                "timestamp": interval["startTime"],
                                **interval["values"],
                            }
                            for interval in json_data["data"]["timelines"][0]["intervals"]
                        ],
                    }
                ],
            }
        ]
        formatted_data = {"tool_results": tool_results}
        json_response = json.dumps(formatted_data, indent=2)
        
        print(json_response)
        
        return json_response