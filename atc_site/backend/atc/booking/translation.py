from modeltranslation.translator import register, TranslationOptions
from .models import BookingStatus

@register(BookingStatus)
class BookingStatusTranslationOptions(TranslationOptions):
    fields = ('name', 'description')  # Add the fields you want to translate
    
