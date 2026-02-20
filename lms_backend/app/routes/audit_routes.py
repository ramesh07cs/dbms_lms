from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import admin_required
from app.models.db import get_db
from app.models.audit_queries import get_audit_logs, get_user_audit_logs

audit_bp = Blueprint("audit", __name__)


@audit_bp.route("/my-logs", methods=["GET"])
@jwt_required()
def my_audit_logs():
    """Student/Teacher: own audit logs."""
    user = get_jwt_identity()
    user_id = user.get("id")
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 20))
    offset = (page - 1) * limit
    conn = get_db()
    logs = get_user_audit_logs(conn, user_id, limit, offset)
    return jsonify(logs)


@audit_bp.route("/all", methods=["GET"])
@jwt_required()
@admin_required
def view_all_audit_logs():
    """Admin: all audit logs."""
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 20))
    offset = (page - 1) * limit
    conn = get_db()
    logs = get_audit_logs(conn, limit, offset)
    return jsonify(logs)


@audit_bp.route("/", methods=["GET"])
@jwt_required()
@admin_required
def view_audit_logs():
    """Alias for /audit/all for backward compatibility."""
    return view_all_audit_logs()
