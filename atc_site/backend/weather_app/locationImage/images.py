from .google_images_download import google_images_download 
from ..location.main import GetLocation
from weather_app.settings import STATIC_ROOT

class GetImagesFromLocation:
    def __init__(self):
        self.image_dir = f'{STATIC_ROOT}//images//locationImages//'
        
        self.location = GetLocation().get_location()
        
        self.query = f'{self.location.city}-{self.location.zip}-{self.location.country},{self.location.city}'
        
        self.response = google_images_download.googleimagesdownload()

    def downloadimages(self):
        '''
            -keywords is the search query
            -format is the image file format
            -limit is the number of images to be downloaded
            -print urls is to print the image file url
            -size is the image size which can
            -be specified manually ("large, medium, icon")
            -aspect ratio denotes the height width ratio
            -of images to download. ("tall, square, wide, panoramic")
        '''
        arguments = {"keywords": self.query,
                 "format": "jpg",
                 "limit":4,
                 "print_urls":True,
                 "print_paths":True,
                #  "safe_search":True,
                #  "no_download":True,
                 "size": "large",
                 "type": "photo",
                #  'output_directory': self.image_dir,
                 "aspect_ratio":"wide"}
        try:
            response = self.response.download(arguments)
            print(response)
        
        # Handling File NotFound Error    
        except FileNotFoundError: 
            arguments = {"keywords": self.query,
                        "format": "jpg",
                        "limit":4,
                        "print_urls":True,
                        #"print_paths":True,
                        "safe_search":True,
                        "no_download":True,
                        "size": "large",
                        "type": "photo",
                        'output_directory': self.image_dir,
                        "aspect_ratio":"wide"}
                        
            # Providing arguments for the searched query
            try:
                # Downloading the photos based
                # on the given arguments
                response = self.response.download(arguments) 
                print(response)
            except:
                pass