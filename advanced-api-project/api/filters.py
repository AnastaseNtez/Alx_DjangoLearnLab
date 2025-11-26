# api/filters.py

import django_filters
from .models import Book

# Purpose: Defines the specific fields and lookup types available for filtering the Book model.
class BookFilter(django_filters.FilterSet):
    # Allows filtering by books published in or after a specific year.
    publication_year_gte = django_filters.NumberFilter(field_name='publication_year', lookup_expr='gte')

    class Meta:
        model = Book
        # Allows exact filtering on title, author, and publication_year
        fields = {
            'title': ['exact', 'icontains'],
            # Note: Filtering by the ForeignKey field 'author' requires using the field name 'author__name'
            # to filter by the author's name, not the author's ID (pk).
            'author__name': ['exact', 'icontains'], 
            'publication_year': ['exact', 'gte', 'lte'],
        }