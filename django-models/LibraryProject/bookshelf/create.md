from bookshelf.models import Book

# Command
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# Expected Output (a simple representation of the created object)
# <Book: 1984 by George Orwell>