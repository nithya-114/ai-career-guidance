"""
AI Career Counselling Backend - Complete Production Version
Features:
- Unique username + email login
- DOB, class, school for students
- Strong password validation (8+ chars, uppercase, lowercase, number, special char)
- Separate registration for students and counsellors
- Proper MongoDB integration
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
from pymongo import MongoClient, ASCENDING
from bson import ObjectId
import bcrypt
import jwt
import os
import re
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
    client = MongoClient(app.config['MONGODB_URI'], serverSelectionTimeoutMS=5000)
    db = client.get_database()
    
    # Create unique indexes
    db.users.create_index([("email", ASCENDING)], unique=True)
    db.users.create_index([("username", ASCENDING)], unique=True)
    
    # Test connection
    client.server_info()
    print("=" * 60)
    print("✅ Connected to MongoDB successfully!")
    print(f"📊 Database: {db.name}")
    print(f"👥 Total users: {db.users.count_documents({})}")
    print("=" * 60)
except Exception as e:
    print("=" * 60)
    print(f"❌ MongoDB Connection Error: {e}")
    print("💡 Make sure MongoDB is running!")
    print("   Windows: net start MongoDB")
    print("   Linux: sudo systemctl start mongod")
    print("=" * 60)
    db = None


# ==================== VALIDATION FUNCTIONS ====================

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_username(username):
    """
    Validate username:
    - 3-20 characters
    - Only letters, numbers, underscore, hyphen
    - Must start with letter
    """
    if len(username) < 3 or len(username) > 20:
        return False, "Username must be 3-20 characters"
    
    pattern = r'^[a-zA-Z][a-zA-Z0-9_-]*$'
    if not re.match(pattern, username):
        return False, "Username must start with letter and contain only letters, numbers, underscore, or hyphen"
    
    return True, ""


def validate_password(password):
    """
    Strong password validation:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)
    """
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not re.search(r'\d', password):
        errors.append("Password must contain at least one number")
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
        errors.append("Password must contain at least one special character (!@#$%^&* etc.)")
    
    if errors:
        return False, errors
    
    return True, []


def validate_dob(dob_str):
    """Validate date of birth (YYYY-MM-DD format)"""
    try:
        dob = datetime.strptime(dob_str, '%Y-%m-%d')
        
        # Check if date is in the past
        if dob >= datetime.now():
            return False, "Date of birth must be in the past"
        
        # Check if person is at least 5 years old
        age = (datetime.now() - dob).days / 365.25
        if age < 5:
            return False, "User must be at least 5 years old"
        
        # Check if person is less than 100 years old
        if age > 100:
            return False, "Invalid date of birth"
        
        return True, ""
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD (e.g., 2005-06-15)"


# ==================== HELPER FUNCTIONS ====================

def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def verify_password(password, hashed):
    """Verify password against hash"""
    try:
        if isinstance(password, bytes):
            password = password.decode('utf-8')
        if isinstance(hashed, str):
            hashed = hashed.encode('utf-8')
        
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
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
        return None, None, 'No token provided', 401
    
    token = auth_header.split(' ')[1]
    
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id'], payload.get('role'), None, None
    except jwt.ExpiredSignatureError:
        return None, None, 'Token expired', 401
    except jwt.InvalidTokenError:
        return None, None, 'Invalid token', 401


# ==================== AUTHENTICATION ROUTES ====================

@app.route('/api/auth/register', methods=['POST', 'OPTIONS'])
def register():
    """Register new user (student or counsellor)"""
    if request.method == 'OPTIONS':
        return '', 200
    
    if db is None:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        data = request.json
        print(f"\n📝 Registration attempt")
        print(f"   Email: {data.get('email')}")
        print(f"   Username: {data.get('username')}")
        print(f"   Role: {data.get('role', 'student')}")
        
        # ========== VALIDATE REQUIRED FIELDS ==========
        required_fields = ['name', 'email', 'username', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field.capitalize()} is required'}), 400
        
        # ========== VALIDATE EMAIL ==========
        email = data['email'].lower().strip()
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # ========== VALIDATE USERNAME ==========
        username = data['username'].lower().strip()
        is_valid, error_msg = validate_username(username)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # ========== VALIDATE PASSWORD ==========
        password = data['password']
        is_valid, errors = validate_password(password)
        if not is_valid:
            return jsonify({
                'error': 'Password does not meet requirements',
                'details': errors
            }), 400
        
        # ========== CHECK IF USER EXISTS ==========
        existing_user = db.users.find_one({
            '$or': [
                {'email': email},
                {'username': username}
            ]
        })
        
        if existing_user:
            if existing_user['email'] == email:
                print(f"❌ Email already registered: {email}")
                return jsonify({'error': 'Email already registered'}), 409
            elif existing_user['username'] == username:
                print(f"❌ Username already taken: {username}")
                return jsonify({'error': 'Username already taken'}), 409
        
        # ========== ROLE-SPECIFIC VALIDATION ==========
        role = data.get('role', 'student')
        
        if role == 'student':
            # Validate student-specific fields
            if not data.get('dob'):
                return jsonify({'error': 'Date of birth is required for students'}), 400
            
            # Validate DOB
            is_valid, error_msg = validate_dob(data['dob'])
            if not is_valid:
                return jsonify({'error': error_msg}), 400
            
            if not data.get('class_level'):
                return jsonify({'error': 'Class/Grade is required for students'}), 400
            
            if not data.get('school'):
                return jsonify({'error': 'School name is required for students'}), 400
        
        elif role == 'counsellor':
            # Validate counsellor-specific fields
            if not data.get('phone'):
                return jsonify({'error': 'Phone number is required for counsellors'}), 400
            
            if not data.get('specialization'):
                return jsonify({'error': 'Specialization is required for counsellors'}), 400
            
            if not data.get('experience'):
                return jsonify({'error': 'Experience is required for counsellors'}), 400
            
            if not data.get('education'):
                return jsonify({'error': 'Education qualification is required for counsellors'}), 400
        
        # ========== HASH PASSWORD ==========
        hashed_password = hash_password(password)
        print(f"🔐 Password hashed successfully")
        
        # ========== CREATE USER DOCUMENT ==========
        user = {
            'name': data['name'].strip(),
            'email': email,
            'username': username,
            'password': hashed_password,
            'role': role,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'is_active': True,
            'email_verified': False
        }
        
        # Add role-specific fields
        if role == 'student':
            user.update({
                'dob': datetime.strptime(data['dob'], '%Y-%m-%d'),
                'class_level': data['class_level'],
                'school': data['school'],
                'location': data.get('location'),
                'profile': {
                    'interests': [],
                    'goals': None,
                    'subjects': [],
                    'skills': []
                }
            })
        elif role == 'counsellor':
            user.update({
                'phone': data['phone'],
                'location': data.get('location'),
                'profile': {
                    'specialization': data['specialization'],
                    'experience': data['experience'],
                    'education': data['education'],
                    'bio': data.get('bio', ''),
                    'rating': 0.0,
                    'sessions_conducted': 0,
                    'hourly_rate': data.get('hourly_rate', 500)
                }
            })
        
        # ========== INSERT INTO DATABASE ==========
        result = db.users.insert_one(user)
        user_id = str(result.inserted_id)
        
        print(f"✅ User registered successfully")
        print(f"   User ID: {user_id}")
        print(f"   Role: {role}")
        print(f"📊 Total users: {db.users.count_documents({})}\n")
        
        # ========== GENERATE TOKEN ==========
        token = generate_token(user_id, role)
        
        return jsonify({
            'message': 'Registration successful',
            'token': token,
            'user': {
                'id': user_id,
                'name': user['name'],
                'email': user['email'],
                'username': user['username'],
                'role': role
            }
        }), 201
        
    except Exception as e:
        print(f"❌ Registration error: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500


@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def login():
    """Login with username/email and password"""
    if request.method == 'OPTIONS':
        return '', 200
    
    if db is None:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        data = request.json
        print(f"\n🔐 Login attempt")
        print(f"   Identifier: {data.get('login')}")
        
        # ========== VALIDATE INPUT ==========
        if not data.get('login') or not data.get('password'):
            return jsonify({'error': 'Username/Email and password are required'}), 400
        
        login_identifier = data['login'].lower().strip()
        password = data['password']
        
        print(f"   Looking up user...")
        
        # ========== FIND USER (by username OR email) ==========
        user = db.users.find_one({
            '$or': [
                {'email': login_identifier},
                {'username': login_identifier}
            ]
        })
        
        if not user:
            print(f"❌ User not found: {login_identifier}\n")
            return jsonify({'error': 'Invalid username/email or password'}), 401
        
        print(f"✅ User found: {user['name']}")
        print(f"   Email: {user['email']}")
        print(f"   Username: {user['username']}")
        print(f"   Role: {user.get('role', 'student')}")
        
        # ========== VERIFY PASSWORD ==========
        if not verify_password(password, user['password']):
            print(f"❌ Invalid password\n")
            return jsonify({'error': 'Invalid username/email or password'}), 401
        
        print(f"✅ Password verified")
        
        # ========== CHECK IF ACCOUNT IS ACTIVE ==========
        if not user.get('is_active', True):
            return jsonify({'error': 'Account is deactivated. Contact support.'}), 403
        
        # ========== UPDATE LAST LOGIN ==========
        db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'last_login': datetime.utcnow()}}
        )
        
        # ========== GENERATE TOKEN ==========
        user_id = str(user['_id'])
        token = generate_token(user_id, user.get('role', 'student'))
        
        print(f"✅ Login successful")
        print(f"   User ID: {user_id}\n")
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user_id,
                'name': user['name'],
                'email': user['email'],
                'username': user['username'],
                'role': user.get('role', 'student')
            }
        }), 200
        
    except Exception as e:
        print(f"❌ Login error: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Login failed: {str(e)}'}), 500


@app.route('/api/auth/check-username', methods=['POST', 'OPTIONS'])
def check_username():
    """Check if username is available"""
    if request.method == 'OPTIONS':
        return '', 200
    
    if db is None:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        data = request.json
        username = data.get('username', '').lower().strip()
        
        if not username:
            return jsonify({'error': 'Username is required'}), 400
        
        # Validate format
        is_valid, error_msg = validate_username(username)
        if not is_valid:
            return jsonify({'available': False, 'error': error_msg}), 200
        
        # Check if exists
        existing = db.users.find_one({'username': username})
        
        if existing:
            return jsonify({'available': False, 'error': 'Username already taken'}), 200
        
        return jsonify({'available': True}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/check-email', methods=['POST', 'OPTIONS'])
def check_email():
    """Check if email is available"""
    if request.method == 'OPTIONS':
        return '', 200
    
    if db is None:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        data = request.json
        email = data.get('email', '').lower().strip()
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        # Validate format
        if not validate_email(email):
            return jsonify({'available': False, 'error': 'Invalid email format'}), 200
        
        # Check if exists
        existing = db.users.find_one({'email': email})
        
        if existing:
            return jsonify({'available': False, 'error': 'Email already registered'}), 200
        
        return jsonify({'available': True}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/verify-token', methods=['GET', 'OPTIONS'])
def verify_token():
    """Verify JWT token"""
    if request.method == 'OPTIONS':
        return '', 200
    
    user_id, role, error, status = get_user_from_token()
    
    if error:
        return jsonify({'error': error}), status
    
    return jsonify({
        'valid': True,
        'user_id': user_id,
        'role': role
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
        user_id, role, error, status = get_user_from_token()
        if error:
            return jsonify({'error': error}), status
        
        user = db.users.find_one({'_id': ObjectId(user_id)}, {'password': 0})
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Format response based on role
        response = {
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email'],
            'username': user['username'],
            'role': user.get('role', 'student'),
            'created_at': user.get('created_at').isoformat() if user.get('created_at') else None
        }
        
        if user.get('role') == 'student':
            response.update({
                'dob': user.get('dob').isoformat() if user.get('dob') else None,
                'class_level': user.get('class_level'),
                'school': user.get('school'),
                'location': user.get('location'),
                'profile': user.get('profile', {})
            })
        elif user.get('role') == 'counsellor':
            response.update({
                'phone': user.get('phone'),
                'location': user.get('location'),
                'profile': user.get('profile', {})
            })
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"❌ Get profile error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ==================== BASIC ROUTES ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    db_status = 'connected' if db is not None else 'disconnected'
    user_count = db.users.count_documents({}) if db else 0
    
    return jsonify({
        'status': 'healthy',
        'message': 'AI Career Counselling API',
        'version': '5.0',
        'timestamp': datetime.utcnow().isoformat(),
        'database': db_status,
        'users_count': user_count
    }), 200


@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'AI Career Counselling Backend API',
        'version': '5.0 - Production Ready',
        'features': [
            'Username + Email login',
            'Strong password validation',
            'Student: DOB, Class, School',
            'Counsellor: Specialization, Experience',
            'JWT Authentication'
        ]
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
    print("🚀 AI CAREER COUNSELLING BACKEND v5.0")
    print("=" * 60)
    print("✅ Features:")
    print("   • Username + Email login")
    print("   • Strong password validation (8+ chars)")
    print("   • Student: DOB, Class, School")
    print("   • Counsellor: Professional info")
    print("   • JWT Authentication")
    if db is not None:
        print(f"\n✅ Database: {db.name}")
        print(f"✅ Users: {db.users.count_documents({})}")
    print(f"\n🌐 Health: http://localhost:{port}/api/health")
    print("=" * 60 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)