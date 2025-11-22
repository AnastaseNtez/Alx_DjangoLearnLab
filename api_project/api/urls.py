from django.urls import path
from .views import BookList

# Define the namespace for this application's URLs
app_name = 'api'

urlpatterns = [
    # Maps the 'books/' path to the BookList view. 
    # This will handle GET requests to retrieve the list of books.
    # The full path will be /api/books/ (due to the include in project urls.py)
    path('books/', BookList.as_view(), name='book-list'),
]