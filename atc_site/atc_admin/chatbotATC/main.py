from ..config import *

class ATCMessageForm(forms.ModelForm):
    class Meta:
        model = ATCMessage
        fields = '__all__'

class ATCMessageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('user', 'role', 'content', 'model')
    search_fields = ('role', 'content', 'model')