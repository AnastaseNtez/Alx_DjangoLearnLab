# posts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from rest_framework_nested import routers
from rest_framework_nested.routers import NestedRouterMixin # NEW IMPORT

from .views import PostViewSet, CommentViewSet, FeedView

# FIX: Create a custom router class that combines DefaultRouter with the NestedRouterMixin
# This ensures the parent router has the necessary methods for the NestedSimpleRouter
class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass

# 1. Main Router for Posts
# Use the new, compatible NestedDefaultRouter class
router = NestedDefaultRouter() 
router.register(r'posts', PostViewSet)

# 2. Nested Router for Comments
# This works fine now, as the 'router' variable has the required mixin methods.
posts_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', CommentViewSet, basename='post-comments')

urlpatterns = [
    # 1. Specific path
    path('feed/', FeedView.as_view(), name='feed'), 
    
    # 2. Main Post routes
    path('', include(router.urls)),
    
    # 3. Nested Comment routes
    path('', include(posts_router.urls)),
]