from django.contrib.auth.models import AbstractUser
from django.db import models

# --- CustomUser Manager (re-adding this based on previous context/hints) ---
# It's good practice to have a CustomUserManager if you are using AbstractUser
# but since it's not strictly required to fix this specific error,
# we'll focus on the model definition itself for now.

# If you were previously told to add a CustomUserManager, make sure it's here
# with an appropriate name if needed, but we focus on the class below.

# --- CustomUser Model FIX ---
class CustomUser(AbstractUser):
    # Add unique related_name arguments to avoid clashes with django.contrib.auth.User
    # This is the FIX for the E304 errors!
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='bookshelf_user_set',  # Unique related name for groups
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='bookshelf_user_permissions', # Unique related name for permissions
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    # Add any other fields you previously defined on CustomUser here
    # e.g., location = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.username


# --- Book Model (Include existing models as well) ---
class Book(models.Model):
    """
    Represents a single book in the library.
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        """Returns a string representation of the book (Title by Author)."""
        return f"{self.title} by {self.author} ({self.publication_year})"