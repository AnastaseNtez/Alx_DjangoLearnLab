from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Inherits from ModelSerializer to automatically handle CRUD operations.
    """
    class Meta:
        # Link the serializer to the Book model
        model = Book
        
        # Explicitly list all fields, including the primary key 'id',
        # which is essential for the ViewSet to handle retrieval and updates/deletions.
        # It also ensures 'POST' requests are correctly processed.
        fields = ['id', 'title', 'author']