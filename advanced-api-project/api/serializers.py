from rest_framework import serializers
from django.utils import timezone
from .models import Author, Book

# BookSerializer
# Purpose: Handles serialization and deserialization for the Book model.
# Includes custom validation to ensure publication year is not in the future.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        # Serialize all fields from the Book model.
        fields = ['id', 'title', 'publication_year', 'author']
        
    # Custom Validation Requirement: Ensure publication_year is not in the future.
    def validate_publication_year(self, value):
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(f"Publication year cannot be in the future ({current_year}).")
        return value

# AuthorSerializer
# Purpose: Handles serialization for the Author model.
# Features: It uses a nested BookSerializer to include the related books, 
# demonstrating how to handle one-to-many relationships in DRF.
class AuthorSerializer(serializers.ModelSerializer):
    # Relationship Handling: 
    # This field uses the related_name='books' from the Book model's ForeignKey 
    # to retrieve all related books for a given author.
    # The nested BookSerializer is used to format these related book objects.
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        # Serialize the 'name' field and the nested 'books' list.
        fields = ['id', 'name', 'books']