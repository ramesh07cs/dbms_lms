from flask import Blueprint, request, jsonify
from app.utils.decorators import admin_required
from app.models.db import get_db
from app.models.audit_queries import get_audit_logs

audit_bp = Blueprint("audit", __name__)


@audit_bp.route("/", methods=["GET"])
@admin_required
def view_audit_logs():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 20))
    offset = (page - 1) * limit

    conn = get_db()
    try:
        logs = get_audit_logs(conn, limit, offset)
        return jsonify(logs)
    finally:
        # request-scoped connection closed by teardown
        pass
