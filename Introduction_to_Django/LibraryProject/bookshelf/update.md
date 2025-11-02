from bookshelf.models import Book

# Command: Retrieve the book using the current title
book_to_update = Book.objects.get(title="1984") 

# Command: Change the title attribute
book_to_update.title = "Nineteen Eighty-Four"

# Command: Save the changes to the database
book_to_update.save()

# Verification Command: Print the updated title to confirm
print(book_to_update.title)

# Expected Documentation: The updated title.
# Nineteen Eighty-Four