"""
Admin API Routes - Complete Admin Panel Backend
"""

from flask import Blueprint, request, jsonify, current_app
from functools import wraps
from bson import ObjectId
from datetime import datetime, timedelta
import jwt

admin_bp = Blueprint('admin', __name__)

# Helper to get current user from token
def get_current_user():
    """Get current user from JWT token"""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    
    try:
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        
        from app import db
        user = db.users.find_one({'_id': ObjectId(payload['user_id'])})
        return user
    except:
        return None


# Admin authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user or user.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/dashboard', methods=['GET', 'OPTIONS'])
@admin_required
def get_dashboard_stats():
    """Get admin dashboard statistics"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        from app import db
        
        # Count users by role
        total_users = db.users.count_documents({})
        total_students = db.users.count_documents({'role': 'student'})
        total_counsellors = db.users.count_documents({'role': 'counsellor'})
        
        # Count careers and colleges
        total_careers = db.careers.count_documents({})
        total_colleges = db.colleges.count_documents({})
        
        # Count sessions
        collection_names = db.list_collection_names()
        total_sessions = db.appointments.count_documents({}) if 'appointments' in collection_names else 0
        
        # Calculate revenue
        if 'appointments' in collection_names:
            revenue_pipeline = [
                {'$match': {'status': 'completed'}},
                {'$group': {'_id': None, 'total': {'$sum': '$amount_paid'}}}
            ]
            revenue_result = list(db.appointments.aggregate(revenue_pipeline))
            revenue = revenue_result[0]['total'] if revenue_result else 0
        else:
            revenue = 0
        
        # Active users (logged in last 24 hours)
        twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
        active_now = db.users.count_documents({
            'last_login': {'$gte': twenty_four_hours_ago}
        })
        
        # Pending counsellor approvals
        pending_approvals = db.users.count_documents({
            'role': 'counsellor',
            'is_active': False
        })
        
        return jsonify({
            'totalUsers': total_users,
            'totalStudents': total_students,
            'totalCounsellors': total_counsellors,
            'totalSessions': total_sessions,
            'totalCareers': total_careers,
            'totalColleges': total_colleges,
            'revenue': revenue,
            'activeNow': active_now,
            'pendingApprovals': pending_approvals
        }), 200
        
    except Exception as e:
        print(f"❌ Dashboard stats error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# ==================== USER MANAGEMENT ====================

@admin_bp.route('/users', methods=['GET', 'OPTIONS'])
@admin_required
def get_all_users():
    """Get all users with filters"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        from app import db
        
        # Get query parameters
        role = request.args.get('role')
        search = request.args.get('search')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 50))
        
        # Build query
        query = {}
        if role:
            query['role'] = role
        if search:
            query['$or'] = [
                {'name': {'$regex': search, '$options': 'i'}},
                {'email': {'$regex': search, '$options': 'i'}},
                {'username': {'$regex': search, '$options': 'i'}}
            ]
        
        # Get users
        users = list(db.users.find(query, {'password': 0})
                    .skip((page - 1) * limit)
                    .limit(limit)
                    .sort('created_at', -1))
        
        # Format response
        for user in users:
            user['_id'] = str(user['_id'])
            if 'created_at' in user:
                user['created_at'] = user['created_at'].isoformat()
        
        # Get total count
        total = db.users.count_documents(query)
        
        return jsonify({
            'users': users,
            'total': total,
            'page': page,
            'pages': (total + limit - 1) // limit
        }), 200
        
    except Exception as e:
        print(f"❌ Get users error: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/users/<user_id>', methods=['PUT', 'OPTIONS'])
@admin_required
def update_user(user_id):
    """Update user details"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        from app import db
        
        data = request.json
        
        # Don't allow password or role updates
        data.pop('password', None)
        data.pop('role', None)
        
        data['updated_at'] = datetime.utcnow()
        
        result = db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': data}
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'message': 'User updated successfully'}), 200
        
    except Exception as e:
        print(f"❌ Update user error: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/users/<user_id>', methods=['DELETE', 'OPTIONS'])
@admin_required
def delete_user(user_id):
    """Delete user"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        from app import db
        
        result = db.users.delete_one({'_id': ObjectId(user_id)})
        
        if result.deleted_count == 0:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'message': 'User deleted successfully'}), 200
        
    except Exception as e:
        print(f"❌ Delete user error: {e}")
        return jsonify({'error': str(e)}), 500


# ==================== COUNSELLOR MANAGEMENT ====================

@admin_bp.route('/counsellors', methods=['GET', 'OPTIONS'])
@admin_required
def get_all_counsellors():
    """Get all counsellors with stats"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        from app import db
        
        counsellors = list(db.users.find({'role': 'counsellor'}, {'password': 0})
                          .sort('created_at', -1))
        
        collection_names = db.list_collection_names()
        
        for counsellor in counsellors:
            counsellor['_id'] = str(counsellor['_id'])
            
            # Get session count for each counsellor
            if 'appointments' in collection_names:
                sessions = db.appointments.count_documents({
                    'counsellor_id': str(counsellor['_id'])
                })
                counsellor['total_sessions'] = sessions
            else:
                counsellor['total_sessions'] = 0
        
        return jsonify({'counsellors': counsellors}), 200
        
    except Exception as e:
        print(f"❌ Get counsellors error: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/counsellors/<counsellor_id>/approve', methods=['PUT', 'OPTIONS'])
@admin_required
def approve_counsellor(counsellor_id):
    """Approve or reject counsellor"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        from app import db
        
        data = request.json
        approved = data.get('approved', True)
        
        result = db.users.update_one(
            {'_id': ObjectId(counsellor_id), 'role': 'counsellor'},
            {'$set': {
                'is_active': approved,
                'approved_at': datetime.utcnow() if approved else None,
                'updated_at': datetime.utcnow()
            }}
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'Counsellor not found'}), 404
        
        return jsonify({
            'message': f'Counsellor {"approved" if approved else "rejected"} successfully'
        }), 200
        
    except Exception as e:
        print(f"❌ Approve counsellor error: {e}")
        return jsonify({'error': str(e)}), 500


