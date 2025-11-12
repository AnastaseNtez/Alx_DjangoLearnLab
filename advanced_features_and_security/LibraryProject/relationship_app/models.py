from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
# Note: The 'bookshelf' CustomUser is used here via get_user_model()

from django.contrib.auth import get_user_model 
User = get_user_model() 

# --- Custom Permissions Setup (Step 1 & 5) ---
# All custom permissions for the system are defined within the Book model.

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
            # CRUD permissions for the Book model
            ("can_view", "Can view book list and details"),
            ("can_create", "Can add a new book entry"),
            ("can_edit", "Can modify an existing book entry"),
            ("can_delete", "Can remove a book entry"),
        ]
        ordering = ['title']
    
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

    # OneToOne relationship to your custom User model
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    
    # Role field, defaulting to Member
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_MEMBER,
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# Signal to automatically create UserProfile when a new User is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, role=UserProfile.ROLE_MEMBER)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()