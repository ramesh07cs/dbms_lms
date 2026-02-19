"""Dashboard stats routes."""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.db import get_db
from app.models.stats_queries import get_admin_stats, get_teacher_stats, get_student_stats
from app.utils.decorators import admin_required

stats_bp = Blueprint("stats", __name__)


@stats_bp.route("/admin", methods=["GET"])
@jwt_required()
@admin_required
def admin_stats():
    conn = get_db()
    stats = get_admin_stats(conn)
    return jsonify(stats)


@stats_bp.route("/teacher", methods=["GET"])
@jwt_required()
def teacher_stats():
    user = get_jwt_identity()
    if user.get("role_id") != 2:
        return jsonify({"error": "Teachers only"}), 403
    conn = get_db()
    stats = get_teacher_stats(conn, user["id"])
    return jsonify(stats)


@stats_bp.route("/student", methods=["GET"])
@jwt_required()
def student_stats():
    user = get_jwt_identity()
    if user.get("role_id") != 3:
        return jsonify({"error": "Students only"}), 403
    conn = get_db()
    stats = get_student_stats(conn, user["id"])
    return jsonify(stats)
