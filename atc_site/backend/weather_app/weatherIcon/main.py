from .weather import GetWeatherCode
from weather_app.settings import STATIC_ROOT

class GetWeatherIcon:
    def __init__(self):
        pass
    
    def get_icon_name(self):
        ''' returns a weather code '''
        try:
            time_of_day = GetWeatherCode().get_time_of_day()
            print(f'{GetWeatherCode().get_weather_code()}-{time_of_day}')
            return f'{GetWeatherCode().get_weather_code()}-{time_of_day}'
        except Exception as e:
            print('error:', e)
            return None
    
    def get_weather_icon(self):
        name = self.get_icon_name()
        try:
            return (f'//images//weatherIcons//animated//{name}.svg' if self.does_icon_exist(f'//images//weatherIcons//animated//{name}.svg') else self.get_backup_icon())
        except:
            return self.get_backup_icon()
        
    def get_backup_icon(self):
        code = GetWeatherCode().get_weather_code()
        time = GetWeatherCode().get_time_of_day()
        try:
            return (f'//images//weatherIcons//animated//{code}.svg' if self.does_icon_exist(f'//images//weatherIcons//animated//{code}.svg') else f'//images//weatherIcons//animated//1000-{time}.svg')
        except:
            return f'//images//weatherIcons//animated//1000-{time}.svg'
        
    def does_icon_exist(self, icon):
        try:
            with open(f'{STATIC_ROOT}{icon}') as f:
                return True
        except:
            return False