from ..config import *

class TicketsForm(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = '__all__'

class TicketsAdmin(admin.ModelAdmin):
    list_display = ('user', 'sent')

    
    