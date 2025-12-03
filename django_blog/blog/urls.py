from django.urls import path
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
    
    
    # Create Comment (Uses the function-based view, linked to the Post's PK)
    path('posts/int:post_id/comments/new/', views.CommentCreateView.as_view(), name='comment-create'),

    # Update Comment (Uses the Comment's PK)
    # The URL pattern for the comment PK must be different from the post PK to ensure the URL resolver works correctly.
    path('posts/int:post_id/comments/update/', views.CommentUpdateView.as_view(), name='comment-update'),
    
    # Delete Comment (Uses the Comment's PK)
    path('posts/int:post_id/comments/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
]