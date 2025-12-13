# accounts/urls.py

from django.urls import path
from .views import RegistrationView, LoginView, UserProfileView, FollowToggleView 

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    
    path('login/', LoginView.as_view(), name='login'),

    path('profile/<str:username>/', UserProfileView.as_view(), name='user-profile'),
    
    path('follow/<int:user_id>/', FollowToggleView.as_view(), name='follow-toggle'), 
    
    # REQUIRED STRING
    path('unfollow/<int:user_id>/', FollowToggleView.as_view(), name='unfollow-toggle'), 
]