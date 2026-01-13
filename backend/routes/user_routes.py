from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import jwt
from bson import ObjectId

user_bp = Blueprint('user', __name__)

# Helper function to get user from token
def get_user_from_token(request):
    """Extract user ID from JWT token"""
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
        return payload['user_id'], None, None
    except jwt.ExpiredSignatureError:
        return None, {'error': 'Token has expired'}, 401
    except jwt.InvalidTokenError:
        return None, {'error': 'Invalid token'}, 401


@user_bp.route('/profile', methods=['GET'])
def get_profile():
    """
    Get user profile
    GET /api/user/profile
    Headers: Authorization: Bearer <token>
    """
    try:
        db = current_app.config['DB']
        
        # Get user from token
        user_id, error, status = get_user_from_token(request)
        if error:
            return jsonify(error), status
        
        # Get user from database
        user = db.users.find_one({'_id': ObjectId(user_id)})
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Return user profile (exclude password)
        profile = {
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email'],
            'role': user['role'],
            'phone': user.get('phone'),
            'location': user.get('location'),
            'profile': user.get('profile', {}),
            'created_at': user['created_at'].isoformat(),
            'last_login': user.get('last_login').isoformat() if user.get('last_login') else None,
            'email_verified': user.get('email_verified', False)
        }
        
        return jsonify(profile), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/profile', methods=['PUT'])
def update_profile():
    """
    Update user profile
    PUT /api/user/profile
    Headers: Authorization: Bearer <token>
    Body: {
        "phone": "1234567890",
        "location": "Mumbai",
        "profile": {
            "education": "12th",
            "interests": ["technology", "science"],
            "goals": "Become a software engineer",
            "subjects": ["Mathematics", "Physics"],
            "skills": ["programming", "problem-solving"]
        }
    }
    """
    try:
        db = current_app.config['DB']
        data = request.json
        
        # Get user from token
        user_id, error, status = get_user_from_token(request)
        if error:
            return jsonify(error), status
        
        # Build update document
        update_doc = {
            'updated_at': datetime.utcnow()
        }
        
        # Update allowed fields
        allowed_fields = ['phone', 'location', 'profile']
        for field in allowed_fields:
            if field in data:
                update_doc[field] = data[field]
        
        # Update user
        result = db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_doc}
        )
        
        if result.modified_count == 0:
            return jsonify({'message': 'No changes made'}), 200
        
        # Get updated user
        user = db.users.find_one({'_id': ObjectId(user_id)})
        
        profile = {
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email'],
            'phone': user.get('phone'),
            'location': user.get('location'),
            'profile': user.get('profile', {}),
            'updated_at': user['updated_at'].isoformat()
        }
        
        return jsonify({
            'message': 'Profile updated successfully',
            'profile': profile
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/profile/interests', methods=['POST'])
def add_interests():
    """
    Add interests to user profile
    POST /api/user/profile/interests
    Headers: Authorization: Bearer <token>
    Body: { "interests": ["technology", "music", "sports"] }
    """
    try:
        db = current_app.config['DB']
        data = request.json
        
        # Get user from token
        user_id, error, status = get_user_from_token(request)
        if error:
            return jsonify(error), status
        
        if not data.get('interests') or not isinstance(data['interests'], list):
            return jsonify({'error': 'interests must be an array'}), 400
        
        # Update user interests
        result = db.users.update_one(
            {'_id': ObjectId(user_id)},
            {
                '$addToSet': {
                    'profile.interests': {'$each': data['interests']}
                },
                '$set': {'updated_at': datetime.utcnow()}
            }
        )
        
        return jsonify({'message': 'Interests added successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/profile/skills', methods=['POST'])
def add_skills():
    """
    Add skills to user profile
    POST /api/user/profile/skills
    Headers: Authorization: Bearer <token>
    Body: { "skills": ["programming", "communication"] }
    """
    try:
        db = current_app.config['DB']
        data = request.json
        
        # Get user from token
        user_id, error, status = get_user_from_token(request)
        if error:
            return jsonify(error), status
        
        if not data.get('skills') or not isinstance(data['skills'], list):
            return jsonify({'error': 'skills must be an array'}), 400
        
        # Update user skills
        result = db.users.update_one(
            {'_id': ObjectId(user_id)},
            {
                '$addToSet': {
                    'profile.skills': {'$each': data['skills']}
                },
                '$set': {'updated_at': datetime.utcnow()}
            }
        )
        
        return jsonify({'message': 'Skills added successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/dashboard-stats', methods=['GET'])
def get_dashboard_stats():
    """
    Get user dashboard statistics
    GET /api/user/dashboard-stats
    Headers: Authorization: Bearer <token>
    """
    try:
        db = current_app.config['DB']
        
        # Get user from token
        user_id, error, status = get_user_from_token(request)
        if error:
            return jsonify(error), status
        
        user_id_str = str(user_id)
        
        # Get statistics
        stats = {
            'profile_completion': 0,
            'quizzes_taken': 0,
            'chat_sessions': 0,
            'recommendations_received': 0,
        }
        
        # Calculate profile completion
        user = db.users.find_one({'_id': ObjectId(user_id)})
        if user:
            fields = ['name', 'email', 'phone', 'location']
            profile_fields = ['education', 'interests', 'goals']
            
            completed = 0
            total = len(fields) + len(profile_fields)
            
            for field in fields:
                if user.get(field):
                    completed += 1
            
            profile = user.get('profile', {})
            for field in profile_fields:
                if profile.get(field):
                    completed += 1
            
            stats['profile_completion'] = int((completed / total) * 100)
        
        # Count quizzes
        stats['quizzes_taken'] = db.quiz_results.count_documents({
            'user_id': user_id_str
        })
        
        # Count chat sessions
        stats['chat_sessions'] = db.chat_history.count_documents({
            'user_id': user_id_str
        })
        
        # Count recommendations
        stats['recommendations_received'] = db.career_recommendations.count_documents({
            'user_id': user_id_str
        })
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/activity', methods=['GET'])
def get_recent_activity():
    """
    Get user's recent activity
    GET /api/user/activity?limit=10
    Headers: Authorization: Bearer <token>
    """
    try:
        db = current_app.config['DB']
        
        # Get user from token
        user_id, error, status = get_user_from_token(request)
        if error:
            return jsonify(error), status
        
        limit = int(request.args.get('limit', 10))
        user_id_str = str(user_id)
        
        activities = []
        
        # Get recent quiz activities
        quizzes = db.quiz_results.find(
            {'user_id': user_id_str}
        ).sort('completed_at', -1).limit(limit)
        
        for quiz in quizzes:
            activities.append({
                'type': 'quiz',
                'description': f"Completed {quiz['quiz_type']} quiz",
                'timestamp': quiz['completed_at'].isoformat()
            })
        
        # Get recent chat sessions
        chats = db.chat_history.find(
            {'user_id': user_id_str}
        ).sort('last_message_at', -1).limit(limit)
        
        for chat in chats:
            activities.append({
                'type': 'chat',
                'description': 'Chat session with AI counselor',
                'timestamp': chat['last_message_at'].isoformat()
            })
        
        # Sort all activities by timestamp
        activities.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return jsonify({
            'activities': activities[:limit]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500