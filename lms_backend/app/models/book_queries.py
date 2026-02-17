from psycopg2.extras import RealDictCursor


def create_book(conn, title, author, isbn, total_copies):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """
            INSERT INTO books (title, author, isbn, total_copies, available_copies)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING book_id;
            """,
            (title, author, isbn, total_copies, total_copies)
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
