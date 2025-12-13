# posts/urls.py
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from django.urls import path, include
from .views import PostViewSet, CommentViewSet

# 1. Main Router for Posts
router = DefaultRouter()
# Register PostViewSet at /posts/
router.register(r'posts', PostViewSet)

# 2. Nested Router for Comments
# The base route for comments will be /posts/{post_pk}/comments/
posts_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
# Register CommentViewSet nested under posts
posts_router.register(r'comments', CommentViewSet, basename='post-comments')

urlpatterns = [
    # Main Post routes (list, create, detail, update, delete)
    path('', include(router.urls)),
    
    # Nested Comment routes (list comments for a post, create comment on a post)
    path('', include(posts_router.urls)),
]