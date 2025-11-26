# api/test_views.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Author, Book

# Define the URLs we will be testing (using the names defined in api/urls.py)
LIST_CREATE_URL = reverse('book-list-create')
DETAIL_URL_NAME = 'book-detail-update-delete'

# Helper function to generate the detail URL for a specific book ID
def detail_url(book_id):
    return reverse(DETAIL_URL_NAME, args=[book_id])

class BookAPITests(APITestCase):
    """
    Base class for setting up test data and users.
    """
    def setUp(self):
        # 1. Create a regular user for authenticated operations (WRITE access)
        self.user = User.objects.create_user(username='writer', password='password123')
        
        # 2. Create an Author instance
        self.author_tolkien = Author.objects.create(name="J.R.R. Tolkien")
        self.author_rowling = Author.objects.create(name="J.K. Rowling")

        # 3. Create initial Book instances
        self.book1 = Book.objects.create(
            title="The Hobbit", 
            publication_year=1937, 
            author=self.author_tolkien
        )
        self.book2 = Book.objects.create(
            title="Fellowship of the Ring", 
            publication_year=1954, 
            author=self.author_tolkien
        )
        self.book3 = Book.objects.create(
            title="Harry Potter and the Sorcerer's Stone",
            publication_year=1997,
            author=self.author_rowling
        )

        # Base data for creating a new book
        self.valid_payload = {
            'title': 'A New Book',
            'publication_year': 2020,
            'author': self.author_tolkien.id 
        }

# --- CRUD Operations Tests ---

class BookCRUDTests(BookAPITests):

    def test_list_books_unauthenticated(self):
        """Test listing all books works for unauthenticated users."""
        response = self.client.get(LIST_CREATE_URL)
        
        # Should succeed (Read-Only access is allowed)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that all 3 initial books are returned
        self.assertEqual(len(response.data), 3)

    def test_retrieve_book_detail(self):
        """Test retrieving a single book works."""
        response = self.client.get(detail_url(self.book1.id))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the title matches
        self.assertEqual(response.data['title'], self.book1.title)

    # --- Create (POST) Tests ---
    
    def test_create_book_unauthenticated_fails(self):
        """Test unauthenticated users cannot create a book (403 Forbidden)."""
        response = self.client.post(LIST_CREATE_URL, self.valid_payload)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Ensure book count didn't change
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_authenticated_success(self):
        """Test authenticated users can successfully create a book (201 Created)."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(LIST_CREATE_URL, self.valid_payload)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        # Check that the saved book data matches the payload
        self.assertEqual(Book.objects.get(id=response.data['id']).title, 'A New Book')

    def test_create_book_with_invalid_year_fails(self):
        """Test serializer validation prevents creating a book with a future publication year (400 Bad Request)."""
        self.client.force_authenticate(user=self.user)
        invalid_payload = self.valid_payload.copy()
        # Assume current year is 2025 (or check current year dynamically)
        invalid_payload['publication_year'] = 3000 
        
        response = self.client.post(LIST_CREATE_URL, invalid_payload)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check for the specific validation error message
        self.assertIn('Publication year cannot be in the future', str(response.data['publication_year']))

    # --- Update (PUT/PATCH) Tests ---

    def test_update_book_unauthenticated_fails(self):
        """Test unauthenticated users cannot update a book (403 Forbidden)."""
        update_payload = {'title': 'Updated Title', 'publication_year': 1990, 'author': self.author_tolkien.id}
        response = self.client.put(detail_url(self.book1.id), update_payload)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Ensure title was not changed
        self.assertEqual(Book.objects.get(id=self.book1.id).title, self.book1.title)

    def test_update_book_authenticated_success(self):
        """Test authenticated users can successfully update a book (200 OK)."""
        self.client.force_authenticate(user=self.user)
        updated_title = 'The Updated Hobbit'
        update_payload = {'title': updated_title, 'publication_year': 1937, 'author': self.author_tolkien.id}
        
        response = self.client.put(detail_url(self.book1.id), update_payload)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify the change was saved
        self.assertEqual(Book.objects.get(id=self.book1.id).title, updated_title)

    # --- Delete (DELETE) Tests ---

    def test_delete_book_unauthenticated_fails(self):
        """Test unauthenticated users cannot delete a book (403 Forbidden)."""
        response = self.client.delete(detail_url(self.book1.id))
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Ensure book still exists
        self.assertTrue(Book.objects.filter(id=self.book1.id).exists())

    def test_delete_book_authenticated_success(self):
        """Test authenticated users can successfully delete a book (204 No Content)."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(detail_url(self.book1.id))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Verify book is removed
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

# --- Query Functionality Tests (Filtering, Searching, Ordering) ---

class BookQueryTests(BookAPITests):

    def test_filter_by_publication_year(self):
        """Test filtering books by exact publication_year."""
        # Query for books published in 1937
        response = self.client.get(LIST_CREATE_URL, {'publication_year': 1937})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'The Hobbit')

    def test_filter_by_publication_year_gte(self):
        """Test filtering books by publication_year greater than or equal to (gte)."""
        # Query for books published in or after 1954 (should include book2 and book3)
        response = self.client.get(LIST_CREATE_URL, {'publication_year__gte': 1954})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Verify the two correct books are returned
        titles = {item['title'] for item in response.data}
        self.assertIn('Fellowship of the Ring', titles)
        self.assertIn("Harry Potter and the Sorcerer's Stone", titles)
        
    def test_filter_by_author_name(self):
        """Test filtering by author's name (foreign key lookup)."""
        # Query for books by J.K. Rowling
        response = self.client.get(LIST_CREATE_URL, {'author__name': 'J.K. Rowling'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Harry Potter and the Sorcerer's Stone")

    def test_search_by_title_or_author(self):
        # We will search for a term that appears in the Author's name for both Tolkien and Rowling, 
        # such as 'R.' or a common letter in their names. 
        # Using 'J.' will match 'J.R.R. Tolkien' (2 books) and 'J.K. Rowling' (1 book).
        search_term = 'J.'
        response = self.client.get(LIST_CREATE_URL, {'search': search_term})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # EXPECTED RESULT: All 3 books should be returned because all authors' names start with J.
        self.assertEqual(len(response.data), 3) 
        
        titles = {item['title'] for item in response.data}
        self.assertIn('Fellowship of the Ring', titles)
        self.assertIn("Harry Potter and the Sorcerer's Stone", titles)
        self.assertIn('The Hobbit', titles)
        

    def test_ordering_ascending(self):
        """Test ordering by title ascending (default ordering)."""
        response = self.client.get(LIST_CREATE_URL, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expected order: Fellowship, Harry Potter, Hobbit
        self.assertEqual(response.data[0]['title'], 'Fellowship of the Ring')
        self.assertEqual(response.data[-1]['title'], 'The Hobbit')

    def test_ordering_descending(self):
        """Test ordering by publication_year descending (newest first)."""
        response = self.client.get(LIST_CREATE_URL, {'ordering': '-publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expected order: Harry Potter (1997), Fellowship (1954), Hobbit (1937)
        self.assertEqual(response.data[0]['publication_year'], 1997)
        self.assertEqual(response.data[-1]['publication_year'], 1937)

# --- End of api/test_views.py ---