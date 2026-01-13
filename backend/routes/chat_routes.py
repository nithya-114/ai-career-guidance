from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from bson import ObjectId
import jwt

chat_bp = Blueprint('chat', __name__)


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
    except:
        return None, {'error': 'Invalid token'}, 401


@chat_bp.route('/chat', methods=['POST'])
def send_message():
    """
    Send message to chatbot
    POST /api/chat
    Headers: Authorization: Bearer <token> (optional)
    Body: {
        "message": "What are my interests?",
        "session_id": "session_123",
        "user_id": "optional_user_id"
    }
    """
    try:
        db = current_app.config['DB']
        data = request.json
        
        # Get user from token (optional for chat)
        user_id = data.get('user_id')  # Can be passed directly for demo
        if not user_id:
            user_id, error, status = get_user_from_token(request)
            if error:
                # Allow anonymous chat for demo
                user_id = 'anonymous'
        
        if not data.get('message'):
            return jsonify({'error': 'Message is required'}), 400
        
        session_id = data.get('session_id', f"session_{user_id}_{datetime.utcnow().timestamp()}")
        
        # Simple response logic (will be enhanced with NLP)
        user_message = data['message'].lower()
        
        # Basic intent detection
        intent = 'general'
        if any(word in user_message for word in ['interest', 'like', 'enjoy', 'love']):
            intent = 'interests'
        elif any(word in user_message for word in ['skill', 'good at', 'talented']):
            intent = 'skills'
        elif any(word in user_message for word in ['career', 'job', 'profession', 'work']):
            intent = 'careers'
        elif any(word in user_message for word in ['college', 'university', 'institution']):
            intent = 'education'
        
        # Generate response based on intent
        responses = {
            'interests': "That's great! Understanding your interests is the first step. What subjects or activities do you enjoy the most? For example, do you like working with technology, helping people, being creative, or solving problems?",
            'skills': "Skills are very important! Tell me more about what you're naturally good at. Do you excel in communication, analytical thinking, creativity, or hands-on activities?",
            'careers': "Let's explore career options together! Based on what you've told me, I can suggest careers that match your profile. Have you completed the aptitude and personality tests yet?",
            'education': "Education is key to your career goals! What level of education are you currently at? Are you looking for undergraduate programs, or are you already in college?",
            'general': "I'm here to help you discover the perfect career path! To give you the best recommendations, I'd like to know more about your interests, skills, and goals. What would you like to discuss first?"
        }
        
        bot_response = responses.get(intent, responses['general'])
        
        # Save to chat history
        chat_session = db.chat_history.find_one({
            'user_id': str(user_id),
            'session_id': session_id
        })
        
        if not chat_session:
            # Create new session
            chat_session = {
                'user_id': str(user_id),
                'session_id': session_id,
                'messages': [],
                'started_at': datetime.utcnow(),
                'last_message_at': datetime.utcnow(),
                'is_active': True
            }
            db.chat_history.insert_one(chat_session)
        
        # Add messages
        db.chat_history.update_one(
            {'session_id': session_id},
            {
                '$push': {
                    'messages': {
                        '$each': [
                            {
                                'type': 'user',
                                'text': data['message'],
                                'timestamp': datetime.utcnow()
                            },
                            {
                                'type': 'bot',
                                'text': bot_response,
                                'timestamp': datetime.utcnow(),
                                'intent': intent
                            }
                        ]
                    }
                },
                '$set': {'last_message_at': datetime.utcnow()}
            }
        )
        
        return jsonify({
            'response': bot_response,
            'intent': intent,
            'session_id': session_id
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/chat/history/<session_id>', methods=['GET'])
def get_chat_history(session_id):
    """
    Get chat history for a session
    GET /api/chat/history/<session_id>
    """
    try:
        db = current_app.config['DB']
        
        chat_session = db.chat_history.find_one({'session_id': session_id})
        
        if not chat_session:
            return jsonify({'error': 'Session not found'}), 404
        
        # Convert datetime objects
        for message in chat_session.get('messages', []):
            if 'timestamp' in message:
                message['timestamp'] = message['timestamp'].isoformat()
        
        return jsonify({
            'session_id': session_id,
            'messages': chat_session.get('messages', []),
            'started_at': chat_session['started_at'].isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/chat/sessions/<user_id>', methods=['GET'])
def get_user_chat_sessions(user_id):
    """
    Get all chat sessions for a user
    GET /api/chat/sessions/<user_id>
    """
    try:
        db = current_app.config['DB']
        
        sessions = list(db.chat_history.find(
            {'user_id': user_id}
        ).sort('last_message_at', -1))
        
        for session in sessions:
            session['_id'] = str(session['_id'])
            session['started_at'] = session['started_at'].isoformat()
            session['last_message_at'] = session['last_message_at'].isoformat()
            # Don't send all messages, just metadata
            session['message_count'] = len(session.get('messages', []))
            session.pop('messages', None)
        
        return jsonify({
            'sessions': sessions,
            'total': len(sessions)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500