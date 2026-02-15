# app/models/book_queries.py

def create_book(conn, title, author, category, isbn, total_copies):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO books (title, author, category, isbn, total_copies, available_copies)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING book_id
        """, (title, author, category, isbn, total_copies, total_copies))
        return cur.fetchone()[0]


def get_book_by_id(conn, book_id):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT book_id, title, available_copies, total_copies
            FROM books
            WHERE book_id = %s AND is_active = TRUE
        """, (book_id,))
        return cur.fetchone()


def search_books(conn, keyword):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT book_id, title, author, category
            FROM books
            WHERE is_active = TRUE
            AND (title ILIKE %s OR author ILIKE %s)
        """, (f"%{keyword}%", f"%{keyword}%"))
        return cur.fetchall()


def update_book_copies(conn, book_id, new_available):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE books
            SET available_copies = %s
            WHERE book_id = %s
        """, (new_available, book_id))
