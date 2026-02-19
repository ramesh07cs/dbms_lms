from datetime import datetime
from app.models.fine_queries import (
    insert_fine,
    get_user_unpaid_fines,
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
    return result["fine_id"] if result else None


def pay_fine(conn, fine_id, admin_id):
    result = mark_fine_paid(conn, fine_id)

    if not result:
        raise ValueError("Fine not found")

    log_action(
        conn,
        admin_id,
        action="PAY_FINE",
        table_name="fines",
        record_id=fine_id,
        description=f"Fine {fine_id} marked as paid"
    )

    conn.commit()
    return True


def get_my_unpaid_fines(conn, user_id, page=1, limit=20):
    offset = (page - 1) * limit
    return get_user_unpaid_fines(conn, user_id, limit, offset)


def get_all_fines_admin(conn, page=1, limit=20):
    offset = (page - 1) * limit
    return get_all_fines(conn, limit, offset)
