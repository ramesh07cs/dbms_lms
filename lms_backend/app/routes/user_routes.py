from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token,jwt_required, get_jwt, get_jwt_identity
from marshmallow import ValidationError


from app.models.db import get_db
from app.services.user_service import register_user, authenticate_user
from app.schemas.user_schema import RegisterSchema, LoginSchema
from app.utils.token_blacklist import add_token_to_blacklist  # import for logout

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
            data["role_id"]
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

    return jsonify({
        "message": "Access granted",
        "user": {
            "user_id": current_user["id"],
            "email": current_user["email"],
            "role_id": current_user["role_id"]
        }
    }), 200

# =========================
# LOGOUT (JWT BLACKLIST)
# =========================
@user_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    claims = get_jwt()
    jti = claims["jti"]

    # Add token to blacklist
    add_token_to_blacklist(jti)

    return jsonify({"message": "Logged out successfully"})
