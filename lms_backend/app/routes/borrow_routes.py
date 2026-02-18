# app/routes/borrow_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models.db import get_db
from app.services.borrow_service import issue_book, return_borrowed_book

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
# TEST ROUTE
# =========================
@borrow_bp.route("/test", methods=["GET"])
def test_route():
    print("Test route hit")
    return "ok"
