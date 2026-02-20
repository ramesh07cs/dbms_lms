from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import admin_required
from app.models.db import get_db
from app.services.audit_service import log_action
from app.services.book_service import (
    add_book,
    fetch_book,
    fetch_all_books,
    change_book_copies,
    update_book_details,
    remove_book,
)

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
            total_copies=data.get("total_copies"),
            category=data.get("category"),
            available_copies=data.get("available_copies"),
        )
        admin = get_jwt_identity()
        log_action(conn, admin["id"], "Book Created", "BOOK", book_id, f"Book created: {data.get('title')}")
        conn.commit()
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
        admin = get_jwt_identity()
        log_action(conn, admin["id"], "Available Copies Updated", "BOOK", book_id, f"Available copies set to {data.get('available_copies')}")
        conn.commit()
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
# ADMIN: UPDATE BOOK (full)
# =========================
@book_bp.route("/<int:book_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_book_route(book_id):
    conn = get_db()
    data = request.get_json()
    try:
        update_book_details(
            conn,
            book_id,
            title=data.get("title"),
            author=data.get("author"),
            category=data.get("category"),
            isbn=data.get("isbn"),
            total_copies=data.get("total_copies"),
            available_copies=data.get("available_copies"),
        )
        admin = get_jwt_identity()
        log_action(conn, admin["id"], "Book Updated", "BOOK", book_id, f"Book {book_id} updated")
        conn.commit()
        return jsonify({"message": "Book updated successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


# =========================
# ADMIN: DELETE BOOK (soft)
# =========================
@book_bp.route("/<int:book_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_book_route(book_id):
    conn = get_db()
    try:
        remove_book(conn, book_id)
        admin = get_jwt_identity()
        log_action(conn, admin["id"], "Book Deleted", "BOOK", book_id, f"Book {book_id} soft-deleted")
        conn.commit()
        return jsonify({"message": "Book deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
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
