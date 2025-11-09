# relationship_app/urls.py

from django.urls import path
from . import views
from .views import list_books, LibraryDetailView

urlpatterns = [
    # URL for Function-Based View: Lists all books
    # Path: /relationship/books/
    path('books/', views.list_books, name='list_books'),

    # URL for Class-Based View: Displays a specific library detail
    # Path: /relationship/library/Central_Library/ 
    # Use 'slug' (or another field) to look up the library by its name
    path('library/<str:slug>/', 
         LibraryDetailView.as_view(), 
         name='library_detail'),
]