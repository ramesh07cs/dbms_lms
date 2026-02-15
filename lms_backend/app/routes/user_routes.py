from flask import Blueprint, request, jsonify
from app.models.db import get_db
from app.services.user_service import register_user, login_user

user_bp = Blueprint("user", __name__, url_prefix="/users")


@user_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    conn = get_db()

    try:
        user_id = register_user(
            conn,
            data["name"],
            data["email"],
            data["password"],
            data["role_id"]
        )
        conn.commit()
        return jsonify({"message": "User created", "user_id": user_id}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    conn = get_db()

    try:
        user_id = login_user(conn, data["email"], data["password"])
        return jsonify({"message": "Login successful", "user_id": user_id})

    except Exception as e:
        return jsonify({"error": str(e)}), 400
