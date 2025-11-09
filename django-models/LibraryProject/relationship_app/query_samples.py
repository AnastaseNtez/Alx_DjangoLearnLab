from relationship_app.models import Author, Book, Library, Librarian

# Query 1: Query all books by a specific author
def books_by_author(author_name):
    """
    Retrieve all books written by a specific author.
    """
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return None


# Query 2: List all books in a library
def books_in_library(library_name):
    """
    List all books available in a specific library.
    """
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return None


# --- Query 3: Retrieve the librarian for a library (OneToOneField lookup) ---
def librarian_for_library(library_name):
    """Retrieve the librarian associated with a specific library."""
    try:
        # spanning relationship lookup (library__name) to filter the Librarian
        
        librarian = Librarian.objects.get(library__name=library_name)
        return librarian
    except Librarian.DoesNotExist:
        # This catches if the library name doesn't exist or if a librarian is not assigned
        return None