from ..config import *

class EventScheduleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'event', 'event_item')
    search_fields = ('id', 'event', 'event_item')
    
    
class EventScheduleItemForm(forms.ModelForm):
    class Meta:
        model = EventScheduleItem
        fields = '__all__'

    def clean_reset_end_time(self):
        end_time = self.cleaned_data.get('end_time')
        start_time = self.cleaned_data.get('start_time')
        if end_time and start_time and end_time < start_time:
            raise ValidationError('End time must be after start time')
        return end_time
    
class EventScheduleItemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = EventScheduleItemForm
    list_display = ('title', 'description', 'start_time', 'end_time', 'last_modified', 'creation_time')
    search_fields = ('title', 'description', 'start_time', 'end_time')
    
    def save_model(self, request, obj, form, change):
        obj.save()
        super().save_model(request, obj, form, change)