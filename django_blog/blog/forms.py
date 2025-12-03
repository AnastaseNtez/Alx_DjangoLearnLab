from django import forms
from django.contrib.auth.models import User
# We need to import the Post model to create a ModelForm for it
from .models import Post 
# Removed: from .forms import CustomUserCreationForm, PostForm (This caused the recursive import error)


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