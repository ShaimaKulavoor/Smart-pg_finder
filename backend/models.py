"""
Database models for Smart PG Recommendation App
"""

from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    saved_pgs = db.relationship('SavedPG', backref='user', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }


class PG(db.Model):
    """PG/Property model from dataset"""
    __tablename__ = 'pgs'
    
    id = db.Column(db.Integer, primary_key=True)
    posted_on = db.Column(db.String(50))
    bhk = db.Column(db.Integer)
    rent = db.Column(db.Integer)
    size = db.Column(db.Integer)
    floor = db.Column(db.String(100))
    area_type = db.Column(db.String(50))
    area_locality = db.Column(db.String(200))
    city = db.Column(db.String(100))
    furnishing_status = db.Column(db.String(50))
    tenant_preferred = db.Column(db.String(100))
    bathroom = db.Column(db.Integer)
    point_of_contact = db.Column(db.String(50))
    rating = db.Column(db.Float, default=4.0)
    image_url = db.Column(db.String(500), default='https://via.placeholder.com/300x200')
    description = db.Column(db.Text, default='')
    # Owner contact details
    owner_phone = db.Column(db.String(20), default='+91-XXXXXXXXXX')
    owner_email = db.Column(db.String(120), default='owner@example.com')
    owner_name = db.Column(db.String(100), default='Property Owner')
    
    # Relationships
    saved_by = db.relationship('SavedPG', backref='pg', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='pg', lazy=True, cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', backref='pg', lazy=True, cascade='all, delete-orphan')
    bookings = db.relationship('Booking', backref='pg', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert PG to dictionary"""
        return {
            'id': self.id,
            'posted_on': self.posted_on,
            'bhk': self.bhk,
            'rent': self.rent,
            'size': self.size,
            'floor': self.floor,
            'area_type': self.area_type,
            'area_locality': self.area_locality,
            'city': self.city,
            'furnishing_status': self.furnishing_status,
            'tenant_preferred': self.tenant_preferred,
            'bathroom': self.bathroom,
            'point_of_contact': self.point_of_contact,
            'rating': self.rating,
            'image_url': self.image_url,
            'description': self.description,
            'amenities': [a.to_dict() for a in self.amenities]
        }


class SavedPG(db.Model):
    """User's saved/favorited PGs"""
    __tablename__ = 'saved_pgs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pg_id = db.Column(db.Integer, db.ForeignKey('pgs.id'), nullable=False)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)


class Review(db.Model):
    """Reviews for PGs"""
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pg_id = db.Column(db.Integer, db.ForeignKey('pgs.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert review to dictionary"""
        return {
            'id': self.id,
            'user': self.user.username,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat()
        }


class Amenity(db.Model):
    """Amenities for PGs"""
    __tablename__ = 'amenities'
    
    id = db.Column(db.Integer, primary_key=True)
    pg_id = db.Column(db.Integer, db.ForeignKey('pgs.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    available = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        """Convert amenity to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'available': self.available
        }


class Booking(db.Model):
    """Booking model for user PG bookings"""
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pg_id = db.Column(db.Integer, db.ForeignKey('pgs.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    check_in_date = db.Column(db.String(50))  # Desired move-in date
    status = db.Column(db.String(50), default='pending')  # pending, confirmed, cancelled
    notes = db.Column(db.Text, default='')
    
    # Relationships
    user = db.relationship('User', backref='bookings')
    
    def to_dict(self):
        """Convert booking to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'pg_id': self.pg_id,
            'booking_date': self.booking_date.isoformat(),
            'check_in_date': self.check_in_date,
            'status': self.status,
            'notes': self.notes,
            'pg': {
                'area_locality': self.pg.area_locality,
                'city': self.pg.city,
                'rent': self.pg.rent
            }
        }
