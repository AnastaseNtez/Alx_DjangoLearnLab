from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# Set the application namespace for reverse lookups (e.g., 'blog:post-detail')
app_name = 'blog'

urlpatterns = [
    path('register/', views.register, name='register'),

    path('profile/', views.profile, name='profile'),
    
    
    path('', views.PostListView.as_view(), name='blog-home'),
    
    
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    
    
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    
    
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='comment-create'),

    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update'),
    
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
   
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),

    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),

    path('tag/<slug:tag_slug>/', views.PostListView.as_view(), name='post-list-by-tag'), 
]