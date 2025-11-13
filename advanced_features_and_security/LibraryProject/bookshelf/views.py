from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q 
from .models import Book 
from .forms import ExampleForm # <--- NEW: Import the ExampleForm

# --- Core Views for Permission Testing ---
APP_LABEL = 'bookshelf'

@login_required # Requires login, but checks for permission manually
def book_list_view(request):
    """
    Checks for the can_view permission manually and safely handles user input (search).
    This function demonstrates SQL Injection prevention via the ORM.
    """
    if not request.user.has_perm(f'{APP_LABEL}.can_view'):
        raise PermissionDenied("You do not have permission to view the book list.")

    # --- SQL INJECTION PREVENTION DEMONSTRATION ---
    search_query = request.GET.get('q', '').strip() 
    
    if search_query:
        # Q objects allow complex 'OR' lookups across fields
        books = Book.objects.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(description__icontains=search_query)
        )
        context = {
            'search_query': search_query,
            'books_count': books.count(),
            'message': f"Found {books.count()} books matching '{search_query}'.",
        }
        return render(request, 'book_list.html', context)
    
    context = {
        'search_query': None,
        'books_count': Book.objects.count(),
        'message': "You can see the list of all books (no search applied)."
    }
    return render(request, 'book_list.html', context)
    # --- END SQL INJECTION PREVENTION DEMO ---


# --- NEW VIEW FOR FORM DEMONSTRATION (XSS and Validation) ---
def form_submit_view(request):
    """
    Handles form submission using Django Forms for robust validation and XSS prevention.
    """
    submission_result = None
    
    if request.method == 'POST':
        # 1. Bind POST data to the form
        form = ExampleForm(request.POST)
        
        # 2. Validate the data
        if form.is_valid():
            # Data is clean, validated, and safe from XSS.
            submission_result = form.cleaned_data
            
            # Re-render the page with the success message/result
            # We pass a new empty form and the submission result
            return render(request, 'form_example.html', {'form': ExampleForm(), 'submission_result': submission_result})
        # If not valid, the form object now contains error messages for display.
    else:
        # Create an empty form for GET request
        form = ExampleForm() 

    # Render the template, passing the form (either empty or with errors)
    return render(request, 'form_example.html', {'form': form})
# --- END NEW VIEW ---


# --- CRUD Views using Decorators (unchanged) ---

@permission_required(f'{APP_LABEL}.can_create', raise_exception=True)
def book_create_view(request):
    """
    Protected by the 'can_create' permission.
    """
    return HttpResponse("<h1>Book Creation Form (CREATE Permission Required)</h1><p>Access Granted: You can create a new book.</p>")


@permission_required(f'{APP_LABEL}.can_edit', raise_exception=True)
def book_edit_view(request, book_id):
    """
    Protected by the 'can_edit' permission.
    """
    return HttpResponse(f"<h1>Editing Book ID {book_id} (EDIT Permission Required)</h1><p>Access Granted: You can modify this book.</p>")


@permission_required(f'{APP_LABEL}.can_delete', raise_exception=True)
def book_delete_view(request, book_id):
    """
    Protected by the 'can_delete' permission.
    """
    return HttpResponse(f"<h1>Deleting Book ID {book_id} (DELETE Permission Required)</h1><p>Access Granted: You can delete this book.</p>")