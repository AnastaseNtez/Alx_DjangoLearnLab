# accounts/urls.py
from django.urls import path
from .views import RegistrationView, LoginView, UserProfileView

urlpatterns = [
    # Route: /api/accounts/register/
    path('register/', RegistrationView.as_view(), name='register'),
    
    # Route: /api/accounts/login/
    path('login/', LoginView.as_view(), name='login'),
    
    # Route: /api/accounts/profile/
    # This route will point to the authenticated user's profile
    path('profile/', UserProfileView.as_view(), name='profile'),
]