
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from .models import Library, Book

# --- 1. Function-Based View (FBV): List all books ---
def list_books(request):
    """Lists all books and their authors using a function-based view."""
    # Retrieve all Book objects from the database
    all_books = Book.objects.all().select_related('author')
    
    context = {
        'books': all_books,
        'view_type': 'Function-Based View'
    }
    
    # Renders the HTML template 'list_books.html'
    return render(request, 'relationship_app/list_books.html', context)


# --- 2. Class-Based View (CBV): Library Detail ---
class LibraryDetailView(DetailView):
    """Displays details for a specific library, including its books."""
    # 1. Specify the model to retrieve the object from
    model = Library
    
    # 2. Specify the name of the template to render
    template_name = 'relationship_app/library_detail.html'
    
    # 3. Specify the context object name used in the template (default is 'object')
    context_object_name = 'library'
    
    # 4. By default, DetailView looks for an object using the 'pk' URL parameter.
    #    ll use a specific field for lookup in the URLs.
    #    We don't need to specify this here, but we will in urls.py.

    # Note: The template 'library_detail.html' uses library.books.all, 
    # which automatically handles the Many-to-Many relationship.
