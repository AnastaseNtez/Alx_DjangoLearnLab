from django.contrib import admin

from .models import Book

# Define the custom configuration for the Book model
class BookAdmin(admin.ModelAdmin):
    # 1. Implement custom configurations to display fields in the list view (list_display)
    list_display = ('title', 'author', 'publication_year')

    # 2. Configure list filters (list_filter)
    list_filter = ('author', 'publication_year')

    # 3. Configure search capabilities (search_fields) - searches based on the provided fields
    search_fields = ('title', 'author')

# Register your model with the custom configuration
admin.site.register(Book, BookAdmin)

