from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from bson import ObjectId
import jwt

admin_bp = Blueprint('admin', __name__)


# Helper function to verify admin
def verify_admin(request):
    """Verify if user is admin"""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return None, {'error': 'No token provided'}, 401
    
    token = auth_header.split(' ')[1]
    
    try:
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        
        if payload.get('role') != 'admin':
            return None, {'error': 'Unauthorized - Admin access required'}, 403
        
        return payload['user_id'], None, None
    except:
        return None, {'error': 'Invalid token'}, 401


# ==================== USER MANAGEMENT ====================

@admin_bp.route('/users', methods=['GET'])
def get_all_users():
    """
    Get all users (admin only)
    GET /api/admin/users?role=student&limit=50&skip=0
    """
    try:
        db = current_app.config['DB']
        
        # Verify admin
        user_id, error, status = verify_admin(request)
        if error:
            return jsonify(error), status
        
        # Get query parameters
        role = request.args.get('role')
        limit = int(request.args.get('limit', 50))
        skip = int(request.args.get('skip', 0))
        
        # Build query
        query = {}
        if role:
            query['role'] = role
        
        # Get users
        users = list(db.users.find(query, {'password': 0}).skip(skip).limit(limit))
        
        # Convert ObjectId
        for user in users:
            user['_id'] = str(user['_id'])
            if 'created_at' in user:
                user['created_at'] = user['created_at'].isoformat()
        
        total = db.users.count_documents(query)
        
        return jsonify({
            'users': users,
            'total': total,
            'limit': limit,
            'skip': skip
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a user (admin only)
    DELETE /api/admin/users/<user_id>
    """
    try:
        db = current_app.config['DB']
        
        # Verify admin
        admin_id, error, status = verify_admin(request)
        if error:
            return jsonify(error), status
        
        result = db.users.delete_one({'_id': ObjectId(user_id)})
        
        if result.deleted_count == 0:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'message': 'User deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== CAREER MANAGEMENT ====================

@admin_bp.route('/careers', methods=['POST'])
def add_career():
    """
    Add new career (admin only)
    POST /api/admin/careers
    Body: {
        "name": "Data Scientist",
        "category": "Technology",
        "description": "...",
        ...
    }
    """
    try:
        db = current_app.config['DB']
        
        # Verify admin
        user_id, error, status = verify_admin(request)
        if error:
            return jsonify(error), status
        
        data = request.json
        
        # Validate required fields
        required = ['name', 'category', 'description']
        for field in required:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Add timestamps
        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        
        result = db.careers.insert_one(data)
        
        return jsonify({
            'message': 'Career added successfully',
            'career_id': str(result.inserted_id)
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/careers/<career_id>', methods=['PUT'])
def update_career(career_id):
    """
    Update career (admin only)
    PUT /api/admin/careers/<career_id>
    """
    try:
        db = current_app.config['DB']
        
        # Verify admin
        user_id, error, status = verify_admin(request)
        if error:
            return jsonify(error), status
        
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
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/careers/<career_id>', methods=['DELETE'])
def delete_career(career_id):
    """
    Delete career (admin only)
    DELETE /api/admin/careers/<career_id>
    """
    try:
        db = current_app.config['DB']
        
        # Verify admin
        user_id, error, status = verify_admin(request)
        if error:
            return jsonify(error), status
        
        result = db.careers.delete_one({'_id': ObjectId(career_id)})
        
        if result.deleted_count == 0:
            return jsonify({'error': 'Career not found'}), 404
        
        return jsonify({'message': 'Career deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== COURSE MANAGEMENT ====================

@admin_bp.route('/courses', methods=['POST'])
def add_course():
    """
    Add new course (admin only)
    POST /api/admin/courses
    """
    try:
        db = current_app.config['DB']
        
        # Verify admin
        user_id, error, status = verify_admin(request)
        if error:
            return jsonify(error), status
        
        data = request.json
        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        
        result = db.courses.insert_one(data)
        
        return jsonify({
            'message': 'Course added successfully',
            'course_id': str(result.inserted_id)
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/colleges', methods=['POST'])
def add_college():
    """
    Add new college (admin only)
    POST /api/admin/colleges
    """
    try:
        db = current_app.config['DB']
        
        # Verify admin
        user_id, error, status = verify_admin(request)
        if error:
            return jsonify(error), status
        
        data = request.json
        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        
        result = db.colleges.insert_one(data)
        
        return jsonify({
            'message': 'College added successfully',
            'college_id': str(result.inserted_id)
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== STATISTICS ====================

@admin_bp.route('/stats', methods=['GET'])
def get_system_stats():
    """
    Get system statistics (admin only)
    GET /api/admin/stats
    """
    try:
        db = current_app.config['DB']
        
        # Verify admin
        user_id, error, status = verify_admin(request)
        if error:
            return jsonify(error), status
        
        stats = {
            'users': {
                'total': db.users.count_documents({}),
                'students': db.users.count_documents({'role': 'student'}),
                'counsellors': db.users.count_documents({'role': 'counsellor'}),
                'admins': db.users.count_documents({'role': 'admin'}),
            },
            'careers': db.careers.count_documents({}),
            'courses': db.courses.count_documents({}),
            'colleges': db.colleges.count_documents({}),
            'quizzes_taken': db.quiz_results.count_documents({}),
            'chat_sessions': db.chat_history.count_documents({}),
            'appointments': db.appointments.count_documents({}),
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500