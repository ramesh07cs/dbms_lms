# app/services/book_service.py

from app.models.book_queries import (
    create_book,
    get_book_by_id
)


def add_book(conn, title, author, category, isbn, total_copies):
    if total_copies <= 0:
        raise ValueError("Total copies must be positive")

    return create_book(conn, title, author, category, isbn, total_copies)
