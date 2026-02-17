from datetime import datetime, timedelta
from flask import g
from app.models.book_queries import get_book_by_id, update_book_copies
from app.models.borrow_queries import (
    create_borrow,
    get_active_borrow,
    return_book_record
)


def issue_book(user_id, book_id):
    conn = g.db

    try:
        book = get_book_by_id(conn, book_id)

        if not book:
            raise ValueError("Book not found")

        if book['available_copies'] <= 0:
            raise ValueError("Book not available")

        existing = get_active_borrow(conn, user_id, book_id)
        if existing:
            raise ValueError("User already borrowed this book")

        due_date = datetime.now() + timedelta(days=7)

        # Step 1: reduce copies first
        update_book_copies(
            conn,
            book_id,
            book['available_copies'] - 1
        )

        # Step 2: create borrow record
        borrow_id = create_borrow(conn, user_id, book_id, due_date)

        conn.commit()
        return borrow_id

    except Exception:
        conn.rollback()
        raise


def return_borrowed_book(user_id, book_id):
    conn = g.db

    try:
        active = get_active_borrow(conn, user_id, book_id)

        if not active:
            raise ValueError("No active borrow found")

        borrow_id = active['borrow_id']

        # Update borrow record
        return_book_record(conn, borrow_id)

        # Increase book copies
        book = get_book_by_id(conn, book_id)
        if book:
            update_book_copies(
                conn,
                book_id,
                book['available_copies'] + 1
            )

        conn.commit()

    except Exception:
        conn.rollback()
        raise
