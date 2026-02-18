# app/services/borrow_service.py
from datetime import datetime, timedelta
from app.models.book_queries import get_book_by_id, update_book_copies
from app.models.borrow_queries import create_borrow, get_active_borrow, return_book_record

def issue_book(conn, user_id, book_id):
    """
    Issues a book to a user.
    Checks available copies and prevents double borrowing.
    """
    print("issue_book called with:", user_id, book_id)

    # Validate book_id
    try:
        book_id = int(book_id)
    except ValueError:
        raise ValueError("Invalid book_id")

    # Check book exists
    book = get_book_by_id(conn, book_id)
    if not book:
        raise ValueError("Book not found")
    if book['available_copies'] <= 0:
        raise ValueError("Book not available")

    # Check if user already borrowed this book
    existing = get_active_borrow(conn, user_id, book_id)
    if existing:
        raise ValueError("User already borrowed this book")

    # Calculate due date
    due_date = datetime.now() + timedelta(days=7)

    # Reduce available copies
    update_book_copies(conn, book_id, book['available_copies'] - 1)

    # Create borrow record
    borrow_id = create_borrow(conn, user_id, book_id, due_date)
    if not borrow_id:
        raise Exception("Failed to issue book")

    # Commit transaction
    conn.commit()
    print("Book issued successfully, borrow_id:", borrow_id)
    return borrow_id


def return_borrowed_book(conn, user_id, book_id):
    """
    Returns a borrowed book and updates available copies.
    """
    print("return_borrowed_book called with:", user_id, book_id)

    # Validate book_id
    try:
        book_id = int(book_id)
    except ValueError:
        raise ValueError("Invalid book_id")

    # Find active borrow
    active = get_active_borrow(conn, user_id, book_id)
    if not active:
        raise ValueError("No active borrow found for this book")

    borrow_id = active['borrow_id']

    # Update borrow record as returned
    return_book_record(conn, borrow_id)

    # Update book copies
    book = get_book_by_id(conn, book_id)
    if book:
        update_book_copies(conn, book_id, book['available_copies'] + 1)

    # Commit transaction
    conn.commit()
    print("Book returned successfully, borrow_id:", borrow_id)
