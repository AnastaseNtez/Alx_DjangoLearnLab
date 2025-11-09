from bookshelf.models import Book

# Command to retrieve the book by its title ("1984")
retrieved_book = Book.objects.get(title="1984")
# Command to display the key attributes
print(f"ID: {retrieved_book.id}, Title: {retrieved_book.title}, Author: {retrieved_book.author}, Year: {retrieved_book.publication_year}")

# Expected Documentation: The output showing the details of the book.
# The ID will be database-assigned, but the data must match the creation step.
# ID: 1, Title: 1984, Author: George Orwell, Year: 1949