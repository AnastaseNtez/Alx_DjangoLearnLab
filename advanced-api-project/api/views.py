# api/views.py

from rest_framework import generics, permissions, filters
# Alias 'rest_framework' is now the DjangoFilterBackend class itself.
from django_filters.rest_framework import DjangoFilterBackend as rest_framework 
from .models import Book
from .serializers import BookSerializer
from .filters import BookFilter 

# --- Book List and Create View ---

class BookListCreateView(generics.ListCreateAPIView):
    """
    Handles API requests for listing all books (GET) and creating a new book (POST).
    
    This view incorporates filtering, searching, and ordering functionality 
    to enhance API query flexibility.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Permissions Setup: Allows any user to read (GET), but only authenticated users to write (POST).
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

    # ----------------------------------------------------
    # Query Functionality Setup (Filtering, Searching, Ordering)
    # ----------------------------------------------------
    
    # Define the filter backends to be used
    filter_backends = [
        # *** CORRECTED LINE HERE ***
        rest_framework, # Use the alias 'rest_framework' alone, as it points to DjangoFilterBackend
        filters.SearchFilter,                
        filters.OrderingFilter               
    ]
    
    # Links the view to the custom BookFilter for complex filtering
    filterset_class = BookFilter

    # Define fields that can be searched using the ?search= parameter
    search_fields = ['title', 'author__name']
    
    # Define fields that can be used for ordering using the ?ordering= parameter
    ordering_fields = ['title', 'publication_year', 'author']
    
    # Set a default ordering for the results
    ordering = ['title'] 


# --- Book Detail, Update, and Delete View ---

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles API requests for a single book instance:
    - Detail retrieval (GET)
    - Update (PUT/PATCH)
    - Deletion (DELETE)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Permissions Setup: Allows any user to read (GET), but only authenticated users to write (PUT/PATCH/DELETE).
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]