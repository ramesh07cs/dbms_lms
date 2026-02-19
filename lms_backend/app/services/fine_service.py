from datetime import datetime

FINE_PER_DAY = 5  # Adjust as needed


def calculate_fine(due_date, return_date):
    """
    Calculate fine based on number of days late.
    """
    if return_date <= due_date:
        return 0

    days_late = (return_date - due_date).days
    return days_late * FINE_PER_DAY


def create_fine(conn, borrow_id, user_id, amount):
    """
    Insert fine record into database.
    """
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO fines (borrow_id, user_id, amount)
            VALUES (%s, %s, %s)
            RETURNING fine_id
        """, (borrow_id, user_id, amount))

        result = cur.fetchone()
        return result["fine_id"] if result else None
