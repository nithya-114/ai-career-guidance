from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
import bcrypt
import jwt
from bson import ObjectId
import re

from models.schemas import UserModel

auth_bp = Blueprint('auth', __name__)

# Helper functions
def hash_password(password):
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def generate_token(user_id, role):
    """Generate JWT token"""
    payload = {
        'user_id': str(user_id),
        'role': role,
        'exp': datetime.utcnow() + timedelta(days=7),  # Token expires in 7 days
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    return True, ""

# Routes
@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    POST /api/auth/register
    Body: { "name": "John Doe", "email": "john@example.com", "password": "password123", "role": "student" }
    """
    try:
        db = current_app.config['DB']
        data = request.json
        
        # Validate required fields
        required_fields = ['name', 'email', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate email format
        if not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password strength
        is_valid, msg = validate_password(data['password'])
        if not is_valid:
            return jsonify({'error': msg}), 400
        
        # Check if user already exists
        if db.users.find_one({'email': data['email'].lower()}):
            return jsonify({'error': 'Email already registered'}), 409
        
        # Hash password
        hashed_password = hash_password(data['password'])
        
        # Create user document
        role = data.get('role', 'student')
        if role not in ['student', 'counsellor', 'admin']:
            role = 'student'
        
        user = UserModel.create_user(
            name=data['name'],
            email=data['email'],
            password=hashed_password,
            role=role
        )
        
        # Insert into database
        result = db.users.insert_one(user)
        user_id = result.inserted_id
        
        # Generate token
        token = generate_token(user_id, role)
        
        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user': {
                'id': str(user_id),
                'name': user['name'],
                'email': user['email'],
                'role': user['role']
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user
    POST /api/auth/login
    Body: { "email": "john@example.com", "password": "password123" }
    """
    try:
        db = current_app.config['DB']
        data = request.json
        
        # Validate required fields
        if not data.get('login') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user
        user = db.users.find_one({'email': data['email'].lower()})
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Verify password
        if not verify_password(data['password'], user['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Check if user is active
        if not user.get('is_active', True):
            return jsonify({'error': 'Account is deactivated'}), 403
        
        # Update last login
        db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'last_login': datetime.utcnow()}}
        )
        
        # Generate token
        token = generate_token(user['_id'], user['role'])
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email'],
                'role': user['role']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """
    Request password reset
    POST /api/auth/forgot-password
    Body: { "email": "john@example.com" }
    """
    try:
        db = current_app.config['DB']
        data = request.json
        
        if not data.get('email'):
            return jsonify({'error': 'Email is required'}), 400
        
        # Check if user exists
        user = db.users.find_one({'email': data['email'].lower()})
        
        # Always return success to prevent email enumeration
        # In production, send actual reset email here
        return jsonify({
            'message': 'If the email exists, a password reset link has been sent'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """
    Reset password with token
    POST /api/auth/reset-password
    Body: { "token": "reset_token", "new_password": "newpass123" }
    """
    try:
        db = current_app.config['DB']
        data = request.json
        
        # Validate required fields
        if not data.get('token') or not data.get('new_password'):
            return jsonify({'error': 'Token and new password are required'}), 400
        
        # Validate new password
        is_valid, msg = validate_password(data['new_password'])
        if not is_valid:
            return jsonify({'error': msg}), 400
        
        # In production, verify reset token here
        # For now, we'll use a simple implementation
        
        return jsonify({
            'message': 'Password reset functionality will be implemented with email service'
        }), 501
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/verify-token', methods=['GET'])
def verify_token():
    """
    Verify if token is valid
    GET /api/auth/verify-token
    Headers: Authorization: Bearer <token>
    """
    try:
        # Get token from header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        
        # Decode token
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        
        return jsonify({
            'valid': True,
            'user_id': payload['user_id'],
            'role': payload['role']
        }), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/change-password', methods=['POST'])
def change_password():
    """
    Change password for logged-in user
    POST /api/auth/change-password
    Headers: Authorization: Bearer <token>
    Body: { "current_password": "oldpass", "new_password": "newpass123" }
    """
    try:
        db = current_app.config['DB']
        
        # Get token from header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Unauthorized'}), 401
        
        token = auth_header.split(' ')[1]
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        
        user_id = ObjectId(payload['user_id'])
        data = request.json
        
        # Validate required fields
        if not data.get('current_password') or not data.get('new_password'):
            return jsonify({'error': 'Current and new passwords are required'}), 400
        
        # Validate new password
        is_valid, msg = validate_password(data['new_password'])
        if not is_valid:
            return jsonify({'error': msg}), 400
        
        # Get user
        user = db.users.find_one({'_id': user_id})
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Verify current password
        if not verify_password(data['current_password'], user['password']):
            return jsonify({'error': 'Current password is incorrect'}), 401
        
        # Hash new password
        new_hashed = hash_password(data['new_password'])
        
        # Update password
        db.users.update_one(
            {'_id': user_id},
            {
                '$set': {
                    'password': new_hashed,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500