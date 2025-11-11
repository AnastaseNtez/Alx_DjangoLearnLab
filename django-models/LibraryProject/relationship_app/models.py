from django.db import models
from django.conf import settings 
# We don't need get_user_model() explicitly here if we use settings.AUTH_USER_MODEL 
# for the ForeignKey and string references for the signals.
from django.db.models.signals import post_save
from django.dispatch import receiver

# Author Model
class Author(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


# Book Model
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    
    class Meta:
        # Define the custom permissions here
        permissions = [
            ("can_add_book", "Can add a book entry"),
            ("can_change_book", "Can edit a book entry"),
            ("can_delete_book", "Can delete a book entry"),
        ]
    
    def __str__(self):
        return self.title


# Library Model
class Library(models.Model):
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book, related_name='libraries')
    
    def __str__(self):
        return self.name


# Librarian Model
class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')
    
    def __str__(self):
        return self.name

# --- User Profile for Role-Based Access Control (RBAC) ---

class UserProfile(models.Model):
    # Role Choices
    ROLE_ADMIN = 'Admin'
    ROLE_LIBRARIAN = 'Librarian'
    ROLE_MEMBER = 'Member'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_LIBRARIAN, 'Librarian'),
        (ROLE_MEMBER, 'Member'),
    ]

    # BEST PRACTICE: Use settings.AUTH_USER_MODEL for ForeignKey reference
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, # This resolves to 'bookshelf.CustomUser'
        on_delete=models.CASCADE
    )
    
    # Role field, defaulting to Member
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_MEMBER,
    )

    def __str__(self):
        # We assume the user has a username field
        return f"{self.user.username} - {self.role}"


# --- Signals ---

# BEST PRACTICE: Use the string reference for the sender in signals
# This avoids importing the model directly, which can cause circular imports.

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """Signal to automatically create UserProfile when a new User is created."""
    if created:
        # Automatically create profile and set default role to Member
        UserProfile.objects.create(user=instance, role=UserProfile.ROLE_MEMBER)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """Signal to save the UserProfile when the associated User is saved."""
    # This check ensures the UserProfile exists before trying to save it
    # which is especially important if you run this on existing users.
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()