import math
from .postcodes import DATA

class PostcodeDatabase:
    def __init__(self, lat, lon): 
        self.lat = lat
        self.lon = lon
        
        self.list_of_dicts = DATA
        
    def get_postcode(self):
        closest_postcode = None
        min_distance = float('inf')

        for postcode in self.list_of_dicts:
            distance = math.sqrt((postcode['lat'] - self.lat)**2 + (postcode['lon'] - self.lon)**2)
            if distance < min_distance:
                min_distance = distance
                closest_postcode = postcode['postcode']

        return closest_postcode
