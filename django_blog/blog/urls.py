from django.urls import path
from django.contrib.auth import views as auth_views
from . import views # Still needed for register, profile, and old home_page
from .views import (
    # These imports are for the new CRUD Class-Based Views (CBVs)
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)

# Namespace for this app, required for {% url 'blog:...' %} in templates
app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
   
    path('new/', PostCreateView.as_view(), name='post-create'),
    
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    
]