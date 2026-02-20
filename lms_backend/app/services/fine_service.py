from datetime import datetime
from app.models.fine_queries import (
    insert_fine,
    get_user_unpaid_fines,
    get_user_fines_with_book,
    mark_fine_paid,
    get_all_fines
)
from app.services.audit_service import log_action

FINE_PER_DAY = 5


def calculate_fine(due_date, return_date):
    if return_date <= due_date:
        return 0

    days_late = (return_date - due_date).days
    return days_late * FINE_PER_DAY


def create_fine(conn, borrow_id, user_id, amount):
    result = insert_fine(conn, borrow_id, user_id, amount)
    fine_id = result[0] if result and isinstance(result, (list, tuple)) else (result.get("fine_id") if result else None)
    if fine_id:
        log_action(
            conn, user_id,
            action="Fine Created",
            table_name="FINE",
            record_id=fine_id,
            description=f"Fine {fine_id} created for borrow {borrow_id}, amount Rs {amount}",
        )
    return fine_id


def pay_fine(conn, fine_id, admin_id):
    result = mark_fine_paid(conn, fine_id)

    if not result:
        raise ValueError("Fine not found")

    log_action(
        conn, admin_id,
        action="Fine Paid",
        table_name="FINE",
        record_id=fine_id,
        description=f"Fine {fine_id} marked as paid"
    )

    conn.commit()
    return True


def get_my_unpaid_fines(conn, user_id, page=1, limit=20):
    offset = (page - 1) * limit
    return get_user_unpaid_fines(conn, user_id, limit, offset)


def get_my_fines_with_book(conn, user_id, page=1, limit=50):
    """All fines for user with book title (paid + unpaid)."""
    offset = (page - 1) * limit
    return get_user_fines_with_book(conn, user_id, limit, offset)


def get_all_fines_admin(conn, page=1, limit=20):
    offset = (page - 1) * limit
    return get_all_fines(conn, limit, offset)
