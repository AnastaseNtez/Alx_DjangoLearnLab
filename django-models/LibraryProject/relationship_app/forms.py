# relationship_app/forms.py

from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    # This class can be left empty if you don't need extra fields, 
    # but defining it ensures a clean form based on the default User model.
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields