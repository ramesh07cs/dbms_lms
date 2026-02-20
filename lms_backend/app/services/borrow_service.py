# app/services/borrow_service.py

from datetime import datetime, timedelta
from app.models.book_queries import get_book_by_id, get_book_by_id_for_update, update_book_copies
from app.models.borrow_queries import (
    create_borrow,
    get_active_borrow,
    get_borrow_by_id,
    return_book_record,
)
from app.models.reservation_queries import (
    expire_overdue_reservations,
    get_oldest_active_reservation,
    get_first_reserved_user_id,
    mark_reservation_fulfilled
)
from app.services.fine_service import calculate_fine, create_fine
from app.services.audit_service import log_action

# =====================================================
# ISSUE BOOK (Reservation Priority Enforced)
# =====================================================
def issue_book(conn, user_id, book_id):
    """
    Issues a book to a user.
    - If ACTIVE reservation exists: only the FIRST user in queue can issue.
    - Others receive: "Book reserved by another user"
    - Transaction-safe with SELECT ... FOR UPDATE
    """
    try:
        book_id = int(book_id)
    except (ValueError, TypeError):
        raise ValueError("Invalid book_id")

    try:
        # 1. Expire overdue reservations (must run before we check queue)
        expire_overdue_reservations(conn)

        # 2. Lock book row for update (prevents race conditions)
        book = get_book_by_id_for_update(conn, book_id)
        if not book:
            raise ValueError("Book not found")
        if book["available_copies"] <= 0:
            raise ValueError("Book not available")

        # 3. Check if user already borrowed this book
        existing = get_active_borrow(conn, user_id, book_id)
        if existing:
            raise ValueError("User already borrowed this book")

        # 4. RESERVATION PRIORITY: If ACTIVE reservation exists, only first in queue can issue
        first_reserved_user_id = get_first_reserved_user_id(conn, book_id)
        if first_reserved_user_id is not None and first_reserved_user_id != user_id:
            raise ValueError("Book reserved by another user")

        # 5. Proceed with issue
        due_date = datetime.utcnow() + timedelta(days=7)
        new_available = book["available_copies"] - 1
        if new_available < 0:
            raise ValueError("Book not available")

        update_book_copies(conn, book_id, new_available)
        borrow_id = create_borrow(conn, user_id, book_id, due_date)
        if not borrow_id:
            raise Exception("Failed to issue book")

        # 6. If user was first in reservation queue, mark reservation FULFILLED
        if first_reserved_user_id == user_id:
            reservation = get_oldest_active_reservation(conn, book_id)
            if reservation:
                mark_reservation_fulfilled(conn, reservation["reservation_id"])

        log_action(
            conn,
            user_id,
            action="ISSUE_BOOK",
            table_name="borrows",
            record_id=borrow_id,
            description=f"Book {book_id} issued to user {user_id}"
        )

        conn.commit()
        return borrow_id

    except ValueError:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        raise e


# =====================================================
# RETURN BOOK + FINE + AUTO-RESERVATION
# =====================================================
def return_borrowed_book(conn, user_id, book_id):
    """
    Returns a borrowed book. Transaction-safe, prevents negative stock, avoids race conditions.
    - Increases stock
    - Fetches oldest ACTIVE reservation (with lock)
    - Auto-assigns to reserved user if any
    - Marks reservation FULFILLED
    - Logs AUTO_ASSIGN_BOOK in audit
    """
    try:
        book_id = int(book_id)
    except (ValueError, TypeError):
        raise ValueError("Invalid book_id")

    active = get_active_borrow(conn, user_id, book_id)
    if not active:
        raise ValueError("No active borrow found for this book")

    borrow_id = active["borrow_id"]
    due_date = active["due_date"]

    try:
        fine_amount = calculate_fine(due_date, datetime.utcnow())
        fine_id = None

        # 1. Mark borrow as returned
        return_book_record(conn, borrow_id)

        # 2. Lock book row and increase stock (prevents negative stock)
        book = get_book_by_id_for_update(conn, book_id)
        if not book:
            raise ValueError("Book not found")
        new_available = book["available_copies"] + 1
        update_book_copies(conn, book_id, new_available)

        # 3. Create fine if late
        if fine_amount > 0:
            fine_id = create_fine(conn, borrow_id, user_id, fine_amount)

        # 4. Check reservation queue (lock reservation row)
        reservation = get_oldest_active_reservation(conn, book_id)
        auto_assigned_borrow_id = None

        if reservation:
            reserved_user_id = reservation["user_id"]
            book_after_return = get_book_by_id(conn, book_id)
            avail = book_after_return["available_copies"]
            if avail <= 0:
                raise ValueError("Invalid state: available copies should be > 0 after return")
            update_book_copies(conn, book_id, avail - 1)
            new_due_date = datetime.utcnow() + timedelta(days=7)
            auto_assigned_borrow_id = create_borrow(conn, reserved_user_id, book_id, new_due_date)
            mark_reservation_fulfilled(conn, reservation["reservation_id"])
            log_action(
                conn,
                reserved_user_id,
                action="AUTO_ASSIGN_BOOK",
                table_name="borrows",
                record_id=auto_assigned_borrow_id,
                description=f"Book {book_id} auto-assigned from reservation"
            )

        log_action(
            conn,
            user_id,
            action="RETURN_BOOK",
            table_name="borrows",
            record_id=borrow_id,
            description=f"Book {book_id} returned by user {user_id}"
        )

        conn.commit()
        return {
            "message": "Book returned successfully",
            "fine_amount": fine_amount,
            "fine_id": fine_id,
            "auto_assigned_borrow_id": auto_assigned_borrow_id
        }

    except ValueError:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        raise e


# =====================================================
# ADMIN: ISSUE BOOK TO ANY USER
# =====================================================
def admin_issue_book(conn, target_user_id, book_id):
    """Admin issues a book to a specific user."""
    return issue_book(conn, target_user_id, book_id)


# =====================================================
# ADMIN: RETURN BY BORROW ID
# =====================================================
def admin_return_by_borrow_id(conn, borrow_id):
    """Admin returns a book by borrow_id. Returns fine info if applicable."""
    borrow = get_borrow_by_id(conn, borrow_id)
    if not borrow:
        raise ValueError("Borrow record not found")
    if borrow["borrow_status"] == "RETURNED":
        raise ValueError("Book already returned")
    user_id = borrow["user_id"]
    book_id = borrow["book_id"]
    return return_borrowed_book(conn, user_id, book_id)
