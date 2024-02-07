from .__init__ import *
from ..models import LocationImagesModel
from ..visionAI import VisionAIModel
from django.core.files.base import ContentFile

class GenerateLocationImage:
    def __init__(self, location=None, city=None, region=None, country=None, lat=None, lon=None):
        self.location = location
        if location:
            self.city = location.city
            self.region = location.region
            self.country = location.country
            self.lat = location.lat
            self.lon = location.lon
        else:
            self.city = city
            self.region = region
            self.country = country
            self.lat = lat
            self.lon = lon
            
        self.prompt = f'{self.city}, {self.region}, {self.country}' 
    
    def generate(self):
        print('CREATIN AI IMAGE WITH PROMPT:', self.prompt)
        response = client.images.generate(
            model=MODEL,
            prompt=self.prompt,
            size="1024x1024",
            style="natural", #natural or vivid
            quality="hd", #standard
            n=1,
        )
        return self.save_image(response.data[0].url)
    
    def get_image(self):
        # LocationImagesModel.objects.filter(city=self.city).delete()
        if LocationImagesModel.objects.filter(city=self.city).exists():
            return LocationImagesModel.objects.get(city=self.city)
        return self.generate()
        

    def save_image(self, url):

        file_name = str(uuid.uuid4()) + '.png'

        file_name = self.check_dir(os.path.join(FILE_PATH, file_name))
        
        # if VisionAIModel(directory).is_image_safe():
        image = self.add_image_to_db(file_name=file_name, response=requests.get(url))
        return image
    
    def add_image_to_db(self, response, file_name):
        self.location_image = LocationImagesModel(
            country=self.country,
            city=self.city,
            lat=self.lat,
            lon=self.lon,
            is_safe=True
        )
        self.location_image.image_url.save(file_name, ContentFile(response.content), save=True)
        return self.location_image

    def generate_name(self, length=50):
        # generate a random name for the image
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
    
    def check_dir(self, directory):
        # check if the directory exists
        if os.path.exists(directory): 
            return self.check_dir((FILE_PATH + self.generate_name() + '.png')).split(FILE_PATH)[1]
        return directory.split(FILE_PATH)[1]
