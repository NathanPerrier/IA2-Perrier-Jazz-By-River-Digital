import json
from tenacity import retry, wait_random_exponential, stop_after_attempt
import requests

from .__init__ import *
from .data import BotData

class Chatbot:
    def __init__(self, model_type=GPT_MODEL):
        self.model = model_type
        
    #*@retry(wait=wait_random_exponential(multiplier=1, max=60), stop=stop_after_attempt(3))
    def chat_completion_request(self, messages):
        print('model:', self.model)
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=TOOLS,
            # temperature=0.01,
            tool_choice="auto",  
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        
        if tool_calls:
            available_functions = {
                "get_current_weather": (lambda botData: botData.WeatherForecast().get_current_forecast)(BotData()),
                "get_daily_weather_forecast": (lambda botData: botData.WeatherForecast().get_daily_forecast)(BotData()),
                "get_hourly_weather_forecast": (lambda botData: botData.WeatherForecast().get_hourly_forecast)(BotData()),
                'get_recent_weather_history': (lambda botData: botData.WeatherHistory().get_weather_history)(BotData()),
                "get_weather_on_route": (lambda botData: botData.WeatherRoute().get_weather_on_route)(BotData()),
                "does_route_exist": (lambda botData: botData.WeatherRoute().does_route_exist)(BotData()),
                
                "atc_current_weather": (lambda botData: botData.ATCWeather.Forecast().get_current_forecast)(BotData()),
                "atc_hourly_weather": (lambda botData: botData.ATCWeather.Forecast().get_hourly_forecast)(BotData()),
                "atc_daily_weather": (lambda botData: botData.ATCWeather.Forecast().get_daily_forecast)(BotData()),
                "atc_rain_weather": (lambda botData: botData.ATCWeather.Forecast().get_rain_forecast)(BotData()),
                "atc_uv_message": (lambda botData: botData.ATCWeather.UVIndex().get_uv_index)(BotData()),
                "atc_weather_warning": (lambda botData: botData.ATCWeather.Warning().get_warnings)(BotData())
            }  
            
            messages.append(response_message)  # extend conversation with assistant's reply
            # Step 4: send the info for each function call and function response to the model
            
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                print('function name:', function_name)
                
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                
                if function_name == 'get_recent_weather_history':
                    function_response = function_to_call(
                        location=function_args.get("location"),
                        unit=function_args.get("unit", "metric"),
                        timestep=function_args.get("timestep"),
                    )

                elif function_name in  ['get_current_weather', 'get_daily_weather_forecast', 'get_hourly_weather_forecast']:
                    function_response = function_to_call(
                        location=function_args.get("location"),
                        unit=function_args.get("unit", "metric"),
                        fields=function_args.get("fields"),
                    )
                    
                   
                elif function_name == 'get_weather_on_route':
                    function_response = function_to_call(
                        startLocation=function_args.get("startLocation"),
                        endLocation=function_args.get("endLocation"),
                        mode=function_args.get("mode"),
                    )
                else:
                    function_response = function_to_call()
                            
                print('function response:', function_response)
                
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )  
            second_response = client.chat.completions.create(
                model=GPT_MODEL,
                # temperature=0.2,
                messages=messages,
            )  
            print('------------------------------------------------------------------------------------------')
            return second_response.choices[0].message.content
        else:
            return response_message.content
