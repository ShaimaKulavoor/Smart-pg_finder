"""
Booking routes for Smart PG Recommendation App
Handles user bookings and owner contact
"""

from flask import Blueprint, request, jsonify
from functools import wraps
from datetime import datetime
import jwt
import os

# Create blueprint
bp = Blueprint('booking', __name__, url_prefix='/api/booking')

def token_required(f):
    """Require valid JWT token for protected routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for token in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'status': 'error', 'message': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'status': 'error', 'message': 'Token is missing'}), 401
        
        try:
            secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production-2024')
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
            current_user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'status': 'error', 'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'status': 'error', 'message': 'Invalid token'}), 401
        
        return f(current_user_id, *args, **kwargs)
    
    return decorated


@bp.route('/book', methods=['POST'])
@token_required
def book_pg(current_user_id):
    """
    Create a booking for a PG
    
    Request body:
    {
        "pg_id": int,
        "check_in_date": "2024-05-15"  (optional)
    }
    """
    try:
        from app import db
        from models import Booking, PG, User
        
        data = request.get_json()
        
        if not data or not data.get('pg_id'):
            return jsonify({
                'status': 'error',
                'message': 'PG ID is required'
            }), 400
        
        pg_id = data.get('pg_id')
        check_in_date = data.get('check_in_date', '')
        
        # Verify PG exists
        pg = PG.query.get(pg_id)
        if not pg:
            return jsonify({
                'status': 'error',
                'message': 'PG not found'
            }), 404
        
        # Check if user already booked this PG
        existing_booking = Booking.query.filter_by(
            user_id=current_user_id,
            pg_id=pg_id,
            status='pending'
        ).first()
        
        if existing_booking:
            return jsonify({
                'status': 'error',
                'message': 'You already have a pending booking for this PG'
            }), 409
        
        # Create booking
        booking = Booking(
            user_id=current_user_id,
            pg_id=pg_id,
            check_in_date=check_in_date,
            status='pending',
            booking_date=datetime.utcnow()
        )
        
        db.session.add(booking)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'Booking confirmed! You will be contacted by the owner at their registered phone number.',
            'booking': booking.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Booking failed: {str(e)}'
        }), 500


@bp.route('/get-owner-details/<int:pg_id>', methods=['GET'])
def get_owner_details(pg_id):
    """
    Get owner contact details for a PG
    
    Response:
    {
        "status": "success",
        "owner": {
            "name": "...",
            "phone": "...",
            "email": "..."
        }
    }
    """
    try:
        from models import PG
        
        pg = PG.query.get(pg_id)
        
        if not pg:
            return jsonify({
                'status': 'error',
                'message': 'PG not found'
            }), 404
        
        return jsonify({
            'status': 'success',
            'owner': {
                'name': pg.owner_name,
                'phone': pg.owner_phone,
                'email': pg.owner_email
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error fetching owner details: {str(e)}'
        }), 500


@bp.route('/my-bookings', methods=['GET'])
@token_required
def get_my_bookings(current_user_id):
    """
    Get all bookings for current user
    
    Response:
    {
        "status": "success",
        "bookings": [...]
    }
    """
    try:
        from models import Booking
        
        bookings = Booking.query.filter_by(user_id=current_user_id).all()
        
        return jsonify({
            'status': 'success',
            'count': len(bookings),
            'bookings': [b.to_dict() for b in bookings]
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error fetching bookings: {str(e)}'
        }), 500


@bp.route('/cancel-booking/<int:booking_id>', methods=['POST'])
@token_required
def cancel_booking(current_user_id, booking_id):
    """
    Cancel a booking
    
    Response:
    {
        "status": "success",
        "message": "Booking cancelled"
    }
    """
    try:
        from app import db
        from models import Booking
        
        booking = Booking.query.get(booking_id)
        
        if not booking:
            return jsonify({
                'status': 'error',
                'message': 'Booking not found'
            }), 404
        
        # Verify ownership
        if booking.user_id != current_user_id:
            return jsonify({
                'status': 'error',
                'message': 'Unauthorized: This is not your booking'
            }), 403
        
        # Only allow cancellation if pending
        if booking.status != 'pending':
            return jsonify({
                'status': 'error',
                'message': f'Cannot cancel {booking.status} booking'
            }), 400
        
        booking.status = 'cancelled'
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Booking cancelled successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error cancelling booking: {str(e)}'
        }), 500
