from flask import Flask
from app.models.db import close_db
from app.routes.user_routes import user_bp
from app.routes.book_routes import book_bp
from app.routes.borrow_routes import borrow_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(user_bp)
app.register_blueprint(book_bp)
app.register_blueprint(borrow_bp)

# Optional: Keep this test route
@app.route("/")
def home():
    return {"message": "LMS Backend Running Successfully"}

# Close DB connection after request
app.teardown_appcontext(close_db)

if __name__ == "__main__":
    app.run(debug=True)
