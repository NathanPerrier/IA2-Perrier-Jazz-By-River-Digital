from ..config import *

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = '__all__'

class RouteAdmin(admin.ModelAdmin):
    list_display = ('ip', 'route', 'start', 'end', 'mode')
    search_fields = ('ip', 'route', 'start', 'end', 'mode')
    