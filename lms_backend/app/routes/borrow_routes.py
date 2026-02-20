# app/routes/borrow_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.db import get_db
from app.models.borrow_queries import get_all_active_borrows, get_user_active_borrows, get_user_borrow_history, get_pending_borrows, get_all_borrows
from app.models.user_queries import get_approved_users_for_borrow, get_students_for_borrow
from app.services.borrow_service import (
    request_borrow,
    issue_book,
    return_borrowed_book,
    admin_issue_book,
    admin_return_by_borrow_id,
    approve_borrow,
    reject_borrow,
)
from app.utils.decorators import admin_required

borrow_bp = Blueprint("borrow", __name__)

# =========================
# REQUEST BORROW (STUDENT & TEACHER) – creates PENDING
# =========================
@borrow_bp.route("/request", methods=["POST"])
@jwt_required()
def request_borrow_route():
    conn = get_db()
    user = get_jwt_identity()
    if user.get("role_id") not in [2, 3]:
        return jsonify({"error": "Only students or teachers can request books"}), 403
    data = request.get_json()
    book_id = data.get("book_id")
    if not book_id:
        return jsonify({"error": "book_id is required"}), 400
    # Ensure user_id is NOT in request body (it comes from JWT)
    if "user_id" in data:
        return jsonify({"error": "user_id should not be in request body; it is derived from JWT"}), 400
    try:
        borrow_id = request_borrow(conn, user["id"], book_id)
        return jsonify({"message": "Borrow request submitted", "borrow_id": borrow_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        print(f"Error in request_borrow_route: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


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
# ADMIN: LIST ALL BORROWS (for Borrow Management)
# =========================
@borrow_bp.route("/admin/all", methods=["GET"])
@jwt_required()
@admin_required
def admin_list_all_borrows():
    conn = get_db()
    borrows = get_all_borrows(conn)
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
# ADMIN: PENDING BORROW REQUESTS
# =========================
@borrow_bp.route("/admin/pending", methods=["GET"])
@jwt_required()
@admin_required
def admin_list_pending():
    conn = get_db()
    borrows = get_pending_borrows(conn)
    return jsonify(borrows)


@borrow_bp.route("/admin/approve/<int:borrow_id>", methods=["POST"])
@jwt_required()
@admin_required
def admin_approve_borrow(borrow_id):
    conn = get_db()
    admin = get_jwt_identity()
    try:
        approve_borrow(conn, borrow_id, admin_id=admin["id"])
        return jsonify({"message": "Borrow approved", "borrow_id": borrow_id}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@borrow_bp.route("/admin/reject/<int:borrow_id>", methods=["POST"])
@jwt_required()
@admin_required
def admin_reject_borrow(borrow_id):
    conn = get_db()
    admin = get_jwt_identity()
    try:
        reject_borrow(conn, borrow_id, admin_id=admin["id"])
        return jsonify({"message": "Borrow rejected", "borrow_id": borrow_id}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


# =========================
# ADMIN: LIST USERS (for Issue form – Students + Teachers)
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
# TEACHER: LIST STUDENTS (for Issue form – Students only)
# =========================
@borrow_bp.route("/teacher/students", methods=["GET"])
@jwt_required()
def teacher_list_students():
    user = get_jwt_identity()
    if user.get("role_id") != 2:
        return jsonify({"error": "Teachers only"}), 403
    conn = get_db()
    users = get_students_for_borrow(conn)
    return jsonify(users)


# =========================
# TEACHER: ISSUE BOOK TO STUDENT ONLY
# =========================
@borrow_bp.route("/teacher/issue", methods=["POST"])
@jwt_required()
def teacher_issue():
    user = get_jwt_identity()
    if user.get("role_id") != 2:
        return jsonify({"error": "Teachers only"}), 403
    conn = get_db()
    data = request.get_json()
    user_id = data.get("user_id")
    book_id = data.get("book_id")
    if not user_id or not book_id:
        return jsonify({"error": "user_id and book_id are required"}), 400
    # Verify target is a student (role_id 3)
    users = get_students_for_borrow(conn)
    if not any(u["user_id"] == int(user_id) for u in users):
        return jsonify({"error": "Teachers can only issue books to students"}), 403
    try:
        borrow_id = admin_issue_book(conn, int(user_id), int(book_id))
        return jsonify({"message": "Book issued successfully", "borrow_id": borrow_id}), 201
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
