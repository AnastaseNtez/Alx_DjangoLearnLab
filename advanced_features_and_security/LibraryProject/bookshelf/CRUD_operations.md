from bookshelf.models import Book

# 1. CREATE
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# 2. RETRIEVE
retrieved_book = Book.objects.get(title="1984")

# 3. UPDATE
retrieved_book.title = "Nineteen Eighty-Four"
retrieved_book.save()

# 4. DELETE
# Retrieve the book using the updated title
book_to_delete = Book.objects.get(title="Nineteen Eighty-Four")
book_to_delete.delete()

# 5. VERIFY DELETION
Book.objects.all()