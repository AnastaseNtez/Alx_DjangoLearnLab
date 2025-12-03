from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm # Import our custom form

# Placeholder view for the main blog app (if not already present)
def home_page(request):
    """
    Placeholder for the main blog landing page.
    """
    return render(request, 'blog/home.html') 

def register(request):
    """
    Handles user registration using the CustomUserCreationForm.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
        
    context = {'form': form, 'title': 'Register'}
    return render(request, 'blog/register.html', context)

@login_required 
def profile(request):
    """
    Allows authenticated users to view their profile. 
    A more advanced version would handle POST requests for profile editing.
    """
    if request.method == 'POST':
        # Simple profile update logic (e.g., updating email, though Django's built-in forms 
        # for User model are complex, so we keep this view simple for now).
        # For this task, we will focus on viewing the profile.
        pass
    
    # Passes the current user object to the template
    context = {'title': 'Profile'}
    return render(request, 'blog/profile.html', context)

# --- Add other Blog views here as needed for other steps ---