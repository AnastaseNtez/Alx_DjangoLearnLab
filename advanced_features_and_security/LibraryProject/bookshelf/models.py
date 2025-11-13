from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings # Needed for Library model reference

# --- Custom User Manager ---
class CustomUserManager(UserManager):
    """
    Custom user manager to ensure required fields are handled correctly
    during user and superuser creation.
    """
    def create_user(self, username, email=None, password=None, **extra_fields):
        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given username and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if 'date_of_birth' not in extra_fields:
            extra_fields['date_of_birth'] = '1900-01-01'

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


# --- Custom User Model ---
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

    # FIX for E304 (related_name clash)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name="custom_user_set", 
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="custom_user_permissions_set", 
        related_query_name="custom_user_permission",
    )
    
    objects = CustomUserManager()

    def __str__(self):
        return self.username


# --- Book Model ---
class Book(models.Model):
    """Represents a book in the bookshelf application."""
    
    # Custom permissions for Books
    class Meta:
        ordering = ['title']
        permissions = [
            ("can_view", "Can view books"),
            ("can_create", "Can create new books"),
            ("can_edit", "Can edit existing books"),
            ("can_delete", "Can delete books"),
        ]

    author = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField(null=True, blank=True)
    
    # New fields
    isbn = models.CharField(max_length=13, blank=True, null=True)
    description = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, # Use AUTH_USER_MODEL for consistency
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books_created'
    )


    def __str__(self):
        return self.title


# --- Library Model ---
class Library(models.Model):
    """Represents a collection of books (a library)."""
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    
    # Many-to-Many relationship with Book
    books = models.ManyToManyField(Book, related_name='libraries')
    
    def __str__(self):
        return self.name


# --- UserProfile Model ---
class UserProfile(models.Model):
    """Represents additional profile information for a CustomUser."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    
    ROLE_CHOICES = (
        ('standard', 'Standard User'),
        ('librarian', 'Librarian'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='standard')
    bio = models.TextField(blank=True, verbose_name=_('Biography'))
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Profile'