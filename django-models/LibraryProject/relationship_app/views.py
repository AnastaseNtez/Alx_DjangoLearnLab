
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from .models import Library, Book
from django.contrib.auth import login
from .forms import CustomUserCreationForm # <-- Import the new form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test # <-- NEW IMPORT
from .models import Book, Library, UserProfile # <-- NEW IMPORT

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

# --- New View: User Registration (FBV) ---
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in immediately after successful registration
            login(request, user) 
            # Redirect to a success page (e.g., the book list)
            return redirect('list_books') 
    else:
        form = CustomUserCreationForm()
        
    # Render the provided register.html template
    return render(request, 'relationship_app/register.html', {'form': form})

# --- Role Check Helper Functions ---
def is_admin(user):
    return user.is_authenticated and user.userprofile.role == UserProfile.ROLE_ADMIN

def is_librarian(user):
    return user.is_authenticated and user.userprofile.role == UserProfile.ROLE_LIBRARIAN

def is_member(user):
    return user.is_authenticated and user.userprofile.role == UserProfile.ROLE_MEMBER

# --- Role-Based Views ---
@user_passes_test(is_admin)
def admin_view(request):
    """View accessible only to Admin users."""
    # Renders the admin_view.html template
    return render(request, 'relationship_app/admin_view.html', {'message': 'Welcome, Admin!'})

@user_passes_test(is_librarian)
def librarian_view(request):
    """View accessible only to Librarian users."""
    # Renders the librarian_view.html template
    return render(request, 'relationship_app/librarian_view.html', {'message': 'Welcome, Librarian!'})

@user_passes_test(is_member)
def member_view(request):
    """View accessible only to Member users."""
    # Renders the member_view.html template
    return render(request, 'relationship_app/member_view.html', {'message': 'Welcome, Member!'})