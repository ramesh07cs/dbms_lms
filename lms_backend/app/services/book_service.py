from app.models.book_queries import (
    create_book,
    get_book_by_id,
    get_book_by_isbn,
    update_book_copies,
    get_all_books
)

def add_book(conn, title, author, isbn, total_copies):
    try:
        if not title or not author or not isbn:
            raise ValueError("Title, Author and ISBN are required")
        if total_copies is None:
            raise ValueError("Total copies is required")

        total_copies = int(total_copies)
        if total_copies <= 0:
            raise ValueError("Total copies must be greater than 0")

        existing = get_book_by_isbn(conn, isbn)
        if existing:
            raise ValueError("Book with this ISBN already exists")

        book_id = create_book(conn, title, author, isbn, total_copies)
        conn.commit()
        return book_id

    except Exception:
        conn.rollback()
        raise


def fetch_book(conn, book_id):
    book = get_book_by_id(conn, book_id)
    if not book:
        raise ValueError("Book not found")
    return book


def fetch_all_books(conn):
    return get_all_books(conn)


def change_book_copies(conn, book_id, new_available_copies):
    try:
        book = get_book_by_id(conn, book_id)
        if not book:
            raise ValueError("Book not found")

        if new_available_copies < 0:
            raise ValueError("Available copies cannot be negative")
        if new_available_copies > book["total_copies"]:
            raise ValueError("Available copies cannot exceed total copies")

        update_book_copies(conn, book_id, new_available_copies)
        conn.commit()

    except Exception:
        conn.rollback()
        raise
