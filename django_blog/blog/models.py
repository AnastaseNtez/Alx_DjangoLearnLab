from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone # Essential for setting default date/time

# The Post model represents a single blog entry.
class Post(models.Model):
    # Field 1: Title of the blog post (required, max length 200)
    title = models.CharField(max_length=200)

    # Field 2: The main content/body of the blog post
    content = models.TextField()
    
    # Field 3: Automatically set to the date and time the post was created.
    # We use default=timezone.now instead of auto_now_add=True so the field 
    # remains editable in update views if we ever choose to expose it.
    published_date = models.DateTimeField(default=timezone.now) 
    
    # Field 4: Links the post to the User who wrote it.
    # on_delete=models.CASCADE ensures that if a User is deleted, all their 
    # associated posts are also deleted.
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # A helpful string representation for the Django Admin and shell
    def __str__(self):
        return self.title

    # Define metadata for the model
    class Meta:
        # Orders posts by the published_date in descending order (newest first)
        ordering = ['-published_date']