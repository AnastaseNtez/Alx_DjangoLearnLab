from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    """
    Converts Book model instances to JSON format and handles validation 
    for incoming data.
    """
    class Meta:
        # 1. Specify the model to serialize
        model = Book
        
        # 2. Specify the fields to be included in the serialized output
        # 'id' is automatically added by Django and is good to include.
        fields = ['id', 'title', 'author']