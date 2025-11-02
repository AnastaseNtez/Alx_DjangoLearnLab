from bookshelf.models import Book

# Command: Retrieve the book using the current title
book = Book.objects.get(title="1984")

# Command: Change the title attribute
book.title = "Nineteen Eighty-Four"

# Command: Save the changes to the database
book.save()

# Verification Command: Print the updated title to confirm
print(book.title)

# Expected Documentation: The updated title.
# Nineteen Eighty-Four