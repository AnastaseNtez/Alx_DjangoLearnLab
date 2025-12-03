from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone # Essential for published_date default

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

# --- 2. COMMENT Model (NEW) ---

class Comment(models.Model):
    # Foreign Key linking to the Post this comment belongs to (many-to-one)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    
    # Foreign Key linking to the User who wrote the comment
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # The actual comment text
    content = models.TextField()
    
    # Date and time when the comment was created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Date and time when the comment was last updated
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    def get_absolute_url(self):
        # After editing or deleting, redirect back to the post detail page
        return reverse('blog:post-detail', kwargs={'pk': self.post.pk})

    class Meta:
        # Order comments by creation time, oldest first
        ordering = ['created_at']