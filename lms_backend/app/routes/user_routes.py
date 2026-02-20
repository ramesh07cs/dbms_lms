from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity
from marshmallow import ValidationError

from app.models.db import get_db
from app.models.user_queries import get_pending_users, get_user_by_id, get_all_users, get_teachers_and_students, update_user_status, delete_user
from app.services.user_service import register_user, authenticate_user, approve_or_reject_user
from app.utils.decorators import admin_required
from app.schemas.user_schema import RegisterSchema, LoginSchema
from app.utils.token_blacklist import add_token_to_blacklist  # import for logout
from app.services.audit_service import log_action

user_bp = Blueprint("user", __name__)

register_schema = RegisterSchema()
login_schema = LoginSchema()


# =========================
# REGISTER
# =========================
@user_bp.route("/register", methods=["POST"])
def register():
    conn = get_db()

    try:
        # Validate input
        data = register_schema.load(request.get_json())

        # Call service
        user_id = register_user(
            conn,
            data["name"],
            data["email"],
            data["password"],
            data["role_id"],
            data.get("phone")
        )

        return jsonify({
            "message": "User created successfully",
            "user_id": user_id
        }), 201

    except ValidationError as err:
        return jsonify({"validation_errors": err.messages}), 400

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500


# =========================
# LOGIN (JWT ISSUED HERE)
# =========================

@user_bp.route("/login", methods=["POST"])
def login():
    conn = get_db()

    try:
        data = login_schema.load(request.get_json())
        user = authenticate_user(conn, data["email"], data["password"])
        log_action(
            conn, user["user_id"],
            action="User Login",
            table_name="USER",
            record_id=user["user_id"],
            description=f"User {user['email']} logged in",
        )
        conn.commit()

        # Create access token (short-lived)
        access_token = create_access_token(
            identity={"id": user["user_id"], "role_id": user["role_id"], "email": user["email"]}
        )

        # Create refresh token (long-lived)
        refresh_token = create_refresh_token(
            identity={"id": user["user_id"], "role_id": user["role_id"], "email": user["email"]}
        )

        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token
        })

    except ValidationError as err:
        return jsonify({"validation_errors": err.messages}), 400

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 401

    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500
    
    

@user_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()

    # Issue a new access token
    new_access_token = create_access_token(identity=current_user)

    return jsonify({
        "access_token": new_access_token
    })



# =========================
# PROTECTED PROFILE
# =========================
@user_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    conn = get_db()
    db_user = get_user_by_id(conn, current_user["id"])
    name = db_user["name"] if db_user else None

    return jsonify({
        "message": "Access granted",
        "user": {
            "user_id": current_user["id"],
            "email": current_user["email"],
            "role_id": current_user["role_id"],
            "name": name or ""
        }
    }), 200

# =========================
# ADMIN: PENDING USERS
# =========================
@user_bp.route("/pending", methods=["GET"])
@jwt_required()
@admin_required
def pending_users():
    conn = get_db()
    users = get_pending_users(conn)
    return jsonify(users)


@user_bp.route("/approve/<int:user_id>", methods=["POST"])
@jwt_required()
@admin_required
def approve_user(user_id):
    conn = get_db()
    admin = get_jwt_identity()
    try:
        approve_or_reject_user(conn, user_id, "APPROVED", admin["id"])
        return jsonify({"message": "User approved successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@user_bp.route("/reject/<int:user_id>", methods=["POST"])
@jwt_required()
@admin_required
def reject_user(user_id):
    conn = get_db()
    admin = get_jwt_identity()
    try:
        approve_or_reject_user(conn, user_id, "REJECTED", admin["id"])
        return jsonify({"message": "User rejected"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# =========================
# TEACHER: LIST TEACHERS & STUDENTS (read-only)
# =========================
@user_bp.route("/list", methods=["GET"])
@jwt_required()
def list_teachers_students():
    current = get_jwt_identity()
    if current.get("role_id") != 2:
        return jsonify({"error": "Teachers only"}), 403
    conn = get_db()
    users = get_teachers_and_students(conn)
    return jsonify(users)


# =========================
# ADMIN: ALL USERS (User Management)
# =========================
@user_bp.route("/all", methods=["GET"])
@jwt_required()
@admin_required
def list_all_users():
    conn = get_db()
    users = get_all_users(conn)
    return jsonify(users)


@user_bp.route("/<int:user_id>/status", methods=["PUT"])
@jwt_required()
@admin_required
def set_user_status(user_id):
    conn = get_db()
    data = request.get_json()
    status = data.get("status")
    if status not in ("APPROVED", "PENDING", "REJECTED"):
        return jsonify({"error": "status must be APPROVED, PENDING, or REJECTED"}), 400
    admin = get_jwt_identity()
    try:
        update_user_status(conn, user_id, status, approved_by=admin["id"])
        log_action(
            conn, admin["id"],
            action="User Status Changed",
            table_name="USER",
            record_id=user_id,
            description=f"User {user_id} status set to {status}",
        )
        conn.commit()
        return jsonify({"message": f"User status set to {status}"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400


@user_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def remove_user(user_id):
    conn = get_db()
    admin = get_jwt_identity()
    if admin["id"] == user_id:
        return jsonify({"error": "Cannot delete your own account"}), 400
    try:
        log_action(
            conn, admin["id"],
            action="User Deleted",
            table_name="USER",
            record_id=user_id,
            description=f"User {user_id} removed by admin",
        )
        delete_user(conn, user_id)
        conn.commit()
        return jsonify({"message": "User removed"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400


# =========================
# LOGOUT (JWT BLACKLIST)
# =========================
@user_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    current_user = get_jwt_identity()
    conn = get_db()
    log_action(
        conn, current_user["id"],
        action="User Logout",
        table_name="USER",
        record_id=current_user["id"],
        description=f"User logged out",
    )
    conn.commit()
    claims = get_jwt()
    jti = claims["jti"]
    add_token_to_blacklist(jti)
    return jsonify({"message": "Logged out successfully"})
