# posts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter 

from .views import PostViewSet, CommentViewSet, FeedView

# 1. Main Router for Posts
# Use the standard DRF DefaultRouter for Posts
router = DefaultRouter() 
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    # --- NON-ROUTED PATHS ---
    
    # 1. Feed View
    path('feed/', FeedView.as_view(), name='feed'), 

    # 2. Liking and Unliking Paths (REQUIRED STRINGS)
    # These manually call the @action method 'toggle_like'
    
    # REQUIRED STRING 1: <int:pk>/like/
    path('posts/<int:pk>/like/', 
         PostViewSet.as_view({'post': 'toggle_like'}), 
         name='post-toggle-like'),
         
    # REQUIRED STRING 2: <int:pk>/unlike/
    path('posts/<int:pk>/unlike/', 
         PostViewSet.as_view({'post': 'toggle_like'}), # Maps to the same toggle action
         name='post-toggle-unlike'),
    
    # --- ROUTER INCLUSION ---
    
    # 3. Main Post routes (list, create, retrieve, update, delete)
    path('', include(router.urls)),

    # --- MANUAL NESTED COMMENT PATHS (Replaces buggy rest_framework_nested) ---
    
    # 4. List and Create comments for a specific post: /posts/{post_pk}/comments/
    path('posts/<int:post_pk>/comments/', 
         CommentViewSet.as_view({'get': 'list', 'post': 'create'}), 
         name='post-comments-list'),
    
    # 5. Detail, Update, Delete for a specific comment: /posts/{post_pk}/comments/{pk}/
    path('posts/<int:post_pk>/comments/<int:pk>/', 
         CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), 
         name='post-comments-detail'),
]