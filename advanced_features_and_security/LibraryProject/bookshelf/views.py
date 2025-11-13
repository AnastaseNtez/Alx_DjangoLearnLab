from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q # <--- CRITICAL: Imports Q object for safe search
from .models import Book # <--- CRITICAL: Imports the Book model

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
    search_query = request.GET.get('q', '').strip() # Safely get user input and sanitize with .strip()
    
    # Use Django's ORM to parameterize the query (prevents SQL Injection)
    if search_query:
        # Q objects allow complex 'OR' lookups across fields
        books = Book.objects.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(description__icontains=search_query)
        )
        return HttpResponse(f"<h1>Book List (VIEW Permission Required)</h1><p>Access Granted: Found {books.count()} books matching '{search_query}'.</p>")
    # --- END SQL INJECTION PREVENTION DEMO ---

    return HttpResponse("<h1>Book List (VIEW Permission Required)</h1><p>Access Granted: You can see the list of all books.</p>")


# --- CRUD Views using Decorators ---

@permission_required(f'{APP_LABEL}.can_create', raise_exception=True)
def book_create_view(request):
    """
    Protected by the 'can_create' permission.
    """
    # NOTE: In a real app, form validation (using Django Forms) is the primary
    # way to sanitize and validate all POST data, preventing XSS and injection via input.
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