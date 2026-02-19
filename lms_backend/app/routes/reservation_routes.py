from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import admin_required
from app.models.db import get_db
from app.models.reservation_queries import (
    create_reservation,
    expire_overdue_reservations,
    get_all_reservations,
    get_user_reservations,
)
from app.services.audit_service import log_action

reservation_bp = Blueprint("reservation", __name__)


@reservation_bp.route("/all", methods=["GET"])
@jwt_required()
@admin_required
def list_all_reservations():
    conn = get_db()
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 50))
    offset = (page - 1) * limit
    reservations = get_all_reservations(conn, limit, offset)
    return jsonify(reservations)


@reservation_bp.route("/my", methods=["GET"])
@jwt_required()
def my_reservations():
    conn = get_db()
    user = get_jwt_identity()
    user_id = user.get("id")
    reservations = get_user_reservations(conn, user_id)
    return jsonify(reservations)


@reservation_bp.route("/create", methods=["POST"])
@jwt_required()
def create_new_reservation():
    data = request.json
    book_id = data.get("book_id")

    # derive user from JWT
    current_user = get_jwt_identity()
    user_id = current_user.get("id")

    conn = get_db()

    try:
        expire_overdue_reservations(conn)

        reservation_id = create_reservation(conn, user_id, book_id)

        log_action(
            conn,
            user_id,
            action="CREATE_RESERVATION",
            table_name="reservations",
            record_id=reservation_id,
            description=f"User {user_id} reserved book {book_id}"
        )

        conn.commit()

        return jsonify({"reservation_id": reservation_id})

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400

    finally:
        # connection is request-scoped and will be closed by app.teardown_appcontext
        pass


@reservation_bp.route("/cancel/<int:reservation_id>", methods=["DELETE"])
@jwt_required()
def cancel_reservation(reservation_id):
    conn = get_db()
    current_user = get_jwt_identity()

    try:
        # ensure owner or admin
        with conn.cursor() as cur:
            cur.execute("SELECT user_id FROM reservations WHERE reservation_id = %s", (reservation_id,))
            row = cur.fetchone()
            owner_id = row[0] if row else None

        if owner_id is None:
            return jsonify({"error": "Reservation not found"}), 404

        if current_user.get("id") != owner_id and current_user.get("role_id") != 1:
            return jsonify({"error": "Forbidden"}), 403

        with conn.cursor() as cur:
            cur.execute("""
                UPDATE reservations
                SET reservation_status = 'CANCELLED'
                WHERE reservation_id = %s
            """, (reservation_id,))

        conn.commit()
        return jsonify({"message": "Reservation cancelled"})

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400

    finally:
        # connection is request-scoped and will be closed by app.teardown_appcontext
        pass
