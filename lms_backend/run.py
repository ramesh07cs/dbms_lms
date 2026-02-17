from flask import Flask, g
from app.models.db import get_db, close_db
from app.routes.user_routes import user_bp
from app.routes.book_routes import book_bp
from app.routes.borrow_routes import borrow_bp

app = Flask(__name__)

# 🔥 ADD THIS
@app.before_request
def before_request():
    get_db()   # This will automatically set g.db

# Register Blueprints
app.register_blueprint(user_bp)
app.register_blueprint(book_bp)
app.register_blueprint(borrow_bp)

@app.route("/")
def home():
    return {"message": "LMS Backend Running Successfully"}

# Close DB connection after request
app.teardown_appcontext(close_db)

if __name__ == "__main__":
    app.run(debug=True)
