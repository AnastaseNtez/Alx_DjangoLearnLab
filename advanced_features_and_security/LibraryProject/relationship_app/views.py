from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied

# --- Core Views for Permission Testing (Step 3) ---

@login_required # Requires login, but no specific permission
def book_list_view(request):
    """
    Checks for the can_view permission manually.
    """
    if not request.user.has_perm('relationship_app.can_view'):
        raise PermissionDenied("You do not have permission to view the book list.")

    return HttpResponse("<h1>Book List (VIEW Permission Required)</h1><p>Access Granted: You can see the list of all books.</p>")


# --- CRUD Views using Decorators (Step 3) ---

@permission_required('relationship_app.can_create', raise_exception=True)
def book_create_view(request):
    """
    Protected by the 'can_create' permission.
    """
    return HttpResponse("<h1>Book Creation Form (CREATE Permission Required)</h1><p>Access Granted: You can create a new book.</p>")


@permission_required('relationship_app.can_edit', raise_exception=True)
def book_edit_view(request, book_id):
    """
    Protected by the 'can_edit' permission.
    """
    return HttpResponse(f"<h1>Editing Book ID {book_id} (EDIT Permission Required)</h1><p>Access Granted: You can modify this book.</p>")


@permission_required('relationship_app.can_delete', raise_exception=True)
def book_delete_view(request, book_id):
    """
    Protected by the 'can_delete' permission.
    """
    return HttpResponse(f"<h1>Deleting Book ID {book_id} (DELETE Permission Required)</h1><p>Access Granted: You can delete this book.</p>")