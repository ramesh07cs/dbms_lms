# app/models/fine_queries.py
from psycopg2.extras import RealDictCursor


def insert_fine(conn, borrow_id, user_id, amount):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO fines (borrow_id, user_id, amount, paid_status, created_at)
            VALUES (%s, %s, %s, FALSE, NOW())
            RETURNING fine_id
        """, (borrow_id, user_id, amount))
        return cur.fetchone()


def get_user_unpaid_fines(conn, user_id, limit=20, offset=0):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT *
            FROM fines
            WHERE user_id = %s AND paid_status = FALSE
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """, (user_id, limit, offset))
        return cur.fetchall()


def get_user_fines_with_book(conn, user_id, limit=50, offset=0):
    """All fines for user with book title (for My Fines page)."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT f.fine_id, f.borrow_id, f.amount, f.paid_status, f.paid_date, f.created_at,
                   bk.title AS book_title
            FROM fines f
            JOIN borrows b ON b.borrow_id = f.borrow_id
            JOIN books bk ON bk.book_id = b.book_id
            WHERE f.user_id = %s
            ORDER BY f.created_at DESC
            LIMIT %s OFFSET %s
        """, (user_id, limit, offset))
        return cur.fetchall()


def mark_fine_paid(conn, fine_id):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE fines
            SET paid_status = TRUE,
                paid_date = NOW()
            WHERE fine_id = %s
            RETURNING fine_id
        """, (fine_id,))
        return cur.fetchone()


def get_all_fines(conn, limit=20, offset=0):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT *
            FROM fines
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """, (limit, offset))
        return cur.fetchall()
