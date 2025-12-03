from django import forms
from django.contrib.auth.models import User
# We need to import the Post model to create a ModelForm for it
from .models import Post 
# Removed: from .forms import CustomUserCreationForm, PostForm (This caused the recursive import error)

from .models import Post, Comment # Ensure Comment is imported

# Assuming this form is for user registration
class CustomUserCreationForm(forms.ModelForm):
    # This structure is commonly used for custom registration forms
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

# Defined the missing PostForm for your Create and Update views
class PostForm(forms.ModelForm):
    """
    A form for creating and updating blog posts.
    """
    class Meta:
        model = Post
        # We only need the user to input the title and content
        fields = ['title', 'content']

# --- NEW: CommentForm for creating and editing comments ---
class CommentForm(forms.ModelForm):
    """
    ModelForm specifically for the Comment model.
    It only exposes the content field to the user.
    """
    class Meta:
        model = Comment
        # Only include content, the rest (post, author, dates) are set in the view
        fields = ['content']
        widgets = {
            # Use Textarea for a larger input box, with a helpful placeholder
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your comment here...'}),
        }