from datetime import datetime, timedelta
from app.models.book_queries import get_book_by_id, update_book_copies
from app.models.borrow_queries import create_borrow, get_active_borrow, return_book

def issue_book(conn, user_id, book_id):
    """
    Handles the logic for a user borrowing a book.
    """
    # Fetch book details - returns a dictionary due to RealDictCursor
    book = get_book_by_id(conn, book_id)

    if not book:
        raise ValueError("Book not found")

    # Access available_copies using the dictionary key
    available_copies = book['available_copies']

    # Now the comparison works because we are comparing int to int
    if available_copies <= 0:
        raise ValueError("Book not available")

    # Check if the user already has an active borrow for this specific book
    existing = get_active_borrow(conn, user_id, book_id)
    if existing:
        raise ValueError("User already borrowed this book")

    # Set return deadline (e.g., 7 days from now)
    due_date = datetime.now() + timedelta(days=7)

    # Create the borrow record and get the new ID
    borrow_id = create_borrow(conn, user_id, book_id, due_date)

    # Decrement the available copies in the books table
    update_book_copies(conn, book_id, available_copies - 1)

    return borrow_id


def return_borrowed_book(conn, user_id, book_id):
    """
    Handles the logic for a user returning a borrowed book.
    """
    # Find the active borrow record
    active = get_active_borrow(conn, user_id, book_id)

    if not active:
        raise ValueError("No active borrow found")

    # Access borrow_id using the dictionary key
    borrow_id = active['borrow_id']

    # Update the borrow record to 'RETURNED'
    return_book(conn, borrow_id)

    # Fetch book details to update the count
    book = get_book_by_id(conn, book_id)
    
    if book:
        available_copies = book['available_copies']
        # Increment the available copies
        update_book_copies(conn, book_id, available_copies + 1)