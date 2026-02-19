# app/routes/borrow_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.db import get_db
from app.models.borrow_queries import get_all_active_borrows, get_user_active_borrows, get_user_borrow_history
from app.models.user_queries import get_approved_users_for_borrow
from app.services.borrow_service import (
    issue_book,
    return_borrowed_book,
    admin_issue_book,
    admin_return_by_borrow_id,
)
from app.utils.decorators import admin_required

borrow_bp = Blueprint("borrow", __name__)

# =========================
# ISSUE BOOK (STUDENT & TEACHER)
# =========================
@borrow_bp.route("/issue", methods=["POST"])
@jwt_required()
def issue():
    conn = get_db()
    user = get_jwt_identity()
    
    # Get role_id from identity, not from claims
    role_id = user.get("role_id")
    
    # Only role 2 (teacher) or 3 (student) can borrow
    if role_id not in [2, 3]:
        return jsonify({"error": "Only students or teachers can borrow books"}), 403

    data = request.get_json()
    book_id = data.get("book_id")
    if not book_id:
        return jsonify({"error": "book_id is required"}), 400

    print("Route /issue called. User:", user, "Book ID:", book_id)

    try:
        borrow_id = issue_book(conn, user["id"], book_id)
        return jsonify({"message": "Book issued successfully", "borrow_id": borrow_id}), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print("Borrow 500:", e)
        return jsonify({"error": "Internal server error"}), 500


# =========================
# RETURN BOOK (STUDENT & TEACHER)
# =========================
@borrow_bp.route("/return", methods=["POST"])
@jwt_required()
def return_book():
    conn = get_db()
    user = get_jwt_identity()
    
    # Get role_id from identity, not from claims
    role_id = user.get("role_id")

    if role_id not in [2, 3]:
        return jsonify({"error": "Only students or teachers can return books"}), 403

    data = request.get_json()
    book_id = data.get("book_id")
    if not book_id:
        return jsonify({"error": "book_id is required"}), 400

    print("Route /return called. User:", user, "Book ID:", book_id)

    try:
        return_borrowed_book(conn, user["id"], book_id)
        return jsonify({"message": "Book returned successfully"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print("Return 500:", e)
        return jsonify({"error": "Internal server error"}), 500


# =========================
# USER: MY ACTIVE BORROWS (for return form - teacher/student)
# =========================
@borrow_bp.route("/my/active", methods=["GET"])
@jwt_required()
def my_active_borrows():
    user = get_jwt_identity()
    if user.get("role_id") not in [2, 3]:
        return jsonify({"error": "Students and teachers only"}), 403
    conn = get_db()
    borrows = get_user_active_borrows(conn, user["id"])
    return jsonify(borrows)


# =========================
# USER: BORROW HISTORY
# =========================
@borrow_bp.route("/my/history", methods=["GET"])
@jwt_required()
def my_borrow_history():
    user = get_jwt_identity()
    if user.get("role_id") not in [2, 3]:
        return jsonify({"error": "Students and teachers only"}), 403
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 50))
    offset = (page - 1) * limit
    conn = get_db()
    borrows = get_user_borrow_history(conn, user["id"], limit, offset)
    return jsonify(borrows)


# =========================
# ADMIN: LIST ACTIVE BORROWS (for Return form)
# =========================
@borrow_bp.route("/admin/active", methods=["GET"])
@jwt_required()
@admin_required
def admin_list_active_borrows():
    conn = get_db()
    borrows = get_all_active_borrows(conn)
    return jsonify(borrows)


# =========================
# ADMIN: LIST USERS (for Issue form)
# =========================
@borrow_bp.route("/admin/users", methods=["GET"])
@jwt_required()
@admin_required
def admin_list_users():
    conn = get_db()
    users = get_approved_users_for_borrow(conn)
    return jsonify(users)


# =========================
# ADMIN: ISSUE BOOK TO USER
# =========================
@borrow_bp.route("/admin/issue", methods=["POST"])
@jwt_required()
@admin_required
def admin_issue():
    conn = get_db()
    data = request.get_json()
    user_id = data.get("user_id")
    book_id = data.get("book_id")
    if not user_id or not book_id:
        return jsonify({"error": "user_id and book_id are required"}), 400
    try:
        borrow_id = admin_issue_book(conn, user_id, book_id)
        return jsonify({"message": "Book issued successfully", "borrow_id": borrow_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


# =========================
# ADMIN: RETURN BOOK BY BORROW ID
# =========================
@borrow_bp.route("/admin/return", methods=["POST"])
@jwt_required()
@admin_required
def admin_return():
    conn = get_db()
    data = request.get_json()
    borrow_id = data.get("borrow_id")
    if not borrow_id:
        return jsonify({"error": "borrow_id is required"}), 400
    try:
        result = admin_return_by_borrow_id(conn, borrow_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


# =========================
# TEST ROUTE
# =========================
@borrow_bp.route("/test", methods=["GET"])
def test_route():
    print("Test route hit")
    return "ok"
