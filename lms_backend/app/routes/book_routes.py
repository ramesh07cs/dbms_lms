from flask import Blueprint, request, jsonify
from app.services.book_service import (
    add_book,
    fetch_book,
    fetch_all_books,
    change_book_copies
)

book_bp = Blueprint("book", __name__, url_prefix="/books")


@book_bp.route("/", methods=["POST"])
def create_book_route():
    data = request.get_json()

    try:
        book_id = add_book(
            title=data.get("title"),
            author=data.get("author"),
            isbn=data.get("isbn"),
            total_copies=data.get("total_copies")
        )

        return jsonify({
            "message": "Book created successfully",
            "book_id": book_id
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@book_bp.route("/<int:book_id>", methods=["GET"])
def get_book_route(book_id):
    try:
        book = fetch_book(book_id)
        return jsonify(book), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    except Exception:
        return jsonify({"error": "Internal server error"}), 500


@book_bp.route("/", methods=["GET"])
def get_all_books_route():
    try:
        books = fetch_all_books()
        return jsonify(books), 200

    except Exception:
        return jsonify({"error": "Internal server error"}), 500


@book_bp.route("/<int:book_id>/copies", methods=["PUT"])
def update_book_copies_route(book_id):
    data = request.get_json()

    try:
        change_book_copies(
            book_id,
            data.get("available_copies")
        )

        return jsonify({"message": "Book copies updated successfully"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception:
        return jsonify({"error": "Internal server error"}), 500
