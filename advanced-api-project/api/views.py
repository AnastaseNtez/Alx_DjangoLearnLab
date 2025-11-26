# api/views.py

from rest_framework import generics, permissions, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer
from django_filters.rest_framework import DjangoFilterBackend # Import DjangoFilterBackend
from .filters import BookFilter # Import the new custom FilterSet

# --- Book List and Create View ---

# Combines ListView (ListModelMixin) and CreateView (CreateModelMixin)
# Endpoint: /books/
class BookListCreateView(generics.ListCreateAPIView):
    """
    Retrieves a list of all Book objects (GET) and allows creation of a new Book (POST).
    This view now supports filtering, searching, and ordering via URL query parameters.
    Configuration:
    - queryset: Defines the data source (all books).
    - serializer_class: Specifies the serializer for data handling.
    - permission_classes: Restricts POST (Create) to authenticated users, 
      while allowing GET (List) for any user (IsAuthenticatedOrReadOnly).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Permissions: Read-only access for unauthenticated users, Write access for authenticated users.
    #permission_classes = [IsAuthenticatedOrReadOnly] 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,  # Handles filtering (e.g., ?publication_year=2000)
        filters.SearchFilter, # Handles searching (e.g., ?search=Tolkien)
        filters.OrderingFilter  # Handles ordering (e.g., ?ordering=-publication_year)
    ]
    
    # Step 1: Set up the custom FilterSet for advanced filtering
    filterset_class = BookFilter

    # Step 2: Define fields that can be searched (using icontains lookup)
    # The 'author__name' field allows searching by the author's name linked via the FK.
    search_fields = ['title', 'author__name']
    
    # Step 3: Define fields that can be used for ordering
    ordering_fields = ['title', 'publication_year', 'author']
    
    # Optional: Set a default ordering
    ordering = ['title']
# --- Book Detail, Update, and Delete View ---

# Combines DetailView (RetrieveModelMixin), UpdateView (UpdateModelMixin), 
# and DeleteView (DestroyModelMixin).
# Endpoint: /books/<int:pk>/
class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieval (GET), updating (PUT/PATCH), and deletion (DELETE) of a single Book instance.

    Configuration:
    - queryset: Defines the data source (used for lookup).
    - serializer_class: Specifies the serializer for data handling.
    - permission_classes: Restricts PUT/PATCH/DELETE to authenticated users, 
      while allowing GET (Detail) for any user (IsAuthenticatedOrReadOnly).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Permissions: Read-only access for unauthenticated users, Write access for authenticated users.
    permission_classes = [IsAuthenticatedOrReadOnly]