from typing import Any
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

    
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
    
    
class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=254, blank=False)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email


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
