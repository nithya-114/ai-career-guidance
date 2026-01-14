"""
Admin Routes - User, Counsellor, Career, College Management & Analytics
"""

from flask import Blueprint, request, jsonify
from functools import wraps
from bson import ObjectId
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)

# Admin authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from app import get_current_user
        
        user = get_current_user()
        if not user or user.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def get_dashboard_stats():
    """Get admin dashboard statistics"""
    try:
        from app import db
        
        # Count users by role
        total_users = db.users.count_documents({})
        total_students = db.users.count_documents({'role': 'student'})
        total_counsellors = db.users.count_documents({'role': 'counsellor'})
        
        # Count careers and colleges
        total_careers = db.careers.count_documents({})
        total_colleges = db.colleges.count_documents({})
        
        # Count sessions (from appointments or bookings)
        total_sessions = db.appointments.count_documents({}) if 'appointments' in db.list_collection_names() else 0
        
        # Calculate revenue (sum of all completed sessions)
        revenue_pipeline = [
            {'$match': {'status': 'completed'}},
            {'$group': {'_id': None, 'total': {'$sum': '$amount'}}}
        ]
        revenue_result = list(db.appointments.aggregate(revenue_pipeline)) if 'appointments' in db.list_collection_names() else []
        revenue = revenue_result[0]['total'] if revenue_result else 0
        
        # Active users (logged in last 24 hours)
        twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
        active_now = db.users.count_documents({
            'last_login': {'$gte': twenty_four_hours_ago}
        }) if 'last_login' in db.users.find_one({}) or {} else 0
        
        return jsonify({
            'totalUsers': total_users,
            'totalStudents': total_students,
            'totalCounsellors': total_counsellors,
            'totalSessions': total_sessions,
            'totalCareers': total_careers,
            'totalColleges': total_colleges,
            'revenue': revenue,
            'activeNow': active_now
        }), 200
        
    except Exception as e:
        print(f"Error getting dashboard stats: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    """Get all users with filters"""
    try:
        from app import db
        
        # Get query parameters
        role = request.args.get('role')
        search = request.args.get('search')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        
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
        users = list(db.users.find(query)
                    .skip((page - 1) * limit)
                    .limit(limit)
                    .sort('created_at', -1))
        
        # Remove password field
        for user in users:
            user['_id'] = str(user['_id'])
            user.pop('password', None)
        
        # Get total count
        total = db.users.count_documents(query)
        
        return jsonify({
            'users': users,
            'total': total,
            'page': page,
            'pages': (total + limit - 1) // limit
        }), 200
        
    except Exception as e:
        print(f"Error getting users: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/users/<user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    """Update user details"""
    try:
        from app import db
        
        data = request.json
        
        # Don't allow password update through this route
        data.pop('password', None)
        data.pop('role', None)  # Prevent role change
        
        data['updated_at'] = datetime.utcnow()
        
        result = db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': data}
        )
        
        if result.modified_count == 0:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'message': 'User updated successfully'}), 200
        
    except Exception as e:
        print(f"Error updating user: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/users/<user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """Delete user"""
    try:
        from app import db
        
        result = db.users.delete_one({'_id': ObjectId(user_id)})
        
        if result.deleted_count == 0:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'message': 'User deleted successfully'}), 200
        
    except Exception as e:
        print(f"Error deleting user: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/counsellors', methods=['GET'])
@admin_required
def get_all_counsellors():
    """Get all counsellors with their stats"""
    try:
        from app import db
        
        counsellors = list(db.users.find({'role': 'counsellor'}).sort('created_at', -1))
        
        for counsellor in counsellors:
            counsellor['_id'] = str(counsellor['_id'])
            counsellor.pop('password', None)
            
            # Get session count for each counsellor
            sessions = db.appointments.count_documents({
                'counsellor_id': str(counsellor['_id'])
            }) if 'appointments' in db.list_collection_names() else 0
            
            counsellor['total_sessions'] = sessions
        
        return jsonify({'counsellors': counsellors}), 200
        
    except Exception as e:
        print(f"Error getting counsellors: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/counsellors/<counsellor_id>/approve', methods=['PUT'])
@admin_required
def approve_counsellor(counsellor_id):
    """Approve or reject counsellor"""
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
        
        if result.modified_count == 0:
            return jsonify({'error': 'Counsellor not found'}), 404
        
        return jsonify({
            'message': f'Counsellor {"approved" if approved else "rejected"} successfully'
        }), 200
        
    except Exception as e:
        print(f"Error approving counsellor: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/careers', methods=['GET'])
@admin_required
def get_all_careers():
    """Get all careers"""
    try:
        from app import db
        
        careers = list(db.careers.find().sort('title', 1))
        
        for career in careers:
            career['_id'] = str(career['_id'])
        
        return jsonify({'careers': careers}), 200
        
    except Exception as e:
        print(f"Error getting careers: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/careers', methods=['POST'])
@admin_required
def add_career():
    """Add new career"""
    try:
        from app import db
        
        data = request.json
        
        # Validate required fields
        required_fields = ['title', 'description', 'category']
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
        print(f"Error adding career: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/careers/<career_id>', methods=['PUT'])
@admin_required
def update_career(career_id):
    """Update career details"""
    try:
        from app import db
        
        data = request.json
        data['updated_at'] = datetime.utcnow()
        
        result = db.careers.update_one(
            {'_id': ObjectId(career_id)},
            {'$set': data}
        )
        
        if result.modified_count == 0:
            return jsonify({'error': 'Career not found'}), 404
        
        return jsonify({'message': 'Career updated successfully'}), 200
        
    except Exception as e:
        print(f"Error updating career: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/careers/<career_id>', methods=['DELETE'])
@admin_required
def delete_career(career_id):
    """Delete career"""
    try:
        from app import db
        
        result = db.careers.delete_one({'_id': ObjectId(career_id)})
        
        if result.deleted_count == 0:
            return jsonify({'error': 'Career not found'}), 404
        
        return jsonify({'message': 'Career deleted successfully'}), 200
        
    except Exception as e:
        print(f"Error deleting career: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/colleges', methods=['GET'])
@admin_required
def get_all_colleges():
    """Get all colleges"""
    try:
        from app import db
        
        colleges = list(db.colleges.find().sort('name', 1))
        
        for college in colleges:
            college['_id'] = str(college['_id'])
        
        return jsonify({'colleges': colleges}), 200
        
    except Exception as e:
        print(f"Error getting colleges: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/colleges', methods=['POST'])
@admin_required
def add_college():
    """Add new college"""
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
        print(f"Error adding college: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/colleges/<college_id>', methods=['PUT'])
@admin_required
def update_college(college_id):
    """Update college details"""
    try:
        from app import db
        
        data = request.json
        data['updated_at'] = datetime.utcnow()
        
        result = db.colleges.update_one(
            {'_id': ObjectId(college_id)},
            {'$set': data}
        )
        
        if result.modified_count == 0:
            return jsonify({'error': 'College not found'}), 404
        
        return jsonify({'message': 'College updated successfully'}), 200
        
    except Exception as e:
        print(f"Error updating college: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/colleges/<college_id>', methods=['DELETE'])
@admin_required
def delete_college(college_id):
    """Delete college"""
    try:
        from app import db
        
        result = db.colleges.delete_one({'_id': ObjectId(college_id)})
        
        if result.deleted_count == 0:
            return jsonify({'error': 'College not found'}), 404
        
        return jsonify({'message': 'College deleted successfully'}), 200
        
    except Exception as e:
        print(f"Error deleting college: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/analytics/users', methods=['GET'])
@admin_required
def get_user_analytics():
    """Get user growth analytics"""
    try:
        from app import db
        
        # Get user registrations by month
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
        print(f"Error getting analytics: {e}")
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/analytics/sessions', methods=['GET'])
@admin_required
def get_session_analytics():
    """Get session analytics"""
    try:
        from app import db
        
        if 'appointments' not in db.list_collection_names():
            return jsonify({'analytics': []}), 200
        
        # Get sessions by month
        pipeline = [
            {
                '$group': {
                    '_id': {
                        'year': {'$year': '$created_at'},
                        'month': {'$month': '$created_at'},
                        'status': '$status'
                    },
                    'count': {'$sum': 1},
                    'revenue': {'$sum': '$amount'}
                }
            },
            {'$sort': {'_id.year': 1, '_id.month': 1}}
        ]
        
        results = list(db.appointments.aggregate(pipeline))
        
        return jsonify({'analytics': results}), 200
        
    except Exception as e:
        print(f"Error getting session analytics: {e}")
        return jsonify({'error': str(e)}), 500