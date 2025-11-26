from django.db import models

# Create your models here.
from django.db import models

# Model for an Author
# Purpose: Stores information about the authors.
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Model for a Book
# Purpose: Stores book details and links each book to a specific Author 
# via a ForeignKey, creating a one-to-many relationship (one Author can have many Books).
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    # The 'related_name' allows accessing books from an Author instance (e.g., author.books.all())
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return f"{self.title} ({self.publication_year})"