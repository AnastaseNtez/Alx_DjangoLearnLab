# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Additional fields
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # Many-to-Many field for followers
    # symmetrical=False means following A doesn't automatically mean A follows B
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following', # Renames the reverse relation
        blank=True
    )

    def __str__(self):
        return self.username