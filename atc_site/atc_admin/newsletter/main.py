from ..config import *

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = '__all__'
        
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    search_fields = ('id', 'email')
    
    