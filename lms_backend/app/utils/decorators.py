from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()

        # Safety check
        if not current_user:
            return jsonify({"msg": "Unauthorized"}), 401

        # Check role_id instead of role
        if current_user.get("role_id") != 1:
            return jsonify({"msg": "Admins only"}), 403

        return fn(*args, **kwargs)

    return wrapper
