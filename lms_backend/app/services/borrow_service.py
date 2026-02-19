# app/services/borrow_service.py

from datetime import datetime, timedelta
from app.models.book_queries import get_book_by_id, update_book_copies
from app.models.borrow_queries import (
    create_borrow,
    get_active_borrow,
    get_borrow_by_id,
    return_book_record,
)
from app.models.reservation_queries import (
    expire_overdue_reservations,
    get_oldest_active_reservation,
    mark_reservation_fulfilled
)
from app.services.fine_service import calculate_fine, create_fine
from app.services.audit_service import log_action

# =====================================================
# ISSUE BOOK
# =====================================================
def issue_book(conn, user_id, book_id):
    """
    Issues a book to a user.
    Checks available copies, prevents double borrowing,
    and expires overdue reservations.
    """
    print("issue_book called with:", user_id, book_id)

    # 0️⃣ Expire overdue reservations before issuing
    expire_overdue_reservations(conn)

    # Validate book_id
    try:
        book_id = int(book_id)
    except ValueError:
        raise ValueError("Invalid book_id")

    # Check book exists
    book = get_book_by_id(conn, book_id)
    if not book:
        raise ValueError("Book not found")
    if book['available_copies'] <= 0:
        raise ValueError("Book not available")

    # Check if user already borrowed this book
    existing = get_active_borrow(conn, user_id, book_id)
    if existing:
        raise ValueError("User already borrowed this book")

    # Calculate due date
    due_date = datetime.utcnow() + timedelta(days=7)

    try:
        # Reduce available copies
        update_book_copies(conn, book_id, book['available_copies'] - 1)

        # Create borrow record
        borrow_id = create_borrow(conn, user_id, book_id, due_date)
        if not borrow_id:
            raise Exception("Failed to issue book")

        # Audit log
        log_action(
            conn,
            user_id,
            action="ISSUE_BOOK",
            table_name="borrows",
            record_id=borrow_id,
            description=f"Book {book_id} issued to user {user_id}"
        )

        # Commit transaction
        conn.commit()
        print("Book issued successfully, borrow_id:", borrow_id)
        return borrow_id

    except Exception as e:
        conn.rollback()
        raise e


# =====================================================
# RETURN BOOK + FINE + AUTO-RESERVATION
# =====================================================
def return_borrowed_book(conn, user_id, book_id):
    """
    Returns a borrowed book:
    - Calculates fine
    - Updates borrow record
    - Updates stock
    - Creates fine record if needed
    - Checks reservations and auto-assigns
    - Logs audit
    """
    print("return_borrowed_book called with:", user_id, book_id)

    try:
        book_id = int(book_id)
    except ValueError:
        raise ValueError("Invalid book_id")

    # Find active borrow
    active = get_active_borrow(conn, user_id, book_id)
    if not active:
        raise ValueError("No active borrow found for this book")

    borrow_id = active["borrow_id"]
    due_date = active["due_date"]
    return_date = datetime.utcnow()

    try:
        # 1️⃣ Calculate fine
        fine_amount = calculate_fine(due_date, return_date)

        # 2️⃣ Mark borrow as returned
        return_book_record(conn, borrow_id)

        # 3️⃣ Increase available copies
        book = get_book_by_id(conn, book_id)
        if book:
            update_book_copies(
                conn,
                book_id,
                book["available_copies"] + 1
            )

        fine_id = None

        # 4️⃣ Create fine if late
        if fine_amount > 0:
            fine_id = create_fine(conn, borrow_id, user_id, fine_amount)

        # 5️⃣ CHECK RESERVATION QUEUE (oldest ACTIVE)
        reservation = get_oldest_active_reservation(conn, book_id)
        auto_assigned_borrow_id = None

        if reservation:
            reserved_user_id = reservation["user_id"]

            # Reduce stock for auto-assign
            book = get_book_by_id(conn, book_id)
            update_book_copies(
                conn,
                book_id,
                book["available_copies"] - 1
            )

            # Create borrow for reserved user
            new_due_date = datetime.utcnow() + timedelta(days=7)
            auto_assigned_borrow_id = create_borrow(
                conn,
                reserved_user_id,
                book_id,
                new_due_date
            )

            # Mark reservation fulfilled
            mark_reservation_fulfilled(conn, reservation["reservation_id"])

            # Audit auto assignment
            log_action(
                conn,
                reserved_user_id,
                action="AUTO_ASSIGN_BOOK",
                table_name="borrows",
                record_id=auto_assigned_borrow_id,
                description=f"Book {book_id} auto-assigned from reservation"
            )

        # 6️⃣ Audit return
        log_action(
            conn,
            user_id,
            action="RETURN_BOOK",
            table_name="borrows",
            record_id=borrow_id,
            description=f"Book {book_id} returned by user {user_id}"
        )

        # Commit all
        conn.commit()

        return {
            "message": "Book returned successfully",
            "fine_amount": fine_amount,
            "fine_id": fine_id,
            "auto_assigned_borrow_id": auto_assigned_borrow_id
        }

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