# ==================== CAREER MANAGEMENT ====================

@admin_bp.route('/careers', methods=['GET', 'OPTIONS'])
@admin_required
def get_all_careers():
    """Get all careers"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        from app import db
        
        careers = list(db.careers.find().sort('name', 1))
        
        for career in careers:
            career['_id'] = str(career['_id'])
        
        return jsonify({'careers': careers}), 200
        
    except Exception as e:
        print(f"❌ Get careers error: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/careers', methods=['POST', 'OPTIONS'])
@admin_required
def add_career():
    """Add new career"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        from app import db
        
        data = request.json
        
        # Validate required fields
        required_fields = ['name', 'description', 'category']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        
        result = db.careers.insert_one(data)
        
        return jsonify({
            'message': 'Career added successfully',
            'career_id': str(result.inserted_id)
        }), 201
        
    except Exception as e:
        print(f"❌ Add career error: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/careers/<career_id>', methods=['PUT', 'OPTIONS'])
@admin_required
def update_career(career_id):
    """Update career details"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        from app import db
        
        data = request.json
        data['updated_at'] = datetime.utcnow()
        
        result = db.careers.update_one(
            {'_id': ObjectId(career_id)},
            {'$set': data}
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'Career not found'}), 404
        
        return jsonify({'message': 'Career updated successfully'}), 200
        
    except Exception as e:
        print(f"❌ Update career error: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/careers/<career_id>', methods=['DELETE', 'OPTIONS'])
@admin_required
def delete_career(career_id):
    """Delete career"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        from app import db
        
        result = db.careers.delete_one({'_id': ObjectId(career_id)})
        
        if result.deleted_count == 0:
            return jsonify({'error': 'Career not found'}), 404
        
        return jsonify({'message': 'Career deleted successfully'}), 200
        
    except Exception as e:
        print(f"❌ Delete career error: {e}")
        return jsonify({'error': str(e)}), 500


# ==================== COLLEGE MANAGEMENT ====================

@admin_bp.route('/colleges', methods=['GET', 'OPTIONS'])
@admin_required
def get_all_colleges():
    """Get all colleges"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        from app import db
        
        colleges = list(db.colleges.find().sort('name', 1))
        
        for college in colleges:
            college['_id'] = str(college['_id'])
        
        return jsonify({'colleges': colleges}), 200
        
    except Exception as e:
        print(f"❌ Get colleges error: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/colleges', methods=['POST', 'OPTIONS'])
@admin_required
def add_college():
    """Add new college"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        from app import db
        
        data = request.json
        
        # Validate required fields
        required_fields = ['name', 'location', 'type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        
        result = db.colleges.insert_one(data)
        
        return jsonify({
            'message': 'College added successfully',
            'college_id': str(result.inserted_id)
        }), 201
        
    except Exception as e:
        print(f"❌ Add college error: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/colleges/<college_id>', methods=['PUT', 'OPTIONS'])
@admin_required
def update_college(college_id):
    """Update college details"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        from app import db
        
        data = request.json
        data['updated_at'] = datetime.utcnow()
        
        result = db.colleges.update_one(
            {'_id': ObjectId(college_id)},
            {'$set': data}
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'College not found'}), 404
        
        return jsonify({'message': 'College updated successfully'}), 200
        
    except Exception as e:
        print(f"❌ Update college error: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/colleges/<college_id>', methods=['DELETE', 'OPTIONS'])
@admin_required
def delete_college(college_id):
    """Delete college"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        from app import db
        
        result = db.colleges.delete_one({'_id': ObjectId(college_id)})
        
        if result.deleted_count == 0:
            return jsonify({'error': 'College not found'}), 404
        
        return jsonify({'message': 'College deleted successfully'}), 200
        
    except Exception as e:
        print(f"❌ Delete college error: {e}")
        return jsonify({'error': str(e)}), 500


# ==================== ANALYTICS ====================

@admin_bp.route('/analytics/users', methods=['GET', 'OPTIONS'])
@admin_required
def get_user_analytics():
    """Get user growth analytics"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        from app import db
        
        pipeline = [
            {
                '$group': {
                    '_id': {
                        'year': {'$year': '$created_at'},
                        'month': {'$month': '$created_at'},
                        'role': '$role'
                    },
                    'count': {'$sum': 1}
                }
            },
            {'$sort': {'_id.year': 1, '_id.month': 1}}
        ]
        
        results = list(db.users.aggregate(pipeline))
        
        return jsonify({'analytics': results}), 200
        
    except Exception as e:
        print(f"❌ Analytics error: {e}")
        return jsonify({'error': str(e)}), 500