from app.models.book_queries import (
    create_book,
    get_book_by_id,
    get_book_by_isbn,
    update_book_copies,
    update_book,
    soft_delete_book,
    get_all_books
)

def add_book(conn, title, author, isbn, total_copies, category=None, available_copies=None):
    try:
        if not title or not author or not isbn:
            raise ValueError("Title, Author and ISBN are required")
        if total_copies is None:
            raise ValueError("Total copies is required")

        total_copies = int(total_copies)
        if total_copies <= 0:
            raise ValueError("Total copies must be greater than 0")
        if available_copies is not None:
            avail = int(available_copies)
            if avail < 0 or avail > total_copies:
                raise ValueError("Available copies must be between 0 and total copies")

        existing = get_book_by_isbn(conn, isbn)
        if existing:
            raise ValueError("Book with this ISBN already exists")

        book_id = create_book(conn, title, author, isbn, total_copies, category, available_copies)
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


def update_book_details(conn, book_id, title=None, author=None, category=None, isbn=None, total_copies=None, available_copies=None):
    """Update book fields. Validates total_copies and available_copies."""
    book = get_book_by_id(conn, book_id)
    if not book:
        raise ValueError("Book not found")
    total = int(book["total_copies"]) if total_copies is None else int(total_copies)
    if total_copies is not None:
        if total < 0:
            raise ValueError("Total copies cannot be negative")
        borrowed = book["total_copies"] - book["available_copies"]
        if total < borrowed:
            raise ValueError("Total copies cannot be less than borrowed copies")
    if available_copies is not None:
        av = int(available_copies)
        if av < 0:
            raise ValueError("Available copies cannot be negative")
        if av > total:
            raise ValueError("Available copies cannot exceed total copies")
    try:
        update_book(conn, book_id, title, author, category, isbn, total_copies, available_copies)
        conn.commit()
    except Exception:
        conn.rollback()
        raise


def remove_book(conn, book_id):
    """Soft delete a book."""
    book = get_book_by_id(conn, book_id)
    if not book:
        raise ValueError("Book not found")
    if book["available_copies"] < book["total_copies"]:
        raise ValueError("Cannot delete book with active borrows")
    try:
        soft_delete_book(conn, book_id)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
