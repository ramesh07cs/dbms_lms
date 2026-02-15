# app/services/borrow_service.py

from datetime import datetime, timedelta
from app.models.book_queries import get_book_by_id, update_book_copies
from app.models.borrow_queries import create_borrow, get_active_borrow, return_book


def issue_book(conn, user_id, book_id):
    book = get_book_by_id(conn, book_id)

    if not book:
        raise ValueError("Book not found")

    book_id, title, available_copies, total_copies = book

    if available_copies <= 0:
        raise ValueError("Book not available")

    existing = get_active_borrow(conn, user_id, book_id)
    if existing:
        raise ValueError("User already borrowed this book")

    due_date = datetime.now() + timedelta(days=7)

    borrow_id = create_borrow(conn, user_id, book_id, due_date)

    update_book_copies(conn, book_id, available_copies - 1)

    return borrow_id


def return_borrowed_book(conn, user_id, book_id):
    active = get_active_borrow(conn, user_id, book_id)

    if not active:
        raise ValueError("No active borrow found")

    borrow_id = active[0]

    return_book(conn, borrow_id)

    book = get_book_by_id(conn, book_id)
    _, _, available_copies, _ = book

    update_book_copies(conn, book_id, available_copies + 1)
