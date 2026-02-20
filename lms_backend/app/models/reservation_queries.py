# app/models/reservation_queries.py

from datetime import datetime, timedelta
from psycopg2.extras import RealDictCursor

# =====================================================
# CREATE RESERVATION
# =====================================================
def create_reservation(conn, user_id, book_id, expiry_days=3):
    """
    Create a new reservation for a user with optional expiry (default 3 days).
    Returns reservation_id.
    """
    expiry_date = datetime.utcnow() + timedelta(days=expiry_days)
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO reservations (user_id, book_id, reservation_date, expiry_date, reservation_status)
            VALUES (%s, %s, NOW(), %s, 'ACTIVE')
            RETURNING reservation_id
        """, (user_id, book_id, expiry_date))
        result = cur.fetchone()
        return result["reservation_id"] if result else None


# =====================================================
# GET OLDEST ACTIVE RESERVATION (FOR AUTO-ASSIGN)
# =====================================================
def get_oldest_active_reservation(conn, book_id):
    """
    Fetch the oldest ACTIVE reservation for a book.
    Uses FOR UPDATE to prevent race conditions during auto-assign.
    Returns reservation dict or None.
    """
    with conn.cursor() as cur:
        cur.execute("""
            SELECT reservation_id, user_id
            FROM reservations
            WHERE book_id = %s
              AND reservation_status = 'ACTIVE'
            ORDER BY reservation_date ASC
            LIMIT 1
            FOR UPDATE
        """, (book_id,))
        return cur.fetchone()


# =====================================================
# MARK RESERVATION FULFILLED
# =====================================================
def mark_reservation_fulfilled(conn, reservation_id):
    """
    Mark a reservation as FULFILLED.
    """
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE reservations
            SET reservation_status = 'FULFILLED'
            WHERE reservation_id = %s
        """, (reservation_id,))
        # commit handled by service layer


# =====================================================
# EXPIRE OVERDUE RESERVATIONS
# =====================================================
def get_all_reservations(conn, limit=100, offset=0):
    """Admin: list all reservations with user and book info."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT r.reservation_id, r.user_id, r.book_id, r.reservation_date, r.expiry_date, r.reservation_status,
                   u.name as user_name, u.email, bk.title as book_title, bk.author
            FROM reservations r
            JOIN users u ON r.user_id = u.user_id
            JOIN books bk ON r.book_id = bk.book_id
            ORDER BY r.reservation_date DESC
            LIMIT %s OFFSET %s
        """, (limit, offset))
        return cur.fetchall()


def get_user_reservations(conn, user_id):
    """Get reservations for a user (own active reservations)."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT r.*, bk.title, bk.author
            FROM reservations r
            JOIN books bk ON r.book_id = bk.book_id
            WHERE r.user_id = %s
            ORDER BY r.reservation_date DESC
        """, (user_id,))
        return cur.fetchall()


def expire_overdue_reservations(conn):
    """
    Expires reservations where expiry_date has passed and status is still ACTIVE.
    Can be called periodically or before issuing a book.
    """
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE reservations
            SET reservation_status = 'EXPIRED'
            WHERE reservation_status = 'ACTIVE'
              AND expiry_date IS NOT NULL
              AND expiry_date < NOW()
        """)
        # commit handled by service layer
