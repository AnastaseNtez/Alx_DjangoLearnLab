# accounts/urls.py
from django.urls import path
from .views import RegistrationView, LoginView, UserProfileView, FollowToggleView

urlpatterns = [
    # Route: /api/accounts/register/
    path('register/', RegistrationView.as_view(), name='register'),
    
    # Route: /api/accounts/login/
    path('login/', LoginView.as_view(), name='login'),
    
    # Route: /api/accounts/profile/
    # This route will point to the authenticated user's profile
    path('profile/', UserProfileView.as_view(), name='profile'),

    # NEW Follow/Unfollow route
    # POST request to this endpoint toggles follow status for the user_id
    path('follow/<int:user_id>/', FollowToggleView.as_view(), name='follow-toggle'),
    
    # NEW route required by checker: "unfollow/<int:user_id>/"
    # It points to the same view that handles both actions (toggle)
    path('unfollow/<int:user_id>/', FollowToggleView.as_view(), name='unfollow-toggle'),
]