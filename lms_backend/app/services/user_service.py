# app/services/user_service.py

from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user_queries import (
    create_user,
    get_user_by_email,
    update_user_status
)


def register_user(conn, name, email, password, role_id):
    existing = get_user_by_email(conn, email)
    if existing:
        raise ValueError("Email already exists")

    password_hash = generate_password_hash(password)

    return create_user(conn, name, email, password_hash, role_id)


def login_user(conn, email, password):
    user = get_user_by_email(conn, email)

    if not user:
        raise ValueError("User not found")

    user_id, name, email, password_hash, role_id, status = user

    if not check_password_hash(password_hash, password):
        raise ValueError("Invalid password")

    if status != "APPROVED":
        raise ValueError("User not approved")

    return user_id
