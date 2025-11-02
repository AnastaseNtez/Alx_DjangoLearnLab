from django.db import models

# Create your models here.

# Define the Book model as specified in the task description.
class Book(models.Model):
    """
    Represents a single book in the library.
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        """Returns a string representation of the book (Title by Author)."""
        return f"{self.title} by {self.author}"

