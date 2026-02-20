from psycopg2.extras import RealDictCursor


def create_book(conn, title, author, isbn, total_copies, category=None, available_copies=None):
    avail = int(available_copies) if available_copies is not None else int(total_copies)
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """
            INSERT INTO books (title, author, isbn, total_copies, available_copies, category)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING book_id;
            """,
            (title, author, isbn, total_copies, avail, category)
        )
        return cur.fetchone()["book_id"]


def get_book_by_id(conn, book_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "SELECT * FROM books WHERE book_id = %s AND is_active = TRUE;",
            (book_id,)
        )
        return cur.fetchone()


def get_book_by_isbn(conn, isbn):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "SELECT * FROM books WHERE isbn = %s;",
            (isbn,)
        )
        return cur.fetchone()


def update_book_copies(conn, book_id, new_available_copies):
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE books
            SET available_copies = %s
            WHERE book_id = %s AND is_active = TRUE;
            """,
            (new_available_copies, book_id)
        )


def get_all_books(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "SELECT * FROM books WHERE is_active = TRUE;"
        )
        return cur.fetchall()


def update_book(conn, book_id, title=None, author=None, category=None, isbn=None, total_copies=None, available_copies=None):
    """Update book fields. Only non-None fields are updated."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        updates = []
        params = []
        if title is not None:
            updates.append("title = %s")
            params.append(title)
        if author is not None:
            updates.append("author = %s")
            params.append(author)
        if category is not None:
            updates.append("category = %s")
            params.append(category)
        if isbn is not None:
            updates.append("isbn = %s")
            params.append(isbn)
        if total_copies is not None:
            updates.append("total_copies = %s")
            params.append(total_copies)
        if available_copies is not None:
            updates.append("available_copies = %s")
            params.append(available_copies)
        if not updates:
            return
        params.append(book_id)
        cur.execute(
            f"UPDATE books SET {', '.join(updates)} WHERE book_id = %s AND is_active = TRUE",
            params
        )


def soft_delete_book(conn, book_id):
    """Soft delete: set is_active = FALSE."""
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE books SET is_active = FALSE WHERE book_id = %s",
            (book_id,)
        )
