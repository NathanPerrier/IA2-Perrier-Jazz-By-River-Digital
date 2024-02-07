import vertexai
from vertexai.vision_models import ImageTextModel, Image
from decouple import config

class VisionAIModel():
    def __init__(self, image):
        
        self.source_image = Image.load_from_file(location=image)
        
        vertexai.init(project=config('GOOGLE_PROJECT_ID'), location='australia-southeast1')
        self.model = ImageTextModel.from_pretrained("imagetext@001")
    
    def get_image_description(self):
        captions = self.model.get_captions(
            image=self.source_image,
            # Optional:
            number_of_results=1,
            language="en",
        )
        print(captions)
        return captions[0].text if captions else None #? works?
    
    def is_image_safe(self):
        answers = self.model.ask_question(
            image=self.source_image,
            question="is this image safe? True/False",
            # Optional:
            number_of_results=1,
        )
        print(answers)
        if 'true' in answers[0].text.lower():
            return True
        return False
        
    