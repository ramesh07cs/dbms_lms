from app.models.book_queries import (
    create_book,
    get_book_by_id,
    get_all_books  # Added for completeness
)

def add_book(conn, title, author, category, isbn, total_copies):
    """
    Handles the logic for adding a new book to the system.
    """
    # Validation logic
    if total_copies <= 0:
        raise ValueError("Total copies must be positive")

    # Pass the data to the query function.
    # create_book should return the new book_id directly.
    return create_book(conn, title, author, category, isbn, total_copies)


def get_book_details(conn, book_id):
    """
    Retrieves a single book and ensures it is handled as a dictionary.
    """
    book = get_book_by_id(conn, book_id)
    
    if not book:
        raise ValueError("Book not found")
        
    # Because of RealDictCursor, 'book' is a dictionary.
    # We can access values safely like this:
    # title = book['title'] 
    
    return book