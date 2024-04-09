from ..config import *

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = '__all__'
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('Email is required')
        elif email in Newsletter.objects.values_list('email', flat=True):
            raise ValidationError('Email already exists')
        return email    
    
class NewsletterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = NewsletterForm
    list_display = ('id', 'email')
    search_fields = ('id', 'email')
    
    