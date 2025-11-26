# api/urls.py

from django.urls import path
from .views import BookListCreateView, BookRetrieveUpdateDestroyView

urlpatterns = [
    # Endpoint for List and Create operations (GET, POST)
    # URL: /api/books/
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    
    # Endpoint for Detail, Update, and Destroy operations (GET, PUT, PATCH, DELETE)
    # URL: /api/books/<id>/
    path('books/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-detail-update-delete'),
]