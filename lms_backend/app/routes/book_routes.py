from flask import Blueprint, request, jsonify
from app.models.db import get_db
from app.services.book_service import add_book

book_bp = Blueprint("book", __name__, url_prefix="/books")


@book_bp.route("/add", methods=["POST"])
def add():
    data = request.get_json()
    conn = get_db()

    try:
        book_id = add_book(
            conn,
            data["title"],
            data.get("author"),
            data.get("category"),
            data.get("isbn"),
            data["total_copies"]
        )
        conn.commit()
        return jsonify({"message": "Book added", "book_id": book_id}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
