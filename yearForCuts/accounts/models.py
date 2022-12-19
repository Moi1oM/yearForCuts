# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# from django.contrib.auth.models import AbstractUser
# from .managers import CustomUserModelManager
from .managers import CustomUserManager, UserManager
from django.utils.translation import gettext_lazy as _

# class CustomUser(AbstractUser):
#     email = models.EmailField(_('email address'), unique=True)
#     nickname = models.CharField(max_length=100)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     objects = CustomUserManager()
    

#     def __str__(self):
#         return self.email
    

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=150, unique=False, null=True, blank=True)
    
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.email

# class User(AbstractUser):
#     email = models.EmailField(
#         verbose_name='email',
#         max_length=255,
#         unique=True,
#     )
#     nickname = models.CharField(max_length=100, null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['nickname']

#     objects = UserManager()
    

#     def __str__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         return True

#     def has_module_perms(self, app_label):
#         return True
    
#     @property
#     def is_staff(self):
#         return self.is_admin