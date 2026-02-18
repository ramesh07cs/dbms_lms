# run.py
from flask import Flask, g
from flask_jwt_extended import JWTManager
from app.config import Config
from app.models.db import get_db, close_db
from app.routes.user_routes import user_bp
from app.routes.book_routes import book_bp
from app.routes.borrow_routes import borrow_bp
from app.utils.token_blacklist import is_token_blacklisted
from app.utils.error_handlers import register_error_handlers


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ==========================
    # Initialize JWT
    # ==========================
    jwt = JWTManager(app)

    # ==========================
    # Token Blacklist Check
    # ==========================
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return is_token_blacklisted(jti)

    # ==========================
    # Database Auto Connection
    # ==========================
    @app.before_request
    def before_request():
        try:
            get_db()  # sets g.db automatically
        except Exception as e:
            print("DB Connection Error in before_request:", e)
            # Don't short-circuit the request here — allow the route handler to
            # run so its debug prints (e.g., in `borrow_routes.issue`) are visible.
            # Route-level DB usage will still raise when `get_db()` is called there.
            g.db_connection_error = e

    app.teardown_appcontext(close_db)

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
    # Register Blueprints
    # ==========================
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(book_bp, url_prefix="/books")
    app.register_blueprint(borrow_bp, url_prefix="/borrow")

    # ==========================
    # Home Route
    # ==========================
    @app.route("/")
    def home():
        return {"message": "LMS Backend Running Successfully"}

    # ==========================
    # Register Custom Error Handlers
    # ==========================
    register_error_handlers(app)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
