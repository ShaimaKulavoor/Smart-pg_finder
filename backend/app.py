"""
Smart PG Recommendation - Flask Backend
Main application entry point
"""

from flask import Flask, jsonify
from flask_cors import CORS
from extensions import db
from datetime import timedelta
import os

# Initialize Flask app
app = Flask(__name__)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT & Session Config
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production-2024')
app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=7)
app.config['SESSION_COOKIE_SECURE'] = False  # Set True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Enable CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:5000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Initialize DB
db.init_app(app)

# 👉 Import models AFTER db init (prevents circular import)
from models import User, PG

# Import routes AFTER models
from routes import auth_routes, recommendation_routes, chat_routes, upload_routes, booking_routes

# Register blueprints
app.register_blueprint(auth_routes.bp)
app.register_blueprint(recommendation_routes.bp)
app.register_blueprint(chat_routes.bp)
app.register_blueprint(upload_routes.bp)
app.register_blueprint(booking_routes.bp)

# Serve uploaded files statically
import os
uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(uploads_dir, exist_ok=True)

@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    from flask import send_from_directory
    return send_from_directory(uploads_dir, filename)

# ---------------- ROUTES ---------------- #

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'message': 'Smart PG Recommendation API is running'
    }), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500


# ---------------- RUN APP ---------------- #

if __name__ == '__main__':
    with app.app_context():
        db.create_all()   # ensure tables exist

    app.run(debug=True, host='0.0.0.0', port=5000)