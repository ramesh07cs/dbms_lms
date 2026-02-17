from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user_queries import (
    create_user,
    get_user_by_email
)


def register_user(conn, name, email, password, role_id):
    """
    Handles full registration workflow:
    - Email check
    - Password hashing
    - User creation
    - Transaction control
    """

    try:
        # Check if email exists
        existing = get_user_by_email(conn, email)
        if existing:
            raise ValueError("Email already exists")

        # Hash password
        password_hash = generate_password_hash(password)

        # Insert user
        user_id = create_user(conn, name, email, password_hash, role_id)

        # Commit transaction
        conn.commit()

        return user_id

    except Exception:
        conn.rollback()
        raise


def login_user(conn, email, password):
    """
    Authenticates user:
    - Check user exists
    - Verify password
    - Check approval status
    """

    user = get_user_by_email(conn, email)

    if not user:
        raise ValueError("User not found")

    user_id = user["user_id"]
    password_hash = user["password"]
    status = user["status"]

    # Verify password
    if not check_password_hash(password_hash, password):
        raise ValueError("Invalid password")

    # Check approval
    if status != "APPROVED":
        raise ValueError("User not approved. Please contact an Admin.")

    return user_id
