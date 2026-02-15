from flask import Blueprint, request, jsonify
from app.models.db import get_db
from app.services.borrow_service import issue_book, return_borrowed_book

borrow_bp = Blueprint("borrow", __name__, url_prefix="/borrow")


@borrow_bp.route("/issue", methods=["POST"])
def issue():
    data = request.get_json()
    conn = get_db()

    try:
        borrow_id = issue_book(conn, data["user_id"], data["book_id"])
        conn.commit()
        return jsonify({"message": "Book issued", "borrow_id": borrow_id}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400


@borrow_bp.route("/return", methods=["POST"])
def return_book():
    data = request.get_json()
    conn = get_db()

    try:
        return_borrowed_book(conn, data["user_id"], data["book_id"])
        conn.commit()
        return jsonify({"message": "Book returned"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
