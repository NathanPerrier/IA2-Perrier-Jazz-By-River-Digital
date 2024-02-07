import requests
from requests import get
from decouple import config
from django.core.cache import cache
from requests.exceptions import ReadTimeout
from django.contrib.auth.hashers import make_password, check_password

from .models import UserLocationModel

class GetLocation:
    def __init__(self):
        pass

    def get_location(self):
        ip_address = self.get_ip_address()
        print('ip_address:', ip_address)
        if ip_address is not None:
            if UserLocationModel.objects.filter(ip=(UserLocationModel().hash_ip(ip_address))).exists() == False:
                try:
                    location_info = get(f'http://ip-api.com/json/{str(ip_address)}', timeout=8).json()
                    if location_info['status'] == 'success':
                        return self.store_user_location(location_info, ip_address)
                    return None
                except Exception as e:
                    print('error: ', e)
                    return None
            return UserLocationModel.objects.get(ip=UserLocationModel().hash_ip(ip_address))
        return None
        
    def get_ip_address(self):
        try:
            return get('https://api.ipify.org?format=json', timeout=10).json()['ip']
        except Exception as e:
            print('error: ', e)
            return None
        
    def store_user_location(self, location, ip):
        try:
            return UserLocationModel.objects.create(
                ip=UserLocationModel().hash_ip(ip), 
                city=location['city'], 
                region=location['region'], 
                region_name=location['regionName'], 
                country=location['country'], 
                timezone=location['timezone'], 
                lat=location['lat'], 
                lon=location['lon'],
                zip=location['zip'],
                country_code=location['countryCode'],
                isp=location['isp']
            )
        except Exception as e:
            print(f"Error creating user location: {e}")
            return None
        
        