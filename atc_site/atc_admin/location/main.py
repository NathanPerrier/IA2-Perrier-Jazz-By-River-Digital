from ..config import *
import hashlib

class UserLocationForm(forms.ModelForm):
    class Meta:
        model = UserLocationModel
        fields = '__all__'
    
    def clean_ip(self):
        ip = self.cleaned_data.get('ip')
        if ip and len(ip) > 15:
            raise ValidationError('IP must be 15 characters long')
        return ip

class UserLocationModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = UserLocationForm
    list_display = ('ip', 'city', 'region', 'region_name', 'country', 'zip', 'lat', 'lon', 'timezone', 'country_code', 'isp')
    search_fields = ('ip', 'city', 'region', 'region_name', 'country', 'zip', 'lat', 'lon', 'timezone', 'country_code', 'isp')
    
    def save_model(self, request, obj, form, change):
        if 'ip' in form.changed_data:
            
            obj.ip = hash_ip(obj.ip)
            
        super().save_model(request, obj, form, change)
        
def hash_ip(ip):
    return hashlib.sha256(ip.encode()).hexdigest()
