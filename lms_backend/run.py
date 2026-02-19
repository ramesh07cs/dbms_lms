# run.py

from flask import Flask
from flask_jwt_extended import JWTManager
from app.config import Config
from app.models.db import close_db, get_db
from app.routes.user_routes import user_bp
from app.routes.book_routes import book_bp
from app.routes.borrow_routes import borrow_bp
from app.routes.reservation_routes import reservation_bp
from app.routes.fine_routes import fine_bp
from app.routes.audit_routes import audit_bp
from app.utils.token_blacklist import is_token_blacklisted
from app.utils.error_handlers import register_error_handlers


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ==========================
    # Initialize JWT
    # ==========================
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return is_token_blacklisted(jwt_payload["jti"])
    
    # ==========================
    # Database Test Route
    # ==========================
    @app.route("/db-test")
    def db_test():
        """
        Test PostgreSQL connection
        """
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT 1 AS test")
            row = cur.fetchone()
            return {"result": row["test"]}
        except Exception as e:
            print("DB Test Error:", e)
            return {"error": str(e)}, 500

    # ==========================
    # DB teardown
    # ==========================
    app.teardown_appcontext(close_db)

    # ==========================
    # Register Blueprints
    # ==========================
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(book_bp, url_prefix="/books")
    app.register_blueprint(borrow_bp, url_prefix="/borrow")
    app.register_blueprint(reservation_bp, url_prefix="/reservation")
    app.register_blueprint(fine_bp, url_prefix="/fine")
    app.register_blueprint(audit_bp, url_prefix="/admin/audit")

    # ==========================
    # Home Route
    # ==========================
    @app.route("/")
    def home():
        return {"message": "LMS Backend Running Successfully"}

    # ==========================
    # Register Global Error Handlers
    # ==========================
    register_error_handlers(app)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
