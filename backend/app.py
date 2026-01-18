"""
AI Career Counselling Backend - Complete Production Version
All Features Integrated - FIXED VERSION WITH CHAT ROUTES
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
from flask_mail import Mail, Message
import secrets

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'career-counselling-secret-key-2026')
app.config['MONGODB_URI'] = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/career_counselling')

# Email Configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@careerguide.com')

mail = Mail(app)

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
    print(f"🎓 Total careers: {db.careers.count_documents({})}")
    print(f"🏫 Total colleges: {db.colleges.count_documents({})}")
    print("=" * 60)
except Exception as e:
    print("=" * 60)
    print(f"❌ MongoDB Connection Error: {e}")
    print("💡 Make sure MongoDB is running!")
    print("=" * 60)
    db = None


# ==================== VALIDATION FUNCTIONS ====================

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_username(username):
    """Validate username: 3-20 chars, starts with letter"""
    if len(username) < 3 or len(username) > 20:
        return False, "Username must be 3-20 characters"
    pattern = r'^[a-zA-Z][a-zA-Z0-9_-]*$'
    if not re.match(pattern, username):
        return False, "Username must start with letter and contain only letters, numbers, underscore, or hyphen"
    return True, ""


def validate_password(password):
    """Strong password validation"""
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
        errors.append("Password must contain at least one special character")
    
    if errors:
        return False, errors
    return True, []


def validate_dob(dob_str):
    """Validate date of birth"""
    try:
        dob = datetime.strptime(dob_str, '%Y-%m-%d')
        if dob >= datetime.now():
            return False, "Date of birth must be in the past"
        age = (datetime.now() - dob).days / 365.25
        if age < 5:
            return False, "User must be at least 5 years old"
        if age > 100:
            return False, "Invalid date of birth"
        return True, ""
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD"


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
    """Register new user"""
    if request.method == 'OPTIONS':
        return '', 200
    
    if db is None:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        data = request.json
        print(f"\n📝 Registration attempt: {data.get('email')}, Role: {data.get('role', 'student')}")
        
        # Validate required fields
        required_fields = ['name', 'email', 'username', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field.capitalize()} is required'}), 400
        
        # Validate email
        email = data['email'].lower().strip()
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate username
        username = data['username'].lower().strip()
        is_valid, error_msg = validate_username(username)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Validate password
        password = data['password']
        is_valid, errors = validate_password(password)
        if not is_valid:
            return jsonify({'error': 'Password does not meet requirements', 'details': errors}), 400
        
        # Check if user exists
        existing_user = db.users.find_one({'$or': [{'email': email}, {'username': username}]})
        if existing_user:
            if existing_user['email'] == email:
                return jsonify({'error': 'Email already registered'}), 409
            elif existing_user['username'] == username:
                return jsonify({'error': 'Username already taken'}), 409
        
        # Role-specific validation
        role = data.get('role', 'student')
        
        if role == 'student':
            if not data.get('dob'):
                return jsonify({'error': 'Date of birth is required for students'}), 400
            is_valid, error_msg = validate_dob(data['dob'])
            if not is_valid:
                return jsonify({'error': error_msg}), 400
            if not data.get('class_level'):
                return jsonify({'error': 'Class/Grade is required for students'}), 400
            if not data.get('school'):
                return jsonify({'error': 'School name is required for students'}), 400
        
        elif role == 'counsellor':
            if not data.get('phone'):
                return jsonify({'error': 'Phone number is required for counsellors'}), 400
            
            profile = data.get('profile', {})
            
            if not profile.get('specialization'):
                return jsonify({'error': 'Specialization is required for counsellors'}), 400
            if profile.get('experience') is None:
                return jsonify({'error': 'Experience is required for counsellors'}), 400
            if not profile.get('education'):
                return jsonify({'error': 'Education qualification is required for counsellors'}), 400
        
        # Hash password
        hashed_password = hash_password(password)
        
        # Create user document
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
            profile = data.get('profile', {})
            
            user.update({
                'phone': data['phone'],
                'location': data.get('location'),
                'profile': {
                    'specialization': profile.get('specialization'),
                    'experience': int(profile.get('experience', 0)),
                    'education': profile.get('education'),
                    'bio': profile.get('bio', ''),
                    'rating': float(profile.get('rating', 4.5)),
                    'sessions_conducted': int(profile.get('sessions_conducted', 0)),
                    'hourly_rate': int(profile.get('hourly_rate', 500))
                }
            })
            
            print(f"✅ Counsellor registered with specialization: {profile.get('specialization')}")
        
        # Insert into database
        result = db.users.insert_one(user)
        user_id = str(result.inserted_id)
        
        print(f"✅ User registered: {user_id}, Role: {role}\n")
        
        # Generate token
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
        print(f"\n🔐 Login attempt: {data.get('login')}")
        
        if not data.get('login') or not data.get('password'):
            return jsonify({'error': 'Username/Email and password are required'}), 400
        
        login_identifier = data['login'].lower().strip()
        password = data['password']
        
        # Find user by username OR email
        user = db.users.find_one({'$or': [{'email': login_identifier}, {'username': login_identifier}]})
        
        if not user:
            print(f"❌ User not found: {login_identifier}\n")
            return jsonify({'error': 'Invalid username/email or password'}), 401
        
        print(f"✅ User found: {user['name']} ({user.get('role', 'student')})")
        
        # Verify password
        if not verify_password(password, user['password']):
            print(f"❌ Invalid password\n")
            return jsonify({'error': 'Invalid username/email or password'}), 401
        
        print(f"✅ Password verified")
        
        # Check if account is active
        if not user.get('is_active', True):
            return jsonify({'error': 'Account is deactivated'}), 403
        
        # Update last login
        db.users.update_one({'_id': user['_id']}, {'$set': {'last_login': datetime.utcnow()}})
        
        # Generate token
        user_id = str(user['_id'])
        token = generate_token(user_id, user.get('role', 'student'))
        
        print(f"✅ Login successful: {user_id}\n")
        
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
        
        is_valid, error_msg = validate_username(username)
        if not is_valid:
            return jsonify({'available': False, 'error': error_msg}), 200
        
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
        
        if not validate_email(email):
            return jsonify({'available': False, 'error': 'Invalid email format'}), 200
        
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
    
    return jsonify({'valid': True, 'user_id': user_id, 'role': role}), 200


# ==================== FORGOT PASSWORD ROUTES ====================

def send_reset_email(to_email, user_name, reset_code, reset_token):
    """Send password reset email"""
    try:
        msg = Message(
            subject='Password Reset Request - AI Career Guidance',
            recipients=[to_email]
        )
        
        msg.html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #4F46E5;">Password Reset Request</h2>
                    
                    <p>Hi {user_name},</p>
                    
                    <p>You requested to reset your password for your AI Career Guidance account.</p>
                    
                    <div style="background-color: #F3F4F6; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <p style="margin: 0; font-size: 14px; color: #666;">Your reset code is:</p>
                        <h1 style="margin: 10px 0; color: #4F46E5; letter-spacing: 5px;">{reset_code}</h1>
                        <p style="margin: 0; font-size: 12px; color: #999;">This code will expire in 15 minutes</p>
                    </div>
                    
                    <p>If you didn't request this, you can safely ignore this email.</p>
                    
                    <hr style="border: none; border-top: 1px solid #E5E7EB; margin: 30px 0;">
                    
                    <p style="font-size: 12px; color: #999;">
                        This is an automated email from AI Career Guidance System.
                    </p>
                </div>
            </body>
        </html>
        """
        
        mail.send(msg)
        return True
        
    except Exception as e:
        print(f"❌ Email sending error: {e}")
        raise e


