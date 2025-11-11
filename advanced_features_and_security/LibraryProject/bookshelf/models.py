from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings # Import settings to reference AUTH_USER_MODEL

# --- Custom User Manager (Step 3) ---
class CustomUserManager(UserManager):
    """
    Custom user manager to ensure new required fields are handled correctly
    during user and superuser creation.
    """
    def create_user(self, username, email=None, password=None, **extra_fields):
        # Override create_user to ensure the model is used correctly
        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given username and password.
        We must explicitly provide a default date_of_birth for the superuser
        creation command if the field is not nullable.
        """
        # Ensure superuser fields are set correctly
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Set a dummy date_of_birth if not provided for superuser creation
        if 'date_of_birth' not in extra_fields:
            extra_fields['date_of_birth'] = '1900-01-01'

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


# --- Custom User Model (Step 1) ---
class CustomUser(AbstractUser):
    """
    A custom user model extending AbstractUser to add custom fields.
    """
    date_of_birth = models.DateField(
        _('date of birth'),
        null=True, 
        blank=True
    )
    profile_photo = models.ImageField(
        _('profile photo'),
        upload_to='profile_photos/',
        null=True,
        blank=True
    )

    # Use the custom manager
    objects = CustomUserManager()

    def __str__(self):
        return self.username

# --- Example of Model Reference Update (Step 5) ---

class Book(models.Model):
    """Represents a book in the bookshelf application."""
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField(null=True, blank=True)
    
    # *** CRITICAL FIX: Reference the user model using the full AUTH_USER_MODEL path ***
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, # Uses the value 'LibraryProject.bookshelf.CustomUser'
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books_created'
    )

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title