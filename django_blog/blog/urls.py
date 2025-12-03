from django.urls import path
from . import views # Correctly imports views.py from the current (blog) directory

# Sets the namespace for this app, e.g., blog:home
app_name = 'blog' 

urlpatterns = [
    # 1. Home page: Accessible at the root path ('/') since the project urls.py delegates to us.
    path('', views.home_page, name='blog-home'),
    
    # 2. User registration page
    path('register/', views.register, name='register'),
    
    # 3. User profile page
    path('profile/', views.profile, name='profile'),
    
    # Note: Login and Logout are already handled in the main django_blog/urls.py
]