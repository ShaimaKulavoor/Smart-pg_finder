"""
Authentication routes
Handles user registration, login, and logout
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import jwt
from functools import wraps

# Create blueprint
bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Import after app initialization to avoid circular imports
def get_db_and_app():
    from app import db, app
    return db, app

def token_required(f):
    """Decorator to require JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'status': 'error', 'message': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'status': 'error', 'message': 'Token is missing'}), 401
        
        try:
            db, app = get_db_and_app()
            from models import User
            
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            
            if not current_user:
                return jsonify({'status': 'error', 'message': 'User not found'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'status': 'error', 'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'status': 'error', 'message': 'Invalid token'}), 401
        except Exception as e:
            return jsonify({'status': 'error', 'message': f'Error verifying token: {str(e)}'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

@bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    
    Request body:
    {
        "username": "string",
        "email": "string",
        "password": "string"
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data or not all(k in data for k in ['username', 'email', 'password']):
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
        
        username = data['username'].strip()
        email = data['email'].strip()
        password = data['password']
        
        # Validate inputs
        if len(username) < 3:
            return jsonify({'status': 'error', 'message': 'Username must be at least 3 characters'}), 400
        
        if len(password) < 6:
            return jsonify({'status': 'error', 'message': 'Password must be at least 6 characters'}), 400
        
        if '@' not in email:
            return jsonify({'status': 'error', 'message': 'Invalid email format'}), 400
        
        db, app = get_db_and_app()
        from models import User
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'status': 'error', 'message': 'Username already exists'}), 409
        
        if User.query.filter_by(email=email).first():
            return jsonify({'status': 'error', 'message': 'Email already exists'}), 409
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Registration error: {str(e)}'}), 500

@bp.route('/login', methods=['POST'])
def login():
    """
    Login user and return JWT token
    
    Request body:
    {
        "username": "string",
        "password": "string"
    }
    """
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['username', 'password']):
            return jsonify({'status': 'error', 'message': 'Missing credentials'}), 400
        
        username = data['username']
        password = data['password']
        
        db, app = get_db_and_app()
        from models import User
        
        # Find user
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.utcnow() + app.config['JWT_EXPIRATION_DELTA']
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'status': 'success',
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Login error: {str(e)}'}), 500

@bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """
    Logout user (no-op on backend, mainly for frontend cleanup)
    """
    return jsonify({
        'status': 'success',
        'message': 'Logout successful'
    }), 200

@bp.route('/verify-token', methods=['GET'])
@token_required
def verify_token(current_user):
    """
    Verify if token is valid and return user info
    """
    return jsonify({
        'status': 'success',
        'user': current_user.to_dict()
    }), 200

@bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """
    Get authenticated user's profile
    """
    return jsonify({
        'status': 'success',
        'user': current_user.to_dict()
    }), 200

@bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    """
    Update user profile
    """
    try:
        db, app = get_db_and_app()
        data = request.get_json()
        
        if 'email' in data:
            current_user.email = data['email']
        
        if 'password' in data:
            current_user.set_password(data['password'])
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Profile updated',
            'user': current_user.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Update error: {str(e)}'}), 500
