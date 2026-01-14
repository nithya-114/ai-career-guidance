"""
Create Admin User Script
Run this once to create an admin account in MongoDB
"""

from pymongo import MongoClient
import bcrypt
from datetime import datetime

# MongoDB connection
MONGODB_URI = 'mongodb://localhost:27017/career_counselling'

def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def create_admin():
    """Create admin user"""
    try:
        # Connect to MongoDB
        client = MongoClient(MONGODB_URI)
        db = client.get_database()
        
        print("=" * 60)
        print("🔐 ADMIN USER CREATION")
        print("=" * 60)
        
        # Check if admin already exists
        existing_admin = db.users.find_one({'role': 'admin'})
        
        if existing_admin:
            print("⚠️  Admin user already exists!")
            print(f"   Username: {existing_admin.get('username')}")
            print(f"   Email: {existing_admin.get('email')}")
            print("\n❓ Do you want to create another admin? (y/n): ", end='')
            choice = input().lower()
            if choice != 'y':
                print("❌ Admin creation cancelled.")
                return
        
        # Get admin details
        print("\n📝 Enter admin details:")
        print("-" * 60)
        
        name = input("Full Name: ").strip()
        username = input("Username (for login): ").strip().lower()
        email = input("Email: ").strip().lower()
        password = input("Password: ").strip()
        
        # Validate inputs
        if not all([name, username, email, password]):
            print("❌ Error: All fields are required!")
            return
        
        if len(password) < 8:
            print("❌ Error: Password must be at least 8 characters!")
            return
        
        # Check if username/email already exists
        if db.users.find_one({'username': username}):
            print(f"❌ Error: Username '{username}' already exists!")
            return
        
        if db.users.find_one({'email': email}):
            print(f"❌ Error: Email '{email}' already registered!")
            return
        
        # Hash password
        hashed_password = hash_password(password)
        
        # Create admin user document
        admin_user = {
            'name': name,
            'username': username,
            'email': email,
            'password': hashed_password,
            'role': 'admin',
            'is_active': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'profile': {
                'permissions': ['all'],
                'department': 'Administration',
                'access_level': 'full'
            }
        }
        
        # Insert admin user
        result = db.users.insert_one(admin_user)
        admin_id = result.inserted_id
        
        print("\n" + "=" * 60)
        print("✅ ADMIN USER CREATED SUCCESSFULLY!")
        print("=" * 60)
        print(f"Admin ID: {admin_id}")
        print(f"Name: {name}")
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Role: admin")
        print("\n🔐 Login Credentials:")
        print(f"   Username: {username}")
        print(f"   Password: [hidden for security]")
        print("\n🌐 Admin Login URL:")
        print("   http://localhost:3000/admin-login")
        print("=" * 60)
        
        # Count total admins
        total_admins = db.users.count_documents({'role': 'admin'})
        print(f"\n📊 Total admins in database: {total_admins}")
        
    except Exception as e:
        print(f"\n❌ Error creating admin: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()

if __name__ == '__main__':
    create_admin()