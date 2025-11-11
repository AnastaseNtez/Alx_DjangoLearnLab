from bookshelf.models import Book

# Command: Retrieve the book using the updated title
# (Using the title "Nineteen Eighty-Four" from the Update step)
book = Book.objects.get(title="Nineteen Eighty-Four")

# Command: Delete the book instance
book.delete()

# Verification Command: Retrieve all Book objects to confirm deletion
Book.objects.all() 
