import requests, json
from .requestError import handle_errors

class GetWeatherHistory:
    def __init__(self, location):
        self.location = location
        
    @handle_errors("Failed to get weather history")  
    def get_recent_weather_history(self, location, unit, timestep):
        print('location:', location)
        
        location = self.location if location is None else location
        
        url = f'https://api.tomorrow.io/v4/weather/history/recent?location={location}&timesteps={timestep}&units={unit}&apikey={config("TOMORROWIO_API_KEY")}'
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        
        if 'code' in json.loads(response.text):
            return json.loads(str(response.text['message']))
        
        return self.format_response_historical(json.loads(response.text), location, unit, timestep)
    
    
    def format_response_historical(self, json_data, location, unit, timestep):
        intervals = 'daily' if timestep == '1d' else 'hourly'
        tool_results = [
            {
                "name": "weather_data",
                "results": [
                    {
                        "location": location,  # Replace with the actual location
                        "unit": unit,  # Replace with the desired unit
                        "fields": list(json_data["timelines"][intervals][0]["values"].keys()),
                        "data": [
                            {
                                "timestamp": interval["time"],
                                **interval["values"],
                            }
                            for interval in json_data["timelines"][intervals]
                        ],
                    }
                ],
            }
        ]
        formatted_data = {"tool_results": tool_results}
        json_response = json.dumps(formatted_data, indent=2)
        
        print(json_response)
        
        return json_response