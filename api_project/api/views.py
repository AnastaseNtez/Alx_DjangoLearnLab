from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions # <-- Import permissions
from .models import Book
from .serializers import BookSerializer

# --- 1. Simple List View (read-only, public) ---
class BookList(generics.ListAPIView):
    """
    List all books (GET only).
    Accessed at /api/books/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Allow anyone to view the simple list
    permission_classes = [permissions.AllowAny]


# --- 2. Full CRUD ViewSet (Secured for writes) ---
class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet that automatically provides full CRUD actions.
    Accessed at /api/books_all/
    
    Permissions:
    - GET (list, retrieve): Allowed for everyone (Read-Only).
    - POST, PUT, PATCH, DELETE: Only allowed for authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # --- PERMISSION CLASS DEFINITION (Step 3 Implementation) ---
    # IsAuthenticatedOrReadOnly: Requires authentication for unsafe methods (POST, PUT, DELETE), 
    # but allows unauthenticated access for safe methods (GET, HEAD, OPTIONS).
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]