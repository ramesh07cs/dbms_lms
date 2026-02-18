from flask import jsonify
from flask_jwt_extended.exceptions import JWTExtendedException

def register_error_handlers(app):

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"msg": "Resource not found"}), 404

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"msg": "Bad request"}), 400

    @app.errorhandler(JWTExtendedException)
    def jwt_errors(e):
        return jsonify({"msg": str(e)}), 401

    @app.errorhandler(Exception)
    def server_error(e):
        return jsonify({"msg": "Internal server error"}), 500
