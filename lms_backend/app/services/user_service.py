from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user_queries import (
    create_user,
    get_user_by_email,
    get_pending_users,
    update_user_status,
)


def register_user(conn, name, email, password, role_id, phone=None):
    """
    Handles full registration workflow:
    - Check if email exists
    - Hash password
    - Create user
    - Commit / Rollback handling
    """

    try:
        # Check if email already exists
        existing_user = get_user_by_email(conn, email)
        if existing_user:
            raise ValueError("Email already exists")

        # Hash password
        hashed_password = generate_password_hash(password)

        # Create user
        user_id = create_user(conn, name, email, hashed_password, role_id, phone)

        # Commit transaction
        conn.commit()

        return user_id

    except Exception as e:
        conn.rollback()
        raise e


def authenticate_user(conn, email, password):
    """
    Authenticates user:
    - Check if user exists
    - Verify password
    - Check approval status
    - Return full user object (for JWT creation)
    """

    user = get_user_by_email(conn, email)

    if not user:
        raise ValueError("User not found")

    # Verify password
    if not check_password_hash(user["password"], password):
        raise ValueError("Invalid password")

    # Check approval status
    if user["status"] != "APPROVED":
        raise ValueError("User not approved. Please contact Admin.")

    return user   # return full user dict (needed for JWT claims)


def approve_or_reject_user(conn, user_id, status, approved_by):
    """Approve or reject a pending user. status must be APPROVED or REJECTED."""
    if status not in ("APPROVED", "REJECTED"):
        raise ValueError("Status must be APPROVED or REJECTED")
    update_user_status(conn, user_id, status, approved_by)
    conn.commit()
