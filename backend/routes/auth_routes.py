from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
import bcrypt
import jwt
from bson import ObjectId
import re

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
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, ""

# Routes
@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user (student or counsellor)
    POST /api/auth/register
    """
    try:
        db = current_app.config['DB']
        data = request.json
        # DEBUG - See what we receive
        print("\n" + "=" * 80)
        print("🔍 BACKEND RECEIVED:")
        import json
        print(json.dumps(data, indent=2, default=str))
        
        print("\n📋 PROFILE CHECK:")
        if 'profile' in data:
            print(f"✅ Profile exists: {data['profile']}")
            if 'specialization' in data['profile']:
                print(f"✅ Specialization: '{data['profile']['specialization']}'")
            else:
                print(f"❌ NO specialization in profile!")
        else:
            print(f"❌ NO profile in data!")
        print("=" * 80 + "\n")
        print("=" * 60)
        print("📝 REGISTRATION REQUEST RECEIVED")
        print(f"Role: {data.get('role')}")
        print(f"Name: {data.get('name')}")
        print(f"Email: {data.get('email')}")
        print(f"Username: {data.get('username')}")
        print(f"Has profile: {bool(data.get('profile'))}")
        if data.get('profile'):
            print(f"Profile data: {data.get('profile')}")
        print("=" * 60)
        
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
        
        # Check if email already exists
        if db.users.find_one({'email': data['email'].lower()}):
            return jsonify({'error': 'Email already registered'}), 409
        
        # Check if username already exists
        username = data.get('username')
        if username:
            if db.users.find_one({'username': username.lower()}):
                return jsonify({'error': 'Username already taken'}), 409
        
        # Hash password
        hashed_password = hash_password(data['password'])
        
        # Determine role
        role = data.get('role', 'student')
        if role not in ['student', 'counsellor', 'admin']:
            role = 'student'
        
        # Create base user document
        user = {
            'name': data['name'],
            'email': data['email'].lower(),
            'username': username.lower() if username else data['email'].split('@')[0].lower(),
            'password': hashed_password,
            'role': role,
            'is_active': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        # Add role-specific fields
        if role == 'counsellor':
            print("🔍 Processing COUNSELLOR registration...")
            
            # Validate counsellor-specific required fields
            if not data.get('phone'):
                return jsonify({'error': 'Phone number is required for counsellors'}), 400
            
            # Get profile data
            profile = data.get('profile', {})
            
            print(f"🔍 Profile received: {profile}")
            
            # Validate required profile fields
            if not profile.get('specialization'):
                return jsonify({'error': 'Specialization is required for counsellors'}), 400
            
            if profile.get('experience') is None:
                return jsonify({'error': 'Experience is required for counsellors'}), 400
            
            if not profile.get('education'):
                return jsonify({'error': 'Education is required for counsellors'}), 400
            
            # Add counsellor fields
            user['phone'] = data['phone']
            user['profile'] = {
                'specialization': profile['specialization'],
                'experience': int(profile.get('experience', 0)),
                'education': profile['education'],
                'bio': profile.get('bio', ''),
                'hourly_rate': int(profile.get('hourly_rate', 500)),
                'rating': float(profile.get('rating', 4.5)),
                'sessions_conducted': int(profile.get('sessions_conducted', 0))
            }
            
            print(f"✅ Counsellor profile created:")
            print(f"   Specialization: {user['profile']['specialization']}")
            print(f"   Experience: {user['profile']['experience']} years")
            print(f"   Education: {user['profile']['education']}")
            print(f"   Hourly Rate: ₹{user['profile']['hourly_rate']}")
            
        elif role == 'student':
            print("🔍 Processing STUDENT registration...")
            
            # Add student-specific fields
            user['dob'] = data.get('dob')
            user['class_level'] = data.get('class_level')
            user['school'] = data.get('school')
            user['location'] = data.get('location')
            user['profile'] = {
                'interests': data.get('interests', []),
                'goals': data.get('goals', ''),
                'subjects': data.get('subjects', []),
                'skills': data.get('skills', [])
            }
            
            print(f"✅ Student profile created:")
            print(f"   Class: {user.get('class_level', 'Not specified')}")
            print(f"   School: {user.get('school', 'Not specified')}")
        
        # Insert into database
        result = db.users.insert_one(user)
        user_id = result.inserted_id
        
        print(f"✅ User inserted into database with ID: {user_id}")
        
        # Generate token
        token = generate_token(user_id, role)
        
        # Return response (exclude password)
        del user['password']
        user['_id'] = str(user_id)
        
        print(f"✅ Registration successful for: {user['email']}")
        print("=" * 60)
        
        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user': {
                'id': str(user_id),
                'name': user['name'],
                'email': user['email'],
                'username': user['username'],
                'role': user['role']
            }
        }), 201
        
    except Exception as e:
        print(f"❌ REGISTRATION ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/check-username', methods=['POST'])
def check_username():
    """
    Check if username is available
    POST /api/auth/check-username
    Body: { "username": "johndoe" }
    """
    try:
        db = current_app.config['DB']
        data = request.json
        
        username = data.get('username', '').lower()
        
        if not username or len(username) < 3:
            return jsonify({'available': False, 'message': 'Username must be at least 3 characters'}), 200
        
        # Check if username exists
        exists = db.users.find_one({'username': username}) is not None
        
        return jsonify({
            'available': not exists,
            'message': 'Username is available' if not exists else 'Username is already taken'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/check-email', methods=['POST'])
def check_email():
    """
    Check if email is available
    POST /api/auth/check-email
    Body: { "email": "john@example.com" }
    """
    try:
        db = current_app.config['DB']
        data = request.json
        
        email = data.get('email', '').lower()
        
        if not email or not validate_email(email):
            return jsonify({'available': False, 'message': 'Invalid email format'}), 200
        
        # Check if email exists
        exists = db.users.find_one({'email': email}) is not None
        
        return jsonify({
            'available': not exists,
            'message': 'Email is available' if not exists else 'Email is already registered'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user
    POST /api/auth/login
    Body: { "login": "john@example.com", "password": "password123" }
    """
    try:
        db = current_app.config['DB']
        data = request.json
        
        # Validate required fields
        if not data.get('login') or not data.get('password'):
            return jsonify({'error': 'Email/Username and password are required'}), 400
        
        # Find user by email or username
        login_input = data['login'].lower()
        
        user = db.users.find_one({
            "$or": [
                {"email": login_input},
                {"username": login_input}
            ]
        })
        
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
        
        print(f"✅ Login successful: {user['email']} (Role: {user['role']})")
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email'],
                'username': user.get('username', ''),
                'role': user['role']
            }
        }), 200
        
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
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