from ..config import *

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = '__all__'
        
class NewsletterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'email')
    search_fields = ('id', 'email')
    
    