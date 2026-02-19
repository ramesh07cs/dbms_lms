from psycopg2.extras import RealDictCursor

def create_borrow(conn, user_id, book_id, due_date):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            INSERT INTO borrows (user_id, book_id, due_date, borrow_status)
            VALUES (%s, %s, %s, 'ISSUED')
            RETURNING borrow_id
        """, (user_id, book_id, due_date))
        result = cur.fetchone()
        if not result:
            return None
        return result['borrow_id']
        


def get_active_borrow(conn, user_id, book_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT borrow_id, user_id, book_id, due_date, borrow_status
            FROM borrows
            WHERE user_id = %s
              AND book_id = %s
              AND borrow_status = 'ISSUED'
        """, (user_id, book_id))
        return cur.fetchone()


def return_book_record(conn, borrow_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            UPDATE borrows
            SET return_date = CURRENT_TIMESTAMP,
                borrow_status = 'RETURNED'
            WHERE borrow_id = %s
        """, (borrow_id,))


def get_borrow_by_id(conn, borrow_id):
    """Get a borrow record by ID."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT b.*, bk.title, bk.author, u.name as user_name
            FROM borrows b
            JOIN books bk ON b.book_id = bk.book_id
            JOIN users u ON b.user_id = u.user_id
            WHERE b.borrow_id = %s
        """, (borrow_id,))
        return cur.fetchone()


def get_user_active_borrows(conn, user_id):
    """Get active borrows for a user (for return form)."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT b.borrow_id, b.book_id, b.issue_date, b.due_date, bk.title, bk.author
            FROM borrows b
            JOIN books bk ON b.book_id = bk.book_id
            WHERE b.user_id = %s AND b.borrow_status = 'ISSUED'
            ORDER BY b.due_date
        """, (user_id,))
        return cur.fetchall()


def get_user_borrow_history(conn, user_id, limit=50, offset=0):
    """Get borrow history for a user."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT b.borrow_id, b.book_id, b.issue_date, b.due_date, b.return_date, b.borrow_status,
                   bk.title, bk.author
            FROM borrows b
            JOIN books bk ON b.book_id = bk.book_id
            WHERE b.user_id = %s
            ORDER BY b.issue_date DESC
            LIMIT %s OFFSET %s
        """, (user_id, limit, offset))
        return cur.fetchall()


def get_all_active_borrows(conn):
    """Get all active (ISSUED) borrows for admin."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT b.borrow_id, b.user_id, b.book_id, b.issue_date, b.due_date,
                   bk.title, bk.author, u.name as user_name, u.email
            FROM borrows b
            JOIN books bk ON b.book_id = bk.book_id
            JOIN users u ON b.user_id = u.user_id
            WHERE b.borrow_status = 'ISSUED'
            ORDER BY b.due_date
        """)
        return cur.fetchall()
