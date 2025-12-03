from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# Get the custom or default User model
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """
    A custom form for user creation which includes the email field.
    """
    class Meta:
        # Use the default Django User model
        model = User
        # Include username, email, and password fields
        fields = ('username', 'email')
        
    # Ensure email is required
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True