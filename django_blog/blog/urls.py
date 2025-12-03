from django.urls import path
from . import views

# Set the application namespace for reverse lookups (e.g., 'blog:post-detail')
app_name = 'blog'

urlpatterns = [
    # --- AUTHENTICATION & PROFILE VIEWS ---
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    
    # --- POST VIEWS (CRUD) ---
    
    # Home/List View (Read All)
    path('', views.PostListView.as_view(), name='blog-home'),
    
    # Detail View (Read One)
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    
    # Create Post
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    
    # Update Post
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    
    # Delete Post
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    
    
    # --- COMMENT VIEWS (CRUD) ---
    
    # Create Comment (Uses the function-based view, linked to the Post's PK)
    path('post/<int:pk>/comment/add/', views.add_comment, name='add-comment'),

    # Update Comment (Uses the Comment's PK)
    # The URL pattern for the comment PK must be different from the post PK to ensure the URL resolver works correctly.
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update'),
    
    # Delete Comment (Uses the Comment's PK)
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
]