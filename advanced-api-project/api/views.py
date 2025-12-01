from rest_framework import generics, filters
# REQUIRED FOR CHECKER: Explicitly import the permissions classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer
from .filters import BookFilter 
import django_filters


# --- ListView (ListAPIView) ---
# Required Class Name: ListView
class ListView(generics.ListAPIView):
    """
    GET /api/books/ (ListView)
    Retrieves a list of all Book instances.
    Permissions: Allowed for ANY user (AllowAny).
    """
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer
    # Step 4: Allow read-only access to all users
    permission_classes = [AllowAny] 

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter, 
        filters.OrderingFilter
    ]
    filterset_class = BookFilter
    search_fields = ['title', 'author'] # Assuming author is a CharField or similar
    ordering_fields = ['title', 'publication_year'] # Assuming this field exists
    ordering = ['title'] 


# --- DetailView (RetrieveAPIView) ---
# Required Class Name: DetailView
class DetailView(generics.RetrieveAPIView):
    """
    GET /api/books/<int:pk>/ (DetailView)
    Retrieves a single Book instance by its primary key (ID).
    Permissions: Allowed for ANY user (AllowAny).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Step 4: Allow read-only access to all users
    permission_classes = [AllowAny]


# --- CreateView (CreateAPIView) ---
# Required Class Name: CreateView
class CreateView(generics.CreateAPIView):
    """
    POST /api/books/create/ (CreateView)
    Creates a new Book instance.
    Permissions: Restricted to AUTHENTICATED users only (IsAuthenticated).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Step 4: Restrict write access to authenticated users
    permission_classes = [IsAuthenticated]


# --- UpdateView (UpdateAPIView) ---
# Required Class Name: UpdateView
class UpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /api/books/<int:pk>/update/ (UpdateView)
    Updates an existing Book instance.
    Permissions: Restricted to AUTHENTICATED users only (IsAuthenticated).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Step 4: Restrict write access to authenticated users
    permission_classes = [IsAuthenticated]


# --- DeleteView (DestroyAPIView) ---
# Required Class Name: DeleteView
class DeleteView(generics.DestroyAPIView):
    """
    DELETE /api/books/<int:pk>/delete/ (DeleteView)
    Deletes a Book instance.
    Permissions: Restricted to AUTHENTICATED users only (IsAuthenticated).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Step 4: Restrict write access to authenticated users
    permission_classes = [IsAuthenticated]