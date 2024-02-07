from .models import LocationImagesModel
from ..location.main import GetLocation
from .images import GetImagesFromLocation
from .visionAI import VisionAIModel

class GetLocationImage:
    def __init__(self):
        self.location = GetLocation().get_location()
        
    def get_location_image(self):
        if not self.does_location_image_exist():
            images = GetImagesFromLocation().downloadimages()
            #split images
            for image in images:
                if VisionAIModel().is_image_safe(image):
                    self.location_image = LocationImagesModel.objects.create(
                        country=self.location.country,
                        city=self.location.city,
                        lat=self.location.lat,
                        lon=self.location.lon,
                        image_url=image,
                        is_safe=True
                    )
                    return self.location_image.image_url
            return None  #? self.get_location_image() with new prompt?
        return self.location_image.image_url
        
    def does_location_image_exist(self):
        try:
            self.location_image = LocationImagesModel.objects.get(city=self.location['city'])
            return True
        except Exception as e:
            print('error:', e)
            return False