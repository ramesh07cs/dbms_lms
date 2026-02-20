from psycopg2.extras import RealDictCursor

def create_borrow(conn, user_id, book_id, due_date):
    """Create an issued borrow (status ACTIVE). Used on approve or direct admin/teacher issue."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            INSERT INTO borrows (user_id, book_id, due_date, borrow_status)
            VALUES (%s, %s, %s, 'ACTIVE')
            RETURNING borrow_id
        """, (user_id, book_id, due_date))
        result = cur.fetchone()
        if not result:
            return None
        return result['borrow_id']


def create_borrow_request(conn, user_id, book_id):
    """Create a borrow request (status PENDING). No copy decrement until approval."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            INSERT INTO borrows (user_id, book_id, due_date, borrow_status)
            VALUES (%s, %s, CURRENT_TIMESTAMP + INTERVAL '7 days', 'PENDING')
            RETURNING borrow_id
        """, (user_id, book_id))
        result = cur.fetchone()
        if not result:
            return None
        return result['borrow_id']


def get_pending_borrows(conn):
    """Get all PENDING borrow requests for admin."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT b.borrow_id, b.user_id, b.book_id, b.borrow_status,
                   bk.title, bk.author, bk.available_copies,
                   u.name AS user_name, u.email, r.role_name
            FROM borrows b
            JOIN books bk ON b.book_id = bk.book_id
            JOIN users u ON b.user_id = u.user_id
            JOIN roles r ON u.role_id = r.role_id
            WHERE b.borrow_status = 'PENDING'
            ORDER BY b.borrow_id ASC
        """)
        return cur.fetchall()


def update_borrow_to_issued(conn, borrow_id, due_date):
    """Set borrow status to ACTIVE and set issue_date (used on approval)."""
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE borrows
            SET borrow_status = 'ACTIVE', issue_date = CURRENT_TIMESTAMP, due_date = %s
            WHERE borrow_id = %s
        """, (due_date, borrow_id))


def reject_borrow_record(conn, borrow_id):
    """Set borrow status to REJECTED."""
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE borrows SET borrow_status = 'REJECTED' WHERE borrow_id = %s
        """, (borrow_id,))
        


def get_active_borrow(conn, user_id, book_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT borrow_id, user_id, book_id, due_date, borrow_status
            FROM borrows
            WHERE user_id = %s
              AND book_id = %s
              AND borrow_status = 'ACTIVE'
        """, (user_id, book_id))
        return cur.fetchone()


def get_pending_borrow(conn, user_id, book_id):
    """Check for existing PENDING request for same user and book."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT borrow_id FROM borrows
            WHERE user_id = %s AND book_id = %s AND borrow_status = 'PENDING'
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
            WHERE b.user_id = %s AND b.borrow_status = 'ACTIVE'
            ORDER BY b.due_date
        """, (user_id,))
        return cur.fetchall()


def get_user_borrow_history(conn, user_id, limit=50, offset=0):
    """Get borrow history for a user, with fine amount if any."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT b.borrow_id, b.book_id, b.issue_date, b.due_date, b.return_date, b.borrow_status,
                   bk.title, bk.author,
                   f.amount AS fine_amount
            FROM borrows b
            JOIN books bk ON b.book_id = bk.book_id
            LEFT JOIN fines f ON f.borrow_id = b.borrow_id
            WHERE b.user_id = %s
            ORDER BY b.issue_date DESC
            LIMIT %s OFFSET %s
        """, (user_id, limit, offset))
        return cur.fetchall()


def get_all_active_borrows(conn):
    """Get all active (ACTIVE) borrows for admin."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT b.borrow_id, b.user_id, b.book_id, b.issue_date, b.due_date,
                   bk.title, bk.author, u.name as user_name, u.email
            FROM borrows b
            JOIN books bk ON b.book_id = bk.book_id
            JOIN users u ON b.user_id = u.user_id
            WHERE b.borrow_status = 'ACTIVE'
            ORDER BY b.due_date
        """)
        return cur.fetchall()


def get_all_borrows(conn):
    """Get all borrows with user name, role, book title, dates, status (for Borrow Management)."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT b.borrow_id, b.user_id, b.book_id, 
                   b.issue_date AS requested_date,
                   b.issue_date, b.due_date, b.return_date,
                   b.borrow_status,
                   bk.title AS book_title, bk.author, bk.available_copies,
                   u.name AS user_name, u.email,
                   r.role_name
            FROM borrows b
            JOIN books bk ON b.book_id = bk.book_id
            JOIN users u ON b.user_id = u.user_id
            JOIN roles r ON u.role_id = r.role_id
            ORDER BY b.borrow_id DESC
        """)
        return cur.fetchall()
