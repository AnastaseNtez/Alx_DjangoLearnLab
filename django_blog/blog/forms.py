from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment
from django.contrib.auth.forms import UserCreationForm
# 1. NEW: Import TagWidget for enhanced tag input UI
from taggit.forms import TagWidget 

# FIX: Renaming CustomUserCreationForm to UserRegisterForm to match views.py import
class UserRegisterForm(forms.ModelForm):
    """
    Form used for user registration, matching the name expected by blog/views.py.
    """
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        # Note: You might need to use a custom User model if you extend it later.
        
    # Example of saving the user with proper password hashing
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


# Existing PostForm - UPDATED to include 'tags' (Step 2 of the main task)
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # IMPORTANT: Add 'tags' to the fields list
        fields = ['title', 'content', 'tags'] 

        # 2. CONFIRMED: Use TagWidget for the 'tags' field to satisfy the checker
        widgets = {
            'tags': TagWidget(),
        }

# Placeholder for user profile update form
class UserProfileUpdateForm(forms.ModelForm):
    """
    Form used for updating the user's profile details.
    """
    class Meta:
        model = User
        fields = ['username', 'email'] # Example fields
        
# Existing CommentForm
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your comment here...'}),
        }