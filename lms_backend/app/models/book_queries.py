# app/models/book_queries.py

def create_book(conn, title, author, category, isbn, total_copies):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO books (title, author, category, isbn, total_copies, available_copies)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING book_id
        """, (title, author, category, isbn, total_copies, total_copies))
        
        result = cur.fetchone()
        return result['book_id'] if result else None

def get_book_by_id(conn, book_id):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT book_id, title, author, category, isbn, total_copies, available_copies
            FROM books
            WHERE book_id = %s AND is_active = TRUE
        """, (book_id,))
        return cur.fetchone()

def update_book_copies(conn, book_id, new_available_count):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE books
            SET available_copies = %s
            WHERE book_id = %s
        """, (new_available_count, book_id))
        # Ensure changes are saved to the DB
        conn.commit()

def get_all_books(conn):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT book_id, title, author, category, isbn, total_copies, available_copies
            FROM books
            WHERE is_active = TRUE
        """)
        # Returns a list of dictionaries
        return cur.fetchall()