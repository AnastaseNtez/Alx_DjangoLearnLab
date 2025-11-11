from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings  # Import settings to reference AUTH_USER_MODEL


# --- Custom User Manager (Step 3) ---
class CustomUserManager(BaseUserManager):
    """
    Custom user manager to ensure new required fields are handled correctly
    during user and superuser creation.
    """
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        # Override create_user to ensure the model is used correctly
        if not username:
            raise ValueError('The Username field must be set')
        
        email = self.normalize_email(email) if email else None
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given username and password.
        We must explicitly provide a default date_of_birth for the superuser
        creation command if the field is not nullable.
        """
        
        # Ensure superuser fields are set correctly
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, password, **extra_fields)


# --- Custom User Model (Step 1) ---
class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    Adds date_of_birth and profile_photo fields.
    """
    date_of_birth = models.DateField(null=True, blank=True, help_text="User's date of birth")
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        null=True,
        blank=True,
        help_text="User's profile photo"
    )
    
    # Assign the custom manager
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username