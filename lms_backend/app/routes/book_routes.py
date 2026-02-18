from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils.decorators import admin_required
from app.models.db import get_db
from app.services.book_service import add_book, fetch_book, fetch_all_books, change_book_copies

book_bp = Blueprint("book", __name__)

# =========================
# ADMIN: ADD BOOK
# =========================
@book_bp.route("/", methods=["POST"])
@jwt_required()
@admin_required
def create_book_route():
    conn = get_db()
    data = request.get_json()

    try:
        book_id = add_book(
            conn,
            title=data.get("title"),
            author=data.get("author"),
            isbn=data.get("isbn"),
            total_copies=data.get("total_copies")
        )
        return jsonify({"message": "Book created successfully", "book_id": book_id}), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500


# =========================
# ADMIN: UPDATE COPIES
# =========================
@book_bp.route("/<int:book_id>/copies", methods=["PUT"])
@jwt_required()
@admin_required
def update_book_copies_route(book_id):
    conn = get_db()
    data = request.get_json()

    try:
        change_book_copies(
            conn,
            book_id,
            data.get("available_copies")
        )
        return jsonify({"message": "Book copies updated successfully"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500


# =========================
# PUBLIC: GET ALL BOOKS
# =========================
@book_bp.route("/", methods=["GET"])
def get_all_books_route():
    conn = get_db()
    try:
        books = fetch_all_books(conn)
        return jsonify(books), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500


# =========================
# PUBLIC: GET SINGLE BOOK
# =========================
@book_bp.route("/<int:book_id>", methods=["GET"])
def get_single_book_route(book_id):
    conn = get_db()
    try:
        book = fetch_book(conn, book_id)
        return jsonify(book), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500
