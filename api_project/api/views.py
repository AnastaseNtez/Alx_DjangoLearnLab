from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    API view to list all Book instances.
    
    Inherits from ListAPIView, which provides a read-only endpoint for 
    a collection of model instances.
    
    This view handles HTTP GET requests to retrieve the list of books.
    """
    
    # 1. Define the queryset: The data that should be returned by this view
    # In this case, it's all objects from the Book model.
    queryset = Book.objects.all()
    
    # 2. Define the serializer class: How the queryset data should be formatted
    # (i.e., converted from model instances to JSON).
    serializer_class = BookSerializer
