from django.urls import path, include
from rest_framework.routers import DefaultRouter # 1. Import DefaultRouter
from .views import BookList, BookViewSet # 2. Import the new ViewSet

# 3. Create a router instance
router = DefaultRouter()

# 4. Register the ViewSet
router.register(r'books_all', BookViewSet, basename='book_all')

# 5. Define the urlpatterns
urlpatterns = [
    # Route 1: Simple list view (ListAPIView) at /books/
    path('books/', BookList.as_view(), name='book-list'),

    # Route 2: Include the router URLs. 
    # This must be the last entry to catch all router-generated paths.
    path('', include(router.urls)), 
]