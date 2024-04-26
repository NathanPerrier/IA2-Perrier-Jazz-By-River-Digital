from ..config import *
import re

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance.email != email:
            if not email:
                raise ValidationError('Email is required')
            if email in CustomUser.objects.values_list('email', flat=True):
                raise ValidationError('Email already exists')
        return email
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        pattern = r'^[A-Za-z]+$'
        if re.match(pattern, first_name) is None:
            raise ValidationError('First name must only contain letters')
        return first_name
        
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        pattern = r'^[A-Za-z]+$'
        if re.match(pattern, last_name) is None:
            raise ValidationError('Last name must only contain letters')
        return last_name
        
    def clean_password(self):  
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long')
        elif not any(char.isdigit() for char in password):
            raise ValidationError('Password must contain at least one digit')
        elif not any(char.isupper() for char in password):
            raise ValidationError('Password must contain at least one uppercase letter')
        return password

class CustomUserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = CustomUserForm
    list_display = ('email', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'last_login')
    search_fields = ('email', 'is_superuser', 'is_staff', 'first_name', 'last_name')
    
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/delete/', self.admin_site.admin_view(self.delete_view), name='delete'),
        ]
        return custom_urls + urls
    
    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.password = make_password(obj.password)
            
        super().save_model(request, obj, form, change)
            
        if obj.email.endswith('@atc.qld.edu.au') and (obj.email not in CustomUser.objects.values_list('email', flat=True)):
            if is_teacher(obj, obj.first_name, obj.last_name, obj.email):
                obj.groups.add(Group.objects.get(name='Teacher'))
                obj.is_staff = True
            elif is_student(obj, obj.email):
                obj.groups.add(Group.objects.get(name='Student'))
            else:
                obj.is_superuser = True
                obj.is_staff = True
                obj.groups.add(Group.objects.get(name='Admin'))
            
        try:
            stripe.Customer.modify(
                id=f'customuser-{str(obj.id)}',
                name=str(obj.first_name + ' ' + obj.last_name),
                email=obj.email,
            )
        except Exception as e:
            print(e)
            stripe.Customer.create(
                id=f'customuser-{str(obj.id)}',
                name=str(obj.first_name + ' ' + obj.last_name),
                email=obj.email,
            )

        if not change:
            EmailAddress.objects.create(user=obj, email=obj.email, primary=True, verified=True)
    

    def delete_view(self, request, object_id, extra_context=None):
        obj = self.get_object(request, object_id)
        
        stripe.Customer.delete(f'customuser-{str(obj.id)}')
        
        return super().delete_view(request, object_id, extra_context)
    

def is_teacher(self, first_name, last_name, email):
        pattern = r'^' + re.escape(last_name.lower() + first_name[0].lower()) + r'@atc\.qld\.edu\.au$'
        return re.match(pattern, email) is not None
    
def is_student(self, email):
    pattern = r'^\d+@atc\.qld\.edu\.au$'
    return re.match(pattern, email) is not None