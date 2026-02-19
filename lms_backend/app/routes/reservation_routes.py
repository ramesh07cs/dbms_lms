from flask import Blueprint, request, jsonify
from app.models.db import get_db
from app.models.reservation_queries import create_reservation, expire_overdue_reservations
from app.services.audit_service import log_action

reservation_bp = Blueprint("reservation", __name__)


@reservation_bp.route("/create", methods=["POST"])
def create_new_reservation():
    data = request.json
    user_id = data.get("user_id")
    book_id = data.get("book_id")

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
def cancel_reservation(reservation_id):
    conn = get_db()
    try:
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
