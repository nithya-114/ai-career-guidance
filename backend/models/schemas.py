"""
Database Models/Schemas for AI Career Counselling Application

This file defines the structure of all collections in MongoDB.
Each class represents a collection schema with validation rules.
"""

from datetime import datetime
from typing import Dict, List, Optional
from bson import ObjectId

class UserModel:
    """
    User Model - For students, counsellors, and admins
    Collection: users
    """
    
    @staticmethod
    def schema():
        return {
            '_id': ObjectId,  # Auto-generated
            'name': str,  # Full name
            'email': str,  # Unique email
            'password': str,  # Hashed password (bcrypt)
            'role': str,  # 'student', 'counsellor', 'admin'
            'phone': Optional[str],
            'location': Optional[str],
            'profile': {
                'education': Optional[str],  # '10th', '12th', 'Undergraduate', etc.
                'interests': Optional[List[str]],  # List of interests
                'goals': Optional[str],  # Career goals text
                'subjects': Optional[List[str]],  # Favorite subjects
                'skills': Optional[List[str]],  # Identified skills
            },
            'created_at': datetime,
            'updated_at': datetime,
            'last_login': Optional[datetime],
            'is_active': bool,
            'email_verified': bool,
        }
    
    @staticmethod
    def create_user(name, email, password, role='student'):
        """Create a new user document"""
        return {
            'name': name,
            'email': email.lower(),
            'password': password,  # Should be hashed before calling this
            'role': role,
            'phone': None,
            'location': None,
            'profile': {
                'education': None,
                'interests': [],
                'goals': None,
                'subjects': [],
                'skills': [],
            },
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'last_login': None,
            'is_active': True,
            'email_verified': False,
        }


class CareerModel:
    """
    Career Model - Information about different careers
    Collection: careers
    """
    
    @staticmethod
    def schema():
        return {
            '_id': ObjectId,
            'name': str,  # Career name
            'category': str,  # Technology, Healthcare, Engineering, etc.
            'description': str,  # Detailed description
            'related_interests': List[str],  # List of relevant interests
            'required_skills': List[str],  # Skills needed
            'related_subjects': List[str],  # Academic subjects
            'personality_fit': Dict[str, int],  # Personality traits (1-10 scale)
            'work_environment': str,  # Office, Remote, Field, etc.
            'salary_range': str,  # Expected salary
            'growth_prospects': str,  # Career growth potential
            'education_required': str,  # Minimum education needed
            'created_at': datetime,
            'updated_at': datetime,
        }


class CourseModel:
    """
    Course Model - Academic courses for careers
    Collection: courses
    """
    
    @staticmethod
    def schema():
        return {
            '_id': ObjectId,
            'name': str,  # Course name
            'career': List[str],  # Related careers (can map to multiple)
            'duration': str,  # Course duration
            'eligibility': str,  # Entry requirements
            'entrance_exams': List[str],  # Required entrance exams
            'type': str,  # Engineering, Medical, Arts, Commerce, etc.
            'average_fees': str,  # Fee range
            'top_specializations': List[str],  # Specialization options
            'created_at': datetime,
            'updated_at': datetime,
        }


class CollegeModel:
    """
    College Model - Information about colleges/universities
    Collection: colleges
    """
    
    @staticmethod
    def schema():
        return {
            '_id': ObjectId,
            'name': str,  # College name
            'location': str,  # City
            'state': str,  # State
            'type': str,  # Government, Private
            'courses': List[str],  # Courses offered
            'ranking': int,  # National/State ranking
            'fees': str,  # Fee structure
            'placements': {
                'average': str,  # Average package
                'highest': str,  # Highest package
                'percentage': str,  # Placement percentage
            },
            'website': str,  # College website
            'facilities': List[str],  # Available facilities
            'created_at': datetime,
            'updated_at': datetime,
        }


class QuizResultModel:
    """
    Quiz Results Model - Store user quiz responses and results
    Collection: quiz_results
    """
    
    @staticmethod
    def schema():
        return {
            '_id': ObjectId,
            'user_id': str,  # Reference to user
            'quiz_type': str,  # 'aptitude', 'personality'
            'questions': List[Dict],  # List of questions with user answers
            'score': Optional[int],  # Score for aptitude tests
            'personality_traits': Optional[Dict[str, int]],  # Personality analysis
            'identified_skills': List[str],  # Skills identified from quiz
            'completed_at': datetime,
            'time_taken': int,  # Time in seconds
        }


class ChatHistoryModel:
    """
    Chat History Model - Store user-bot conversations
    Collection: chat_history
    """
    
    @staticmethod
    def schema():
        return {
            '_id': ObjectId,
            'user_id': str,  # Reference to user
            'session_id': str,  # Chat session identifier
            'messages': List[Dict],  # List of message objects
            # Each message: {
            #   'type': 'user' or 'bot',
            #   'text': str,
            #   'timestamp': datetime,
            #   'intent': Optional[str],
            #   'keywords': Optional[List[str]]
            # }
            'started_at': datetime,
            'last_message_at': datetime,
            'is_active': bool,
        }
    
    @staticmethod
    def create_message(msg_type, text, intent=None, keywords=None):
        """Create a message object"""
        return {
            'type': msg_type,
            'text': text,
            'timestamp': datetime.utcnow(),
            'intent': intent,
            'keywords': keywords or []
        }


class AppointmentModel:
    """
    Appointment Model - Counsellor bookings
    Collection: appointments
    """
    
    @staticmethod
    def schema():
        return {
            '_id': ObjectId,
            'student_id': str,  # Reference to student user
            'counsellor_id': str,  # Reference to counsellor user
            'appointment_date': datetime,
            'duration': int,  # Duration in minutes
            'status': str,  # 'scheduled', 'completed', 'cancelled'
            'meeting_link': Optional[str],  # Video call link
            'notes': Optional[str],  # Session notes by counsellor
            'rating': Optional[int],  # Student rating (1-5)
            'feedback': Optional[str],  # Student feedback
            'payment_status': str,  # 'pending', 'completed', 'refunded'
            'payment_amount': float,
            'created_at': datetime,
            'updated_at': datetime,
        }


class CareerRecommendationModel:
    """
    Career Recommendations Model - Store AI recommendations for users
    Collection: career_recommendations
    """
    
    @staticmethod
    def schema():
        return {
            '_id': ObjectId,
            'user_id': str,  # Reference to user
            'recommendations': List[Dict],  # List of career recommendations
            # Each recommendation: {
            #   'career_name': str,
            #   'match_score': float (0-1),
            #   'reasons': List[str],
            #   'career_id': str
            # }
            'generated_at': datetime,
            'based_on': {
                'quiz_results': bool,
                'chat_analysis': bool,
                'profile_data': bool,
            },
            'user_feedback': Optional[str],
        }


# Database validation schemas for MongoDB
VALIDATION_SCHEMAS = {
    'users': {
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['name', 'email', 'password', 'role', 'created_at'],
            'properties': {
                'name': {'bsonType': 'string'},
                'email': {'bsonType': 'string'},
                'password': {'bsonType': 'string'},
                'role': {
                    'bsonType': 'string',
                    'enum': ['student', 'counsellor', 'admin']
                },
                'phone': {'bsonType': ['string', 'null']},
                'location': {'bsonType': ['string', 'null']},
                'profile': {'bsonType': 'object'},
                'created_at': {'bsonType': 'date'},
                'updated_at': {'bsonType': 'date'},
                'is_active': {'bsonType': 'bool'},
                'email_verified': {'bsonType': 'bool'},
            }
        }
    },
    'careers': {
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['name', 'category', 'description'],
            'properties': {
                'name': {'bsonType': 'string'},
                'category': {'bsonType': 'string'},
                'description': {'bsonType': 'string'},
            }
        }
    }
}


# Utility function to initialize collections
def initialize_collections(db):
    """
    Initialize all collections with validation schemas
    Call this function when setting up the database
    """
    collections = [
        'users', 'careers', 'courses', 'colleges',
        'quiz_results', 'chat_history', 'appointments',
        'career_recommendations'
    ]
    
    for collection in collections:
        if collection not in db.list_collection_names():
            db.create_collection(collection)
            print(f"✅ Created collection: {collection}")
    
    print("✅ All collections initialized!")