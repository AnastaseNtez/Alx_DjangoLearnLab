from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer
from .filters import BookFilter 

# --- Step 1 & 4: ListView (Read-Only/Public) ---
# Maps to generics.ListAPIView
class ListView(generics.ListAPIView):
    """
    GET /api/books/ (ListView)
    Retrieves a list of all Book instances.
    Permissions: Allowed for ANY user (permissions.AllowAny).

    Documentation: This view is customized with advanced query features (filtering,
    searching, and ordering).
    """
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer
    # Step 4: Allow read-only access to all users
    permission_classes = [permissions.AllowAny] 

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = BookFilter
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author']
    ordering = ['title'] 


# --- Step 1 & 4: DetailView (Read-Only/Public) ---
# Maps to generics.RetrieveAPIView
class DetailView(generics.RetrieveAPIView):
    """
    GET /api/books/<int:pk>/ (DetailView)
    Retrieves a single Book instance by its primary key (ID).
    Permissions: Allowed for ANY user (permissions.AllowAny).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Step 4: Allow read-only access to all users
    permission_classes = [permissions.AllowAny]


# --- Step 1, 3, & 4: CreateView (Write Operations - Authenticated Only) ---
# Maps to generics.CreateAPIView
class CreateView(generics.CreateAPIView):
    """
    POST /api/books/create/ (CreateView)
    Creates a new Book instance.
    Permissions: Restricted to AUTHENTICATED users only (permissions.IsAuthenticated).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Step 4: Restrict write access to authenticated users
    permission_classes = [permissions.IsAuthenticated]


# --- Step 1, 3, & 4: UpdateView (Write Operations - Authenticated Only) ---
# Maps to generics.UpdateAPIView
class UpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /api/books/<int:pk>/update/ (UpdateView)
    Updates an existing Book instance.
    Permissions: Restricted to AUTHENTICATED users only (permissions.IsAuthenticated).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Step 4: Restrict write access to authenticated users
    permission_classes = [permissions.IsAuthenticated]


# --- Step 1, 3, & 4: DeleteView (Write Operations - Authenticated Only) ---
# Maps to generics.DestroyAPIView
class DeleteView(generics.DestroyAPIView):
    """
    DELETE /api/books/<int:pk>/delete/ (DeleteView)
    Deletes a Book instance.
    Permissions: Restricted to AUTHENTICATED users only (permissions.IsAuthenticated).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Step 4: Restrict write access to authenticated users
    permission_classes = [permissions.IsAuthenticated]