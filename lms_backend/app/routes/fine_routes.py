from flask import Blueprint, request, jsonify
from app.models.db import get_db
from app.services.fine_service import pay_fine, get_my_unpaid_fines, get_all_fines_admin

fine_bp = Blueprint("fine", __name__)


@fine_bp.route("/my", methods=["GET"])
def my_fines():
    user_id = request.args.get("user_id")
    page = int(request.args.get("page", 1))

    conn = get_db()
    try:
        fines = get_my_unpaid_fines(conn, user_id, page)
        return jsonify(fines)
    finally:
        # request-scoped connection closed by teardown
        pass


@fine_bp.route("/pay/<int:fine_id>", methods=["POST"])
def pay_fine_route(fine_id):
    admin_id = request.json.get("admin_id")

    conn = get_db()
    try:
        pay_fine(conn, fine_id, admin_id)
        return jsonify({"message": "Fine paid successfully"})
    finally:
        # request-scoped connection closed by teardown
        pass
