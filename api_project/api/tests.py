from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .models import Book
import json

class BookAPITestCase(TestCase):
    """
    Tests the functionality of the BookList API endpoint (/api/books/).
    """

    def setUp(self):
        """
        Set up necessary data for the tests: create two sample Book objects.
        
        NOTE: This now only uses the 'title' and 'author' fields 
        as defined in api/models.py.
        """
        self.book1 = Book.objects.create(
            title="The Martian Chronicles",
            author="Ray Bradbury",
        )
        self.book2 = Book.objects.create(
            title="Dune",
            author="Frank Herbert",
        )
        # The URL is reversed using the app namespace 'api' and the path name 'book-list'
        self.url = reverse('api:book-list')
        print(f"Testing URL: {self.url}")


    def test_book_list_endpoint_status(self):
        """
        Ensure the GET request to /api/books/ returns a 200 OK status code.
        """
        response = self.client.get(self.url)
        # Check if the HTTP status is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_list_endpoint_content(self):
        """
        Ensure the GET request returns the correct number of items and the correct data.
        """
        response = self.client.get(self.url)
        
        # Parse the JSON response content
        # Note: DRF may return a bytes object, so we decode it.
        response_data = json.loads(response.content)

        # 1. Check if the response contains the correct number of books
        self.assertEqual(len(response_data), 2)
        
        # 2. Check the data integrity (titles and authors)
        titles = [item['title'] for item in response_data]
        self.assertIn("The Martian Chronicles", titles)
        self.assertIn("Dune", titles)

        # 3. Check specific field content for one of the books
        dune_book = next(item for item in response_data if item['title'] == 'Dune')
        self.assertEqual(dune_book['author'], 'Frank Herbert')
        # We only check for the fields defined in the model: 'id', 'title', 'author'