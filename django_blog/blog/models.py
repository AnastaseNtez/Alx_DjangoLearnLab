from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse # NEW: Required for get_absolute_url
from django.utils import timezone # NEW: Required for timezone.now

# The Post model represents a single blog entry.
class Post(models.Model):
    # Field 1: Title of the blog post (using max_length=200 from your file)
    title = models.CharField(max_length=200)
    
    # Field 2: The main content/body of the blog post
    content = models.TextField()
    
    # Field 3: Renamed to date_posted to match views, uses default=timezone.now
    # instead of auto_now_add=True so the field is editable in UpdateView.
    date_posted = models.DateTimeField(default=timezone.now) 
    
    # Field 4: Links the post to the User who wrote it.
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
        
    # --- CRITICAL ADDITION FOR CRUD VIEWS ---
    def get_absolute_url(self):
        """
        Tells CreateView and UpdateView where to redirect after successful submission.
        """
        # Uses the URL name 'blog:post-detail' and passes the post's primary key (pk)
        return reverse('blog:post-detail', kwargs={'pk': self.pk})

    # Optional: We can keep the Meta class for ordering here, but PostListView already does this.
    # class Meta:
    #     ordering = ['-date_posted']