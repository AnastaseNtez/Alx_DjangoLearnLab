from django.urls import path
from . import views # Correctly imports views.py from the current (blog) directory
from django.contrib.auth import views as auth_views

# Sets the namespace for this app, e.g., blog:home
app_name = 'blog' 

urlpatterns = [
    path('', views.home_page, name='blog-home'),
   
    path('register/', views.register, name='register'),
    
    # 3. User profile page
    path('profile/', views.profile, name='profile'),
    
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
]