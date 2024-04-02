from ..config import *

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
    
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'content', 'model')
    search_fields = ('role', 'content', 'model')