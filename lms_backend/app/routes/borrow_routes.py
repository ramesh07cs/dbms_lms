from flask import Blueprint, request, jsonify
from app.services.borrow_service import issue_book, return_borrowed_book

borrow_bp = Blueprint("borrow", __name__, url_prefix="/borrow")


@borrow_bp.route("/issue", methods=["POST"])
def issue():
    data = request.get_json()

    try:
        borrow_id = issue_book(
            data["user_id"],
            data["book_id"]
        )

        return jsonify({
            "message": "Book issued",
            "borrow_id": borrow_id
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception:
        return jsonify({"error": "Internal server error"}), 500


@borrow_bp.route("/return", methods=["POST"])
def return_book():
    data = request.get_json()

    try:
        return_borrowed_book(
            data["user_id"],
            data["book_id"]
        )

        return jsonify({"message": "Book returned"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception:
        return jsonify({"error": "Internal server error"}), 500
