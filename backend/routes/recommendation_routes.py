"""
Recommendation routes
Handles PG recommendations and details
"""

from flask import Blueprint, request, jsonify
from functools import wraps
import jwt
from datetime import datetime

# Create blueprint
bp = Blueprint('recommendations', __name__, url_prefix='/api')

def get_db_and_recommender():
    """Get db and recommender instances"""
    from app import db
    from ml_model import get_recommendations, get_similar_recommendations
    return db, get_recommendations, get_similar_recommendations

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
            # Allow unauthenticated access for recommendations
            return f(None, *args, **kwargs)
        
        try:
            from app import app
            from models import User
            
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            
            if not current_user:
                return f(None, *args, **kwargs)
        except:
            return f(None, *args, **kwargs)
        
        return f(current_user, *args, **kwargs)
    
    return decorated

@bp.route('/recommend', methods=['GET', 'POST'])
@token_required
def recommend(current_user):
    """
    Get PG recommendations based on user preferences
    
    Query parameters or JSON body:
    {
        "city": "string",
        "max_budget": integer,
        "tenant_type": "string",
        "bhk": integer,
        "top_n": integer (default: 5)
    }
    """
    try:
        # Get parameters from query string or JSON body
        if request.method == 'POST':
            data = request.get_json() or {}
        else:
            data = request.args.to_dict()
        
        city = data.get('city')
        max_budget = data.get('max_budget')
        tenant_type = data.get('tenant_type')
        bhk = data.get('bhk')
        top_n = int(data.get('top_n', 5))
        
        # Convert budget and bhk to proper types
        if max_budget:
            try:
                max_budget = int(max_budget)
            except:
                max_budget = None
        
        if bhk:
            try:
                bhk = int(bhk)
            except:
                bhk = None
        
        db, get_recommendations_fn, _ = get_db_and_recommender()
        from models import PG
        
        # Get recommendations from ML model
        recommendations = get_recommendations_fn(city, max_budget, tenant_type, bhk, top_n)
        
        # If no recommendations from ML, return from database
        if not recommendations:
            query = PG.query
            
            if city:
                query = query.filter(PG.city.ilike(f'%{city}%'))
            if max_budget:
                query = query.filter(PG.rent <= max_budget)
            if tenant_type:
                query = query.filter(PG.tenant_preferred.ilike(f'%{tenant_type}%'))
            if bhk:
                query = query.filter(PG.bhk == bhk)
            
            pgs = query.order_by(PG.rent.asc(), PG.rating.desc()).limit(top_n).all()
            recommendations = [pg.to_dict() for pg in pgs]
        
        return jsonify({
            'status': 'success',
            'count': len(recommendations),
            'recommendations': recommendations
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Recommendation error: {str(e)}'
        }), 500

@bp.route('/pg/<int:pg_id>', methods=['GET'])
def get_pg_details(pg_id):
    """
    Get detailed information about a specific PG
    
    Parameters:
        pg_id: PG ID
    """
    try:
        db, _, get_similar_recommendations_fn = get_db_and_recommender()
        from models import PG
        
        pg = PG.query.get(pg_id)
        
        if not pg:
            return jsonify({
                'status': 'error',
                'message': 'PG not found'
            }), 404
        
        pg_dict = pg.to_dict()
        
        # Get similar recommendations
        similar = get_similar_recommendations_fn(pg.area_locality, top_n=3)
        pg_dict['similar_pgs'] = similar
        
        # Get reviews
        reviews = [review.to_dict() for review in pg.reviews]
        pg_dict['reviews'] = reviews
        
        return jsonify({
            'status': 'success',
            'pg': pg_dict
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error fetching PG details: {str(e)}'
        }), 500

@bp.route('/filter', methods=['GET', 'POST'])
def filter_pgs():
    """
    Filter PGs based on multiple criteria
    
    Query parameters or JSON body:
    {
        "city": "string",
        "min_budget": integer,
        "max_budget": integer,
        "bhk": integer,
        "furnishing": "string",
        "tenant_type": "string",
        "area_type": "string",
        "skip": integer (default: 0),
        "limit": integer (default: 20)
    }
    """
    try:
        if request.method == 'POST':
            data = request.get_json() or {}
        else:
            data = request.args.to_dict()
        
        db, _, _ = get_db_and_recommender()
        from models import PG
        
        query = PG.query
        
        if data.get('city'):
            query = query.filter(PG.city.ilike(f"%{data['city']}%"))
        
        if data.get('min_budget'):
            try:
                query = query.filter(PG.rent >= int(data['min_budget']))
            except:
                pass
        
        if data.get('max_budget'):
            try:
                query = query.filter(PG.rent <= int(data['max_budget']))
            except:
                pass
        
        if data.get('bhk'):
            try:
                query = query.filter(PG.bhk == int(data['bhk']))
            except:
                pass
        
        if data.get('furnishing'):
            query = query.filter(PG.furnishing_status.ilike(f"%{data['furnishing']}%"))
        
        if data.get('tenant_type'):
            query = query.filter(PG.tenant_preferred.ilike(f"%{data['tenant_type']}%"))
        
        if data.get('area_type'):
            query = query.filter(PG.area_type.ilike(f"%{data['area_type']}%"))
        
        # Pagination
        skip = int(data.get('skip', 0))
        limit = int(data.get('limit', 20))
        
        total = query.count()
        pgs = query.order_by(PG.rating.desc()).offset(skip).limit(limit).all()
        
        return jsonify({
            'status': 'success',
            'total': total,
            'skip': skip,
            'limit': limit,
            'count': len(pgs),
            'pgs': [pg.to_dict() for pg in pgs]
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Filter error: {str(e)}'
        }), 500

