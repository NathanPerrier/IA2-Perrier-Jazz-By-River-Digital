from typing import Any
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import Group
import re

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        self.check_group(email, **extra_fields)
        return user
        
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self.create_user(email, password, **extra_fields)
    
    def create_staff(self, email, password=None, **extra_fields):
        extra_fields['is_staff'] = True
        return self.create_user(email, password, **extra_fields)
    
    def check_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        else:
            if self.is_teacher(extra_fields['first_name'], extra_fields['last_name'], email):
                return self.create_staff(email, password, **extra_fields)       
            if self.is_admin(extra_fields['first_name'], extra_fields['last_name'], email):
                return self.create_superuser(email, password, **extra_fields) 
            else:
                return self.create_user(email, password, **extra_fields)
    
    def check_group(self, email, **extra_fields):
        if self.is_teacher(extra_fields['first_name'], extra_fields['last_name'], email):
            self.assign_user_to_group(email, 'Teachers')
        elif self.is_student(email):
            self.assign_user_to_group(email, 'Students')
        else:
            self.assign_user_to_group(email, 'User')
            

    def is_admin(self, first_name, last_name, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@atc\.qld\.edu\.au$'
        if not self.is_student(email) and not self.is_teacher(first_name, last_name, email):
            if re.match(pattern, email):
                return True
        return False
    
    def is_teacher(self, first_name, last_name, email):
        pattern = r'^' + re.escape(last_name.lower() + first_name[0].lower()) + r'@atc\.qld\.edu\.au$'
        return re.match(pattern, email) is not None
    
    def is_student(self, email):
        pattern = r'^\d+@atc\.qld\.edu\.au$'
        return re.match(pattern, email) is not None
    
    def update_password(self, email, password):
        user = self.get_by_email(email)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def authenticate(self, email, password):
        user = self.get_by_email(email)
        if user is not None and user.check_password(password):
            return user
        return None
    
    
    def normalize_email(self, email):
        return email.lower()
    
    def get_by_email(self, email):
        try:
            print(CustomUser.objects.get(email=email))
            return CustomUser.objects.get(email=email)  #! issue so defualts to none
        except:
            return None

    def get_by_id(self, id):
        try:
            return CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            return None
        
    def delete_by_id(self, id):
        try:
            self.get(id=id).delete()
            return True
        except CustomUser.DoesNotExist:
            return False
    
    def delete_by_email(self, email):
        try:
            self.get(email=email).delete()
            return True
        except:
            return False
        
    def assign_user_to_group(self, user_email, group_name):
        user = CustomUser.objects.get(email=user_email)
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        user.save()
        
    
class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=254, blank=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # True if the user is a superuser, else False
        return self.is_superuser

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # True if the user is a superuser, else False
        return self.is_superuser
    

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name="customuser_groups",
        related_query_name="customuser",
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name="customuser_user_permissions",
        related_query_name="customuser",
        help_text='Specific permissions for this user.',
    )
