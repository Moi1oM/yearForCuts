from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, nickname, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname)
        # user.set_password(password)
        user.save()
        return user
    def create_superuser(self, email, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_admin') is not True:
            raise ValueError(_('Superuser must have is_admin=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email)
        # return self.create_user(email, password, **extra_fields)
# class CustomUserModelManager(BaseUserManager):
#     def create_user(self,email,nickname=None, password = None):

#         user = self.model(
            
#             email = self.normalize_email(email),
#             nickname = nickname
#         )

#         user.set_password(password)
#         user.save(using = self._db)

#         return user

    
#     def create_superuser(self,email, password):
#         user = self.create_user(
#         email,
#         password = password
#         )

#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using = self._db)

#         return user

class UserManager(BaseUserManager):
    def create_superuser(self, email, nickname, password, **other_fields):
        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
      
        if other_fields.get('is_admin') is not True:
            raise ValueError('Superuser must be assigned to is_admin=True')
       
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')
        user =  self.create_user(email, nickname, password, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, nickname, password, **other_fields):
        if not email:
            raise ValueError('Email address is required!')
        email = self.normalize_email(email)
        if password is not None:
            user = self.model(email=email, nickname=nickname,password=password, **other_fields)
            user.save()
        else:
            user = self.model(email=email, nickname=nickname, password=password,**other_fields)
            user.set_unusable_password()
            user.save()

        return user
    # def create_user(self, email, nickname=None, password=None):
    #     if not email:
    #         raise ValueError('Users must have an email address')

    #     user = self.model(
    #         email=self.normalize_email(email),
    #         nickname=nickname
    #     )

    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    # def create_superuser(self, email, password, nickname=None):
    #     user = self.create_user(
    #         email,
    #         password=password,
    #         nickname=nickname,
    #     )
    #     user.is_admin = True
    #     user.save(using=self._db)
    #     return user

