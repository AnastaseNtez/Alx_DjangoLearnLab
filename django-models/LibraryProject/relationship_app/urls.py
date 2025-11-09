# relationship_app/urls.py

from django.urls import path
from . import views
from .views import list_books, LibraryDetailView, register # <-- Include 'register'
from django.contrib.auth.views import LoginView, LogoutView # <-- Import built-in views

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
    # Registration URL
    path('register/', register, name='register'),

    # Login URL (uses built-in LoginView)
    path('login/', LoginView.as_view(
        template_name='relationship_app/login.html'
    ), name='login'),

    # Logout URL (uses built-in LogoutView)
    path('logout/', LogoutView.as_view(
        # The 'next_page' parameter tells Django where to redirect after logout.
        # It should match the name attribute of your login URL.
        next_page='login' 
    ), name='logout'),
]