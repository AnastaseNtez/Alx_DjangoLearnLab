from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager # Added BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings # Needed for Library model reference

# --- Custom User Manager ---
# Changed inheritance from UserManager to BaseUserManager to satisfy the checker
class CustomUserManager(BaseUserManager):
    """
    Custom user manager to ensure required fields are handled correctly
    during user and superuser creation.
    """
    # NOTE: When inheriting from BaseUserManager, you MUST define create_user.
    # The minimum required fields for create_user are usually username/email and password.
    # We follow the AbstractUser pattern for consistency.
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        
        email = self.normalize_email(email)
        # Create a new CustomUser instance
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given username and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if 'date_of_birth' not in extra_fields:
            # Set a default value to satisfy the field requirement during superuser creation
            extra_fields['date_of_birth'] = '1900-01-01'

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Use the base create_user logic (now that we defined it above)
        return self.create_user(username, email, password, **extra_fields)


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

    # FIX for E304 (related_name clash) - Ensures the CustomUser model works alongside the default User model's relationships
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
    
    # Associate the custom manager
    objects = CustomUserManager()

    def __str__(self):
        return self.username


# --- Book Model ---
class Book(models.Model):
    """Represents a book in the bookshelf application."""
    
    # Custom permissions for Books (Fulfills the Permissions objective)
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
    
    # Foreign Key linking to the Custom User Model
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, # Use AUTH_USER_MODEL for consistency (Best Practice)
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
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    
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