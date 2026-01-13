from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'test-secret-key'
users = {}  # Store users in memory (no database needed!)

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'database': 'in-memory'})

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    email = data['email'].lower()
    
    if email in users:
        return jsonify({'error': 'Email already registered'}), 409
    
    hashed = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
    users[email] = {
        'name': data['name'],
        'password': hashed,
        'email': email,
        'role': 'student'
    }
    
    token = jwt.encode({
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=7)
    }, app.config['SECRET_KEY'])
    
    return jsonify({
        'message': 'User registered successfully',
        'token': token,
        'user': {
            'id': email,
            'name': data['name'],
            'email': email,
            'role': 'student'
        }
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data['email'].lower()
    
    if email not in users:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if not bcrypt.checkpw(data['password'].encode(), users[email]['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=7)
    }, app.config['SECRET_KEY'])
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'id': email,
            'name': users[email]['name'],
            'email': email,
            'role': 'student'
        }
    }), 200

@app.route('/api/user/profile', methods=['GET'])
def get_profile():
    # Simple profile endpoint for testing
    return jsonify({
        'name': 'Test User',
        'email': 'test@example.com',
        'role': 'student'
    })

if __name__ == '__main__':
    print("🚀 Simple backend starting...")
    print("✅ No database needed - using in-memory storage")
    print("🌐 Open: http://localhost:5000/api/health")
    app.run(host='0.0.0.0', port=5000, debug=True)