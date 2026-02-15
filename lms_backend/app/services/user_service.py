from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user_queries import (
    create_user,
    get_user_by_email,
    update_user_status
)

def register_user(conn, name, email, password, role_id):
    """
    Registers a new user after checking if the email already exists.
    """
    # get_user_by_email returns a dictionary or None
    existing = get_user_by_email(conn, email)
    if existing:
        raise ValueError("Email already exists")

    # Hash the password for security
    password_hash = generate_password_hash(password)

    # create_user handles the INSERT and returns the new user_id
    return create_user(conn, name, email, password_hash, role_id)


def login_user(conn, email, password):
    """
    Authenticates a user and checks if their account is APPROVED.
    """
    # Fetch user data - returns a dictionary due to RealDictCursor
    user = get_user_by_email(conn, email)

    if not user:
        raise ValueError("User not found")

    # FIX: Access values using dictionary keys as defined in your schema
    user_id = user['user_id']
    password_hash = user['password']
    status = user['status']

    # Verify the provided password against the stored hash
    if not check_password_hash(password_hash, password):
        raise ValueError("Invalid password")

    # Check approval status
    if status != "APPROVED":
        raise ValueError("User not approved. Please contact an Admin.")

    return user_id