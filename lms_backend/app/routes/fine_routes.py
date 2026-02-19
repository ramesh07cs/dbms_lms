from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import admin_required
from app.models.db import get_db
from app.services.fine_service import pay_fine, get_my_unpaid_fines, get_all_fines_admin

fine_bp = Blueprint("fine", __name__)


@fine_bp.route("/all", methods=["GET"])
@jwt_required()
@admin_required
def all_fines():
    page = int(request.args.get("page", 1))
    conn = get_db()
    try:
        fines = get_all_fines_admin(conn, page)
        return jsonify(fines)
    finally:
        pass


@fine_bp.route("/my", methods=["GET"])
@jwt_required()
def my_fines():
    page = int(request.args.get("page", 1))

    current_user = get_jwt_identity()
    user_id = current_user.get("id")

    conn = get_db()
    try:
        fines = get_my_unpaid_fines(conn, user_id, page)
        return jsonify(fines)
    finally:
        # request-scoped connection closed by teardown
        pass


@fine_bp.route("/pay/<int:fine_id>", methods=["POST"])
@jwt_required()
@admin_required
def pay_fine_route(fine_id):
    current_user = get_jwt_identity()
    admin_id = current_user.get("id")

    conn = get_db()
    try:
        pay_fine(conn, fine_id, admin_id)
        conn.commit()
        return jsonify({"message": "Fine paid successfully"})
    finally:
        # request-scoped connection closed by teardown
        pass