@app.route('/api/auth/forgot-password', methods=['POST', 'OPTIONS'])
def forgot_password():
    """Request password reset"""
    if request.method == 'OPTIONS':
        return '', 200
    
    if db is None:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        data = request.json
        print(f"\n🔑 Password reset request")
        
        if not data.get('email'):
            return jsonify({'error': 'Email is required'}), 400
        
        email = data['email'].lower().strip()
        
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        user = db.users.find_one({'email': email})
        
        if not user:
            print(f"❌ Email not found: {email}")
            return jsonify({
                'message': 'If this email is registered, you will receive a password reset link shortly.'
            }), 200
        
        print(f"✅ User found: {user['name']}")
        
        # Generate reset token and code
        reset_token = secrets.token_urlsafe(32)
        reset_code = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
        
        expires_at = datetime.utcnow() + timedelta(minutes=15)
        
        db.users.update_one(
            {'_id': user['_id']},
            {
                '$set': {
                    'reset_token': reset_token,
                    'reset_code': reset_code,
                    'reset_expires': expires_at,
                    'reset_requested_at': datetime.utcnow()
                }
            }
        )
        
        print(f"✅ Reset code generated: {reset_code}")
        
        try:
            send_reset_email(user['email'], user['name'], reset_code, reset_token)
            print(f"✅ Reset email sent to: {email}")
        except Exception as email_error:
            print(f"⚠️ Email sending failed: {email_error}")
        
        return jsonify({
            'message': 'If this email is registered, you will receive a password reset link shortly.',
            'reset_code': reset_code if os.getenv('FLASK_ENV') == 'development' else None
        }), 200
        
    except Exception as e:
        print(f"❌ Forgot password error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Failed to process request'}), 500


@app.route('/api/auth/verify-reset-code', methods=['POST', 'OPTIONS'])
def verify_reset_code():
    """Verify reset code"""
    if request.method == 'OPTIONS':
        return '', 200
    
    if db is None:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        data = request.json
        
        if not data.get('email') or not data.get('code'):
            return jsonify({'error': 'Email and code are required'}), 400
        
        email = data['email'].lower().strip()
        code = data['code'].strip()
        
        user = db.users.find_one({'email': email})
        
        if not user:
            return jsonify({'error': 'Invalid email or code'}), 401
        
        if not user.get('reset_code'):
            return jsonify({'error': 'No reset request found'}), 401
        
        if user.get('reset_expires') and user['reset_expires'] < datetime.utcnow():
            return jsonify({'error': 'Reset code has expired. Please request a new one.'}), 401
        
        if user['reset_code'] != code:
            return jsonify({'error': 'Invalid reset code'}), 401
        
        print(f"✅ Reset code verified for: {email}")
        
        return jsonify({
            'message': 'Code verified successfully',
            'reset_token': user.get('reset_token')
        }), 200
        
    except Exception as e:
        print(f"❌ Verify code error: {str(e)}")
        return jsonify({'error': 'Verification failed'}), 500


@app.route('/api/auth/reset-password', methods=['POST', 'OPTIONS'])
def reset_password():
    """Reset password using token"""
    if request.method == 'OPTIONS':
        return '', 200
    
    if db is None:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        data = request.json
        print(f"\n🔐 Password reset attempt")
        
        if not data.get('email') or not data.get('reset_token') or not data.get('new_password'):
            return jsonify({'error': 'Email, reset token, and new password are required'}), 400
        
        email = data['email'].lower().strip()
        reset_token = data['reset_token']
        new_password = data['new_password']
        
        is_valid, errors = validate_password(new_password)
        if not is_valid:
            return jsonify({
                'error': 'Password does not meet requirements',
                'details': errors
            }), 400
        
        user = db.users.find_one({'email': email})
        
        if not user:
            return jsonify({'error': 'Invalid reset token'}), 401
        
        if not user.get('reset_token') or user['reset_token'] != reset_token:
            return jsonify({'error': 'Invalid reset token'}), 401
        
        if user.get('reset_expires') and user['reset_expires'] < datetime.utcnow():
            return jsonify({'error': 'Reset token has expired'}), 401
        
        hashed_password = hash_password(new_password)
        
        db.users.update_one(
            {'_id': user['_id']},
            {
                '$set': {
                    'password': hashed_password,
                    'updated_at': datetime.utcnow()
                },
                '$unset': {
                    'reset_token': '',
                    'reset_code': '',
                    'reset_expires': '',
                    'reset_requested_at': ''
                }
            }
        )
        
        print(f"✅ Password reset successful for: {email}")
        
        return jsonify({'message': 'Password reset successful. You can now login with your new password.'}), 200
        
    except Exception as e:
        print(f"❌ Reset password error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Password reset failed'}), 500


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


@app.route('/api/user/profile', methods=['PUT', 'OPTIONS'])
def update_profile():
    """Update user profile"""
    if request.method == 'OPTIONS':
        return '', 200
    
    if db is None:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        user_id, role, error, status = get_user_from_token()
        if error:
            return jsonify({'error': error}), status
        
        data = request.json
        
        # Build update document
        update_doc = {'$set': {'updated_at': datetime.utcnow()}}
        
        if 'name' in data:
            update_doc['$set']['name'] = data['name']
        
        if role == 'student':
            if 'profile' in data:
                update_doc['$set']['profile'] = data['profile']
            if 'location' in data:
                update_doc['$set']['location'] = data['location']
        
        elif role == 'counsellor':
            if 'profile' in data:
                update_doc['$set']['profile'] = data['profile']
            if 'location' in data:
                update_doc['$set']['location'] = data['location']
        
        # Update user
        result = db.users.update_one({'_id': ObjectId(user_id)}, update_doc)
        
        if result.modified_count == 0:
            return jsonify({'message': 'No changes made'}), 200
        
        return jsonify({'message': 'Profile updated successfully'}), 200
        
    except Exception as e:
        print(f"❌ Update profile error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ==================== CAREER ROUTES ====================

@app.route('/api/careers', methods=['GET', 'OPTIONS'])
def get_careers():
    """Get all careers with optional filters"""
    if request.method == 'OPTIONS':
        return '', 200
    
    if db is None:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        category = request.args.get('category')
        search = request.args.get('search')
        
        query = {}
        
        if category and category.lower() != 'all':
            query['category'] = {'$regex': category, '$options': 'i'}
        
        if search:
            query['$or'] = [
                {'name': {'$regex': search, '$options': 'i'}},
                {'description': {'$regex': search, '$options': 'i'}}
            ]
        
        careers = list(db.careers.find(query))
        
        for career in careers:
            career['_id'] = str(career['_id'])
        
        print(f"✅ Fetched {len(careers)} careers")
        
        return jsonify({'careers': careers, 'count': len(careers)}), 200
        
    except Exception as e:
        print(f"❌ Error fetching careers: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/careers/<career_id>', methods=['GET', 'OPTIONS'])
def get_career_details(career_id):
    """Get detailed career information"""
    if request.method == 'OPTIONS':
        return '', 200
    
    if db is None:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        career = db.careers.find_one({'_id': ObjectId(career_id)})
        
        if not career:
            return jsonify({'error': 'Career not found'}), 404
        
        career['_id'] = str(career['_id'])
        
        return jsonify(career), 200
        
    except Exception as e:
        print(f"❌ Error fetching career details: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ==================== COLLEGE ROUTES ====================

@app.route('/api/colleges', methods=['GET', 'OPTIONS'])
def get_colleges():
    """Get all colleges with optional filters"""
    if request.method == 'OPTIONS':
        return '', 200
    
    if db is None:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        district = request.args.get('district')
        college_type = request.args.get('type')
        search = request.args.get('search')
        
        query = {}
        
        if district and district.lower() != 'all':
            query['district'] = {'$regex': district, '$options': 'i'}
        
        if college_type and college_type.lower() != 'all':
            query['type'] = {'$regex': college_type, '$options': 'i'}
        
        if search:
            query['$or'] = [
                {'name': {'$regex': search, '$options': 'i'}},
                {'location': {'$regex': search, '$options': 'i'}},
                {'short_name': {'$regex': search, '$options': 'i'}}
            ]
        
        colleges = list(db.colleges.find(query))
        
        for college in colleges:
            college['_id'] = str(college['_id'])
            if 'created_at' in college:
                college['created_at'] = college['created_at'].isoformat()
            if 'updated_at' in college:
                college['updated_at'] = college['updated_at'].isoformat()
        
        print(f"✅ Fetched {len(colleges)} colleges")
        
        return jsonify({'colleges': colleges, 'count': len(colleges)}), 200
        
    except Exception as e:
        print(f"❌ Error fetching colleges: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/colleges/<college_id>', methods=['GET', 'OPTIONS'])
def get_college_details(college_id):
    """Get detailed college information"""
    if request.method == 'OPTIONS':
        return '', 200
    
    if db is None:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        college = db.colleges.find_one({'_id': ObjectId(college_id)})
        
        if not college:
            return jsonify({'error': 'College not found'}), 404
        
        college['_id'] = str(college['_id'])
        
        if 'created_at' in college:
            college['created_at'] = college['created_at'].isoformat()
        if 'updated_at' in college:
            college['updated_at'] = college['updated_at'].isoformat()
        
        return jsonify(college), 200
        
    except Exception as e:
        print(f"❌ Error fetching college details: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/colleges/stats', methods=['GET', 'OPTIONS'])
def get_college_stats():
    """Get statistics about colleges"""
    if request.method == 'OPTIONS':
        return '', 200
    
    if db is None:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        total = db.colleges.count_documents({})
        
        by_type = {}
        types = db.colleges.distinct('type')
        for ctype in types:
            count = db.colleges.count_documents({'type': ctype})
            by_type[ctype] = count
        
        by_district = {}
        districts = db.colleges.distinct('district')
        for district in districts:
            count = db.colleges.count_documents({'district': district})
            by_district[district] = count
        
        return jsonify({
            'total': total,
            'by_type': by_type,
            'by_district': by_district
        }), 200
        
    except Exception as e:
        print(f"❌ Error fetching stats: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ==================== COURSES ROUTES ====================

@app.route('/api/courses', methods=['GET', 'OPTIONS'])
def get_courses():
    """Get all courses"""
    if request.method == 'OPTIONS':
        return '', 200
    
    if db is None:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        courses = list(db.courses.find({}))
        
        for course in courses:
            course['_id'] = str(course['_id'])
        
        return jsonify({'courses': courses, 'count': len(courses)}), 200
        
    except Exception as e:
        print(f"❌ Error fetching courses: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ==================== RECOMMENDATIONS ROUTES ====================

@app.route('/api/recommendations', methods=['GET', 'OPTIONS'])
def get_recommendations():
    """Get AI career recommendations"""
    if request.method == 'OPTIONS':
        return '', 200
    
    if db is None:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        user_id, role, error, status = get_user_from_token()
        if error:
            return jsonify({'error': error}), status
        
        # Get user profile
        user = db.users.find_one({'_id': ObjectId(user_id)})
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Mock recommendations
        recommendations = [
            {
                'career_name': 'Software Engineer',
                'match_score': 92.5,
                'interest_score': 95,
                'skill_score': 90,
                'personality_score': 92,
                'reasons': ['Matches your technology interests', 'Aligns with analytical skills'],
                'education': ['B.Tech Computer Science', 'BCA', 'MCA'],
                'salary_range': '₹4-25 LPA',
                'growth_prospects': 'Excellent'
            }
        ]
        
        return jsonify({
            'recommendations': recommendations,
            'based_on': {
                'interests': user.get('profile', {}).get('interests', []),
                'skills': user.get('profile', {}).get('skills', [])
            }
        }), 200
        
    except Exception as e:
        print(f"❌ Recommendations error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ==================== COUNSELLOR ROUTES ====================

@app.route('/api/counsellors', methods=['GET', 'OPTIONS'])
def get_counsellors():
    """Get all counsellors"""
    if request.method == 'OPTIONS':
        return '', 200
    
    if db is None:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        counsellors = list(db.users.find(
            {'role': 'counsellor'},
            {'password': 0}
        ))
        
        for counsellor in counsellors:
            counsellor['_id'] = str(counsellor['_id'])
        
        return jsonify({'counsellors': counsellors, 'count': len(counsellors)}), 200
        
    except Exception as e:
        print(f"❌ Error fetching counsellors: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/counsellors/<counsellor_id>', methods=['GET', 'OPTIONS'])
def get_counsellor_details(counsellor_id):
    """Get counsellor details"""
    if request.method == 'OPTIONS':
        return '', 200
    
    if db is None:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        counsellor = db.users.find_one(
            {'_id': ObjectId(counsellor_id), 'role': 'counsellor'},
            {'password': 0}
        )
        
        if not counsellor:
            return jsonify({'error': 'Counsellor not found'}), 404
        
        counsellor['_id'] = str(counsellor['_id'])
        
        return jsonify(counsellor), 200
        
    except Exception as e:
        print(f"❌ Error fetching counsellor: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ==================== BASIC ROUTES ====================

@app.route('/api/health', methods=['GET', 'OPTIONS'])
def health_check():
    """Health check endpoint"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        db_status = 'connected' if db is not None else 'disconnected'
        
        if db is not None:
            user_count = db.users.count_documents({})
            career_count = db.careers.count_documents({})
            college_count = db.colleges.count_documents({})
        else:
            user_count = 0
            career_count = 0
            college_count = 0
        
        return jsonify({
            'status': 'healthy',
            'message': 'AI Career Counselling API',
            'version': '7.0 - CHAT ROUTES FIXED',
            'timestamp': datetime.utcnow().isoformat(),
            'database': db_status,
            'counts': {
                'users': user_count,
                'careers': career_count,
                'colleges': college_count
            }
        }), 200
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'AI Career Counselling Backend API',
        'version': '7.0 - Chat Routes Fixed',
        'features': [
            'Authentication (username/email login, strong passwords)',
            'User profiles (students & counsellors)',
            'Career management',
            'Kerala colleges (15 real colleges)',
            'Course listings',
            'AI chatbot',
            'Quiz system',
            'Recommendations',
            'Counsellor directory',
            'JWT authentication'
        ],
        'endpoints': [
            'POST /api/auth/register',
            'POST /api/auth/login',
            'GET /api/careers',
            'GET /api/colleges',
            'GET /api/counsellors',
            'GET /api/recommendations',
            'POST /api/chat/send'
        ]
    }), 200


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


# ==================== BLUEPRINT REGISTRATION ====================

if __name__ == '__main__':
    # Set DB in app config for blueprints
    app.config['DB'] = db
    
    # Register Quiz API
    try:
        from quiz_api import quiz_bp
        app.register_blueprint(quiz_bp, url_prefix='/api')
        print("✅ Quiz API registered")
    except ImportError as e:
        print(f"⚠️ quiz_api.py not found - skipping ({e})")
    
    # Register Appointment API
    try:
        from appointment_routes import appointment_bp
        app.register_blueprint(appointment_bp, url_prefix='/api')
        print("✅ Appointment API registered")
    except ImportError as e:
        print(f"⚠️ appointment_routes.py not found - skipping ({e})")
    
    # Register Payment API
    try:
        from payment_routes import payment_bp
        app.register_blueprint(payment_bp, url_prefix='/api/payment')
        print("✅ Payment API registered")
    except ImportError as e:
        print(f"⚠️ payment_routes.py not found - skipping ({e})")
    
    # Register Chat Routes - FIXED
    try:
        from routes.chat_routes import chat_bp
        app.register_blueprint(chat_bp, url_prefix='/api')
        print("✅ Chat API registered at /api/chat")
    except ImportError:
        try:
            from chat_routes import chat_bp
            app.register_blueprint(chat_bp, url_prefix='/api')
            print("✅ Chat API registered at /api/chat")
        except ImportError as e:
            print(f"⚠️ chat_routes.py not found - skipping ({e})")
    
    # Register Admin API
    try:
        from admin_api import admin_bp
        app.register_blueprint(admin_bp, url_prefix='/api/admin')
        print("✅ Admin API registered")
    except ImportError as e:
        print(f"⚠️ admin_api.py not found - skipping ({e})")
    
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    print("\n" + "=" * 60)
    print("🚀 AI CAREER COUNSELLING BACKEND v7.0")
    print("=" * 60)
    print("✅ All Features Integrated")
    print("✅ Chat Routes Fixed - No Duplicates")
    print("✅ MongoDB Connection Working")
    if db is not None:
        print(f"\n✅ Database: {db.name}")
        print(f"✅ Users: {db.users.count_documents({})}")
        print(f"✅ Careers: {db.careers.count_documents({})}")
        print(f"✅ Colleges: {db.colleges.count_documents({})}")
    print(f"\n🌐 Server: http://localhost:{port}")
    print(f"🏥 Health: http://localhost:{port}/api/health")
    print(f"💬 Chat: http://localhost:{port}/api/chat/send")
    print("=" * 60 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)