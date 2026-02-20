"""Stats/dashboard queries for LMS."""
from datetime import datetime, timedelta
from psycopg2.extras import RealDictCursor


def get_admin_stats(conn):
    """Total issued, available books, students, teachers, fine collected."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT
                (SELECT COUNT(*) FROM borrows WHERE borrow_status = 'ACTIVE') AS total_issued_books,
                (SELECT COALESCE(SUM(available_copies), 0)::int FROM books WHERE is_active = TRUE) AS total_available_books,
                (SELECT COUNT(*) FROM users WHERE role_id = 3 AND status = 'APPROVED') AS total_students,
                (SELECT COUNT(*) FROM users WHERE role_id = 2 AND status = 'APPROVED') AS total_teachers,
                (SELECT COALESCE(SUM(amount), 0) FROM fines WHERE paid_status = TRUE) AS total_fine_collected
        """)
        return cur.fetchone()


def get_teacher_stats(conn, user_id):
    """Issued books count, due today, overdue for teacher."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT COUNT(*) AS issued_count
            FROM borrows WHERE user_id = %s AND borrow_status = 'ACTIVE'
        """, (user_id,))
        issued = cur.fetchone()["issued_count"]

        cur.execute("""
            SELECT b.borrow_id, b.book_id, b.due_date, bk.title, bk.author
            FROM borrows b
            JOIN books bk ON b.book_id = bk.book_id
            WHERE b.user_id = %s AND b.borrow_status = 'ACTIVE'
              AND b.due_date::date = CURRENT_DATE
            ORDER BY b.due_date
        """, (user_id,))
        due_today = cur.fetchall()

        cur.execute("""
            SELECT b.borrow_id, b.book_id, b.due_date, bk.title, bk.author
            FROM borrows b
            JOIN books bk ON b.book_id = bk.book_id
            WHERE b.user_id = %s AND b.borrow_status = 'ACTIVE'
              AND b.due_date < NOW()
            ORDER BY b.due_date
        """, (user_id,))
        overdue = cur.fetchall()

    return {
        "issued_count": issued,
        "due_today": due_today,
        "overdue": overdue,
    }


def get_student_stats(conn, user_id):
    """Currently borrowed, due soon, total fines, active reservations for student."""
    soon_days = 2
    soon_end = datetime.utcnow() + timedelta(days=soon_days)
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT COUNT(*) AS count FROM borrows WHERE user_id = %s AND borrow_status = 'ACTIVE'
        """, (user_id,))
        borrowed = cur.fetchone()["count"]

        cur.execute("""
            SELECT b.borrow_id, b.book_id, b.due_date, bk.title, bk.author
            FROM borrows b
            JOIN books bk ON b.book_id = bk.book_id
            WHERE b.user_id = %s AND b.borrow_status = 'ACTIVE'
              AND b.due_date >= NOW() AND b.due_date <= %s
            ORDER BY b.due_date
        """, (user_id, soon_end))
        due_soon = cur.fetchall()

        cur.execute("""
            SELECT COALESCE(SUM(amount), 0)::float AS total FROM fines WHERE user_id = %s AND paid_status = FALSE
        """, (user_id,))
        total_fines = cur.fetchone()["total"] or 0

        cur.execute("""
            SELECT COUNT(*) AS count FROM reservations WHERE user_id = %s AND reservation_status = 'ACTIVE'
        """, (user_id,))
        active_reservations = cur.fetchone()["count"]

    return {
        "borrowed_count": borrowed,
        "due_soon": due_soon,
        "total_fines": float(total_fines),
        "active_reservations": active_reservations,
    }
