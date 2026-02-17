from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.models.db import get_db
from app.services.user_service import register_user, login_user
from app.schemas.user_schema import RegisterSchema, LoginSchema

user_bp = Blueprint("user", __name__, url_prefix="/users")

register_schema = RegisterSchema()
login_schema = LoginSchema()


@user_bp.route("/register", methods=["POST"])
def register():
    conn = get_db()

    try:
        # Validate input
        data = register_schema.load(request.get_json())

        # Call service layer
        user_id = register_user(
            conn,
            data["name"],
            data["email"],
            data["password"],
            data["role_id"]
        )

        return jsonify({
            "message": "User created",
            "user_id": user_id
        }), 201

    except ValidationError as err:
        return jsonify({"validation_errors": err.messages}), 400

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500


@user_bp.route("/login", methods=["POST"])
def login():
    conn = get_db()

    try:
        # Validate input
        data = login_schema.load(request.get_json())

        # Call service layer
        user_id = login_user(conn, data["email"], data["password"])

        return jsonify({
            "message": "Login successful",
            "user_id": user_id
        })

    except ValidationError as err:
        return jsonify({"validation_errors": err.messages}), 400

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500