@bp.route('/cities', methods=['GET'])
def get_cities():
    """Get list of all cities with PG listings"""
    try:
        from app import db
        from models import PG
        
        # Query using the current app's db session
        cities = db.session.query(PG.city).distinct().all()
        cities = [city[0] for city in cities if city[0]]
        
        return jsonify({
            'status': 'success',
            'cities': sorted(cities)
        }), 200
    
    except Exception as e:
        import traceback
        print(f"Cities endpoint error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'message': f'Error fetching cities: {str(e)}'
        }), 500

@bp.route('/localities/<city>', methods=['GET'])
def get_localities(city):
    """Get list of localities in a specific city"""
    try:
        db, _, _ = get_db_and_recommender()
        from models import PG
        
        localities = db.session.query(PG.area_locality).filter(
            PG.city.ilike(f'%{city}%')
        ).distinct().all()
        localities = [loc[0] for loc in localities if loc[0]]
        
        return jsonify({
            'status': 'success',
            'city': city,
            'localities': sorted(localities)
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error fetching localities: {str(e)}'
        }), 500

@bp.route('/stats', methods=['GET'])
def get_stats():
    """Get general statistics about PGs"""
    try:
        db, _, _ = get_db_and_recommender()
        from models import PG
        from sqlalchemy import func
        
        total_pgs = PG.query.count()
        avg_rent = db.session.query(func.avg(PG.rent)).scalar()
        avg_rating = db.session.query(func.avg(PG.rating)).scalar()
        
        return jsonify({
            'status': 'success',
            'stats': {
                'total_pgs': total_pgs,
                'average_rent': round(float(avg_rent) if avg_rent else 0, 2),
                'average_rating': round(float(avg_rating) if avg_rating else 0, 1)
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error fetching stats: {str(e)}'
        }), 500

@bp.route('/favorites', methods=['GET'])
@token_required
def get_favorites(current_user):
    """Get user's favorite/saved PGs"""
    if not current_user:
        return jsonify({
            'status': 'error',
            'message': 'Authentication required'
        }), 401
    
    try:
        db, _, _ = get_db_and_recommender()
        
        saved_pgs = current_user.saved_pgs
        pgs = [saved_pg.pg.to_dict() for saved_pg in saved_pgs]
        
        return jsonify({
            'status': 'success',
            'count': len(pgs),
            'favorites': pgs
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error fetching favorites: {str(e)}'
        }), 500

@bp.route('/favorites/<int:pg_id>', methods=['POST'])
@token_required
def save_favorite(current_user, pg_id):
    """Save a PG to favorites"""
    if not current_user:
        return jsonify({
            'status': 'error',
            'message': 'Authentication required'
        }), 401
    
    try:
        db, _, _ = get_db_and_recommender()
        from models import PG, SavedPG
        
        pg = PG.query.get(pg_id)
        if not pg:
            return jsonify({
                'status': 'error',
                'message': 'PG not found'
            }), 404
        
        # Check if already saved
        existing = SavedPG.query.filter_by(user_id=current_user.id, pg_id=pg_id).first()
        if existing:
            return jsonify({
                'status': 'error',
                'message': 'Already in favorites'
            }), 400
        
        # Add to favorites
        saved_pg = SavedPG(user_id=current_user.id, pg_id=pg_id)
        db.session.add(saved_pg)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Added to favorites'
        }), 201
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error saving favorite: {str(e)}'
        }), 500

@bp.route('/favorites/<int:pg_id>', methods=['DELETE'])
@token_required
def remove_favorite(current_user, pg_id):
    """Remove a PG from favorites"""
    if not current_user:
        return jsonify({
            'status': 'error',
            'message': 'Authentication required'
        }), 401
    
    try:
        db, _, _ = get_db_and_recommender()
        from models import SavedPG
        
        saved_pg = SavedPG.query.filter_by(user_id=current_user.id, pg_id=pg_id).first()
        if not saved_pg:
            return jsonify({
                'status': 'error',
                'message': 'PG not in favorites'
            }), 404
        
        db.session.delete(saved_pg)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Removed from favorites'
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error removing favorite: {str(e)}'
        }), 500

@bp.route('/favorites/<int:pg_id>/check', methods=['GET'])
@token_required
def check_favorite(current_user, pg_id):
    """Check if PG is in user's favorites"""
    if not current_user:
        return jsonify({
            'status': 'success',
            'is_favorite': False
        }), 200
    
    try:
        from models import SavedPG
        
        saved_pg = SavedPG.query.filter_by(user_id=current_user.id, pg_id=pg_id).first()
        
        return jsonify({
            'status': 'success',
            'is_favorite': saved_pg is not None
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error checking favorite: {str(e)}'
        }), 500

