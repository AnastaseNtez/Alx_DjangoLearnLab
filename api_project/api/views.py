from rest_framework import generics
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

# --- 1. Simple List View (retained for the 'books/' path) ---
class BookList(generics.ListAPIView):
    """
    List all books (GET only).
    This serves the path 'books/'
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# --- 2. Full CRUD ViewSet (NEW) ---
class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet that automatically provides 'list', 'create', 'retrieve',
    'update', 'partial_update', and 'destroy' actions.
    This serves the paths 'books_all/' and 'books_all/<pk>/'
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer