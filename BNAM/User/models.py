from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
# Create your models here.

class UserProfileManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    def create_staffuser(self, email,username, password=None):
        user = self.create_user(email,
            password=password,
            username=username
        )     
        user.is_staff = True
        user.save(using=self._db)
        
        return user
    def create_superuser(self, email, username, password=None):
        user = self.create_user(email,
            password=password,
            username=username
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        
        return user
    
class UserProfile(AbstractBaseUser):
  
    email = models.EmailField(verbose_name='email address',
        max_length=255,unique=True,
        )
    username = models.CharField(_('username'),
        max_length=150,
        unique=True,
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]     
    objects = UserProfileManager()
    
    def get_full_name(self):
        return self.email
    def get_short_name(self):
        return self.email
    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True