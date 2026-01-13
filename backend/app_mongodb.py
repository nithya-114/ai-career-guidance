"""
AI Career Counselling Backend - MongoDB Version
Proper MongoDB integration with error handling
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
from pymongo import MongoClient
from bson import ObjectId
import bcrypt
import jwt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'career-counselling-secret-key-2026')
app.config['MONGODB_URI'] = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/career_counselling')

# Enable CORS
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# MongoDB Connection
try:
    client = MongoClient(app.config['MONGODB_URI'])
    db = client.get_database()
    
    # Test connection
    client.server_info()
    print("=" * 60)
    print("✅ Connected to MongoDB successfully!")
    print(f"📊 Database: {db.name}")
    print(f"👥 Users collection: {db.users.count_documents({})}")
    print("=" * 60)
except Exception as e:
    print("=" * 60)
    print(f"❌ MongoDB Connection Error: {e}")
    print("💡 Make sure MongoDB is running!")
    print("=" * 60)
    db = None


# ==================== HELPER FUNCTIONS ====================

def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def verify_password(password, hashed):
    """Verify password against hash"""
    try:
        # Handle both bytes and string formats
        if isinstance(password, bytes):
            password = password.decode('utf-8')
        if isinstance(hashed, str):
            hashed = hashed.encode('utf-8')
        
        result = bcrypt.checkpw(password.encode('utf-8'), hashed)
        print(f"🔐 Password verification: {'✅ SUCCESS' if result else '❌ FAILED'}")
        return result
    except Exception as e:
        print(f"❌ Password verification error: {e}")
        return False


def generate_token(user_id, role='student'):
    """Generate JWT token"""
    payload = {
        'user_id': str(user_id),
        'role': role,
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')


def get_user_from_token():
    """Extract user from Authorization header"""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return None, 'No token provided', 401
    
    token = auth_header.split(' ')[1]
    
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id'], None, None
    except jwt.ExpiredSignatureError:
        return None, 'Token expired', 401
    except jwt.InvalidTokenError:
        return None, 'Invalid token', 401


# ==================== AUTHENTICATION ROUTES ====================

@app.route('/api/auth/register', methods=['POST', 'OPTIONS'])
def register():
    """Register new user"""
    if request.method == 'OPTIONS':
        return '', 200
    
    if db is None:
        return jsonify({'error': 'Database connection error'}), 500
        
    try:
        data = request.json
        print(f"\n📝 Registration attempt: {data.get('email')}")
        
        # Validate required fields
        if not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400
        if not data.get('email'):
            return jsonify({'error': 'Email is required'}), 400
        if not data.get('password'):
            return jsonify({'error': 'Password is required'}), 400
        
        email = data['email'].lower().strip()
        
        # Check if user exists
        existing_user = db.users.find_one({'email': email})
        if existing_user:
            print(f"❌ Registration failed: Email {email} already exists")
            return jsonify({'error': 'Email already registered'}), 409
        
        # Validate password length
        if len(data['password']) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        # Hash password
        hashed_password = hash_password(data['password'])
        print(f"🔐 Password hashed successfully")
        
        # Create user document
        user = {
            'name': data['name'],
            'email': email,
            'password': hashed_password,
            'role': data.get('role', 'student'),
            'phone': data.get('phone'),
            'location': None,
            'profile': data.get('profile', {
                'education': None,
                'interests': [],
                'goals': None,
                'subjects': [],
                'skills': [],
                'specialization': data.get('profile', {}).get('specialization'),
                'experience': data.get('profile', {}).get('experience'),
                'bio': data.get('profile', {}).get('bio')
            }),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'is_active': True,
            'email_verified': False
        }
        
        # Insert into database
        result = db.users.insert_one(user)
        user_id = str(result.inserted_id)
        
        print(f"✅ User registered successfully: {email}")
        print(f"📊 Total users: {db.users.count_documents({})}\n")
        
        # Generate token
        token = generate_token(user_id, user['role'])
        
        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user': {
                'id': user_id,
                'name': user['name'],
                'email': user['email'],
                'role': user['role']
            }
        }), 201
        
    except Exception as e:
        print(f"❌ Registration error: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500


@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def login():
    """Login user"""
    if request.method == 'OPTIONS':
        return '', 200
    
    if db is None:
        return jsonify({'error': 'Database connection error'}), 500
        
    try:
        data = request.json
        print(f"\n🔐 Login attempt for: {data.get('email')}")
        
        # Validate
        if not data.get('email') or not data.get('password'):
            print("❌ Missing email or password\n")
            return jsonify({'error': 'Email and password are required'}), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        
        print(f"📧 Looking up user: {email}")
        
        # Find user by email
        user = db.users.find_one({'email': email})
        
        if not user:
            print(f"❌ Login failed: User {email} not found")
            print(f"💡 User might not be registered\n")
            return jsonify({'error': 'Invalid credentials'}), 401
        
        print(f"✅ User found: {user['name']}")
        print(f"👤 Role: {user.get('role', 'student')}")
        print(f"🔑 Password hash exists: {bool(user.get('password'))}")
        
        # Verify password
        stored_password = user.get('password')
        if not stored_password:
            print("❌ No password hash stored for user\n")
            return jsonify({'error': 'Invalid credentials'}), 401
        
        password_match = verify_password(password, stored_password)
        
        if not password_match:
            print(f"❌ Login failed: Incorrect password for {email}\n")
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Generate token
        user_id = str(user['_id'])
        token = generate_token(user_id, user.get('role', 'student'))
        
        print(f"✅ Login successful: {email}")
        print(f"🎫 Token generated for user: {user_id}\n")
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user_id,
                'name': user['name'],
                'email': user['email'],
                'role': user.get('role', 'student')
            }
        }), 200
        
    except Exception as e:
        print(f"❌ Login error: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Login failed: {str(e)}'}), 500


@app.route('/api/auth/verify-token', methods=['GET', 'OPTIONS'])
def verify_token():
    """Verify JWT token"""
    if request.method == 'OPTIONS':
        return '', 200
        
    user_id, error, status = get_user_from_token()
    
    if error:
        return jsonify({'error': error}), status
    
    return jsonify({
        'valid': True,
        'user_id': user_id
    }), 200


# ==================== USER PROFILE ROUTES ====================

@app.route('/api/user/profile', methods=['GET', 'OPTIONS'])
def get_profile():
    """Get user profile"""
    if request.method == 'OPTIONS':
        return '', 200
    
    if db is None:
        return jsonify({'error': 'Database connection error'}), 500
        
    try:
        user_id, error, status = get_user_from_token()
        if error:
            return jsonify({'error': error}), status
        
        user = db.users.find_one({'_id': ObjectId(user_id)})
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email'],
            'role': user.get('role', 'student'),
            'phone': user.get('phone'),
            'location': user.get('location'),
            'profile': user.get('profile', {}),
            'created_at': user.get('created_at').isoformat() if user.get('created_at') else None
        }), 200
        
    except Exception as e:
        print(f"❌ Get profile error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/user/profile', methods=['PUT', 'OPTIONS'])
def update_profile():
    """Update user profile"""
    if request.method == 'OPTIONS':
        return '', 200
    
    if db is None:
        return jsonify({'error': 'Database connection error'}), 500
        
    try:
        user_id, error, status = get_user_from_token()
        if error:
            return jsonify({'error': error}), status
        
        data = request.json
        
        # Build update document
        update_doc = {
            'updated_at': datetime.utcnow()
        }
        
        if 'phone' in data:
            update_doc['phone'] = data['phone']
        if 'location' in data:
            update_doc['location'] = data['location']
        if 'profile' in data:
            update_doc['profile'] = data['profile']
        
        # Update user
        result = db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_doc}
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'User not found'}), 404
        
        # Get updated user
        user = db.users.find_one({'_id': ObjectId(user_id)})
        
        print(f"✅ Profile updated for: {user['email']}")
        
        return jsonify({
            'message': 'Profile updated successfully',
            'profile': {
                'name': user['name'],
                'email': user['email'],
                'phone': user.get('phone'),
                'location': user.get('location'),
                'profile': user.get('profile', {})
            }
        }), 200
        
    except Exception as e:
        print(f"❌ Update profile error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ==================== DEBUG ROUTES ====================

@app.route('/api/debug/users', methods=['GET'])
def debug_users():
    """Debug: List all users (REMOVE IN PRODUCTION!)"""
    if db is None:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        users = list(db.users.find({}, {'password': 0}))
        
        users_list = []
        for user in users:
            users_list.append({
                'id': str(user['_id']),
                'email': user['email'],
                'name': user['name'],
                'role': user.get('role', 'student'),
                'created_at': user.get('created_at').isoformat() if user.get('created_at') else None
            })
        
        return jsonify({
            'total': len(users_list),
            'users': users_list
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/debug/test-password', methods=['POST'])
def test_password():
    """Debug: Test password verification (REMOVE IN PRODUCTION!)"""
    if db is None:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        data = request.json
        email = data.get('email', '').lower().strip()
        password = data.get('password', '')
        
        user = db.users.find_one({'email': email})
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        match = verify_password(password, user['password'])
        
        return jsonify({
            'email': email,
            'password_match': match,
            'hash_type': str(type(user['password']))
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== BASIC ROUTES ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    db_status = 'connected' if db is not None else 'disconnected'
    user_count = db.users.count_documents({}) if db else 0
    
    return jsonify({
        'status': 'healthy',
        'message': 'AI Career Counselling API is running',
        'timestamp': datetime.utcnow().isoformat(),
        'database': db_status,
        'users_count': user_count
    }), 200


@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'AI Career Counselling Backend API',
        'version': '4.0 MongoDB',
        'status': 'running',
        'database': 'MongoDB',
        'endpoints': {
            'health': '/api/health',
            'register': 'POST /api/auth/register',
            'login': 'POST /api/auth/login',
            'profile': 'GET /api/user/profile',
            'debug_users': 'GET /api/debug/users'
        }
    }), 200


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    print("\n" + "=" * 60)
    print("🚀 AI CAREER COUNSELLING BACKEND - MongoDB Version")
    print("=" * 60)
    print(f"✅ Mode: {os.getenv('FLASK_ENV', 'development')}")
    print(f"✅ Port: {port}")
    print(f"✅ Database: MongoDB")
    if db:
        print(f"✅ DB Name: {db.name}")
        print(f"✅ Users: {db.users.count_documents({})}")
    print(f"\n🌐 Health: http://localhost:{port}/api/health")
    print(f"🐛 Debug Users: http://localhost:{port}/api/debug/users")
    print("=" * 60 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)