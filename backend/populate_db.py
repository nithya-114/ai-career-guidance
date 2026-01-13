"""
Database Population Script
Run this script to populate the database with sample data
"""

from pymongo import MongoClient
from datetime import datetime
import sys

# MongoDB connection
MONGODB_URI = 'mongodb://localhost:27017/'
DB_NAME = 'career_counselling'

def populate_database():
    """Populate database with sample data"""
    
    try:
        client = MongoClient(MONGODB_URI)
        db = client[DB_NAME]
        
        print("🔗 Connected to MongoDB")
        
        # Clear existing data (optional - comment out to keep existing data)
        # print("🗑️  Clearing existing data...")
        # db.careers.delete_many({})
        # db.courses.delete_many({})
        # db.colleges.delete_many({})
        # db.quiz_questions.delete_many({})
        
        # ==================== CAREERS ====================
        print("\n📊 Adding careers...")
        
        careers = [
            {
                'name': 'Software Engineer',
                'category': 'Technology',
                'description': 'Design, develop, and maintain software applications and systems',
                'related_interests': ['technology', 'problem-solving', 'coding', 'innovation', 'computers'],
                'required_skills': ['programming', 'logical-thinking', 'creativity', 'teamwork', 'attention-to-detail'],
                'related_subjects': ['Computer Science', 'Mathematics', 'Physics'],
                'personality_fit': {
                    'analytical': 8,
                    'creative': 6,
                    'detail-oriented': 8,
                    'independent': 7,
                    'team-player': 7
                },
                'work_environment': 'Office, Remote',
                'salary_range': '₹4-25 LPA',
                'growth_prospects': 'Excellent',
                'education_required': 'B.Tech/B.E. in Computer Science or related field',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'name': 'Doctor (MBBS)',
                'category': 'Healthcare',
                'description': 'Diagnose and treat patients, provide medical care and health guidance',
                'related_interests': ['helping-people', 'science', 'health', 'research', 'biology'],
                'required_skills': ['empathy', 'decision-making', 'attention-to-detail', 'communication', 'problem-solving'],
                'related_subjects': ['Biology', 'Chemistry', 'Physics'],
                'personality_fit': {
                    'empathetic': 9,
                    'patient': 8,
                    'analytical': 7,
                    'detail-oriented': 9,
                    'people-oriented': 8
                },
                'work_environment': 'Hospital, Clinic',
                'salary_range': '₹6-50 LPA',
                'growth_prospects': 'Very Good',
                'education_required': 'MBBS (5.5 years) + MD/MS specialization',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'name': 'Data Scientist',
                'category': 'Technology',
                'description': 'Analyze complex data to help organizations make better decisions',
                'related_interests': ['mathematics', 'statistics', 'technology', 'analysis', 'patterns'],
                'required_skills': ['analytical-thinking', 'programming', 'statistics', 'communication', 'problem-solving'],
                'related_subjects': ['Mathematics', 'Statistics', 'Computer Science'],
                'personality_fit': {
                    'analytical': 9,
                    'detail-oriented': 8,
                    'curious': 8,
                    'independent': 7,
                    'logical': 9
                },
                'work_environment': 'Office, Remote',
                'salary_range': '₹6-30 LPA',
                'growth_prospects': 'Excellent',
                'education_required': 'B.Tech/B.Sc. in Computer Science, Statistics, or Mathematics',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            # Add more careers here...
        ]
        
        result = db.careers.insert_many(careers)
        print(f"✅ Added {len(result.inserted_ids)} careers")
        
        # ==================== COURSES ====================
        print("\n📚 Adding courses...")
        
        courses = [
            {
                'name': 'B.Tech Computer Science',
                'career': ['Software Engineer', 'Data Scientist'],
                'duration': '4 years',
                'eligibility': '12th with PCM (60% minimum)',
                'entrance_exams': ['JEE Main', 'State CET', 'BITSAT'],
                'type': 'Engineering',
                'average_fees': '₹4-15 Lakhs',
                'top_specializations': ['AI & ML', 'Cybersecurity', 'Data Science', 'Cloud Computing'],
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'name': 'MBBS',
                'career': ['Doctor (MBBS)'],
                'duration': '5.5 years (including internship)',
                'eligibility': '12th with PCB (50% minimum)',
                'entrance_exams': ['NEET UG'],
                'type': 'Medical',
                'average_fees': '₹10-80 Lakhs',
                'top_specializations': ['General Medicine', 'Surgery', 'Pediatrics', 'Orthopedics'],
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            # Add more courses here...
        ]
        
        result = db.courses.insert_many(courses)
        print(f"✅ Added {len(result.inserted_ids)} courses")
        
        # ==================== COLLEGES ====================
        print("\n🏫 Adding colleges...")
        
        colleges = [
            {
                'name': 'Indian Institute of Technology (IIT) Delhi',
                'location': 'Delhi',
                'state': 'Delhi',
                'type': 'Government',
                'courses': ['B.Tech Computer Science', 'B.Tech Civil Engineering', 'B.Tech Mechanical Engineering'],
                'ranking': 1,
                'fees': '₹8-10 Lakhs (4 years)',
                'placements': {
                    'average': '₹18-20 LPA',
                    'highest': '₹1.2 Crore',
                    'percentage': '95%'
                },
                'website': 'https://www.iitd.ac.in',
                'facilities': ['Hostel', 'Library', 'Sports Complex', 'Labs', 'WiFi'],
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'name': 'All India Institute of Medical Sciences (AIIMS) Delhi',
                'location': 'Delhi',
                'state': 'Delhi',
                'type': 'Government',
                'courses': ['MBBS'],
                'ranking': 1,
                'fees': '₹5,856 (total)',
                'placements': {
                    'average': 'Not Applicable',
                    'highest': 'Not Applicable',
                    'percentage': '100% (Residency)'
                },
                'website': 'https://www.aiims.edu',
                'facilities': ['Hostel', 'Hospital', 'Library', 'Research Centers'],
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            # Add more colleges here...
        ]
        
        result = db.colleges.insert_many(colleges)
        print(f"✅ Added {len(result.inserted_ids)} colleges")
        
        # ==================== QUIZ QUESTIONS ====================
        print("\n❓ Adding quiz questions...")
        
        quiz_questions = [
            # Aptitude questions
            {
                'type': 'aptitude',
                'category': 'logical-reasoning',
                'question': 'If all roses are flowers and some flowers fade quickly, then which statement is definitely true?',
                'options': [
                    'All roses fade quickly',
                    'Some roses are flowers',
                    'Some flowers are not roses',
                    'No roses fade quickly'
                ],
                'correct_answer': 1,
                'skills_tested': ['logical-thinking', 'reasoning']
            },
            {
                'type': 'aptitude',
                'category': 'numerical',
                'question': 'What is 15% of 200?',
                'options': ['25', '30', '35', '40'],
                'correct_answer': 1,
                'skills_tested': ['mathematics', 'problem-solving']
            },
            # Personality questions
            {
                'type': 'personality',
                'category': 'work-style',
                'question': 'When working on a project, I prefer to:',
                'options': [
                    'Work alone at my own pace',
                    'Work with a small, close team',
                    'Lead a large team',
                    'Get guidance from a mentor'
                ],
                'trait_mapping': {
                    '0': {'independent': 2, 'team-player': -1},
                    '1': {'team-player': 2, 'collaborative': 2},
                    '2': {'leadership': 2, 'people-oriented': 2},
                    '3': {'receptive': 2, 'team-player': 1}
                }
            },
            # Add more questions here...
        ]
        
        result = db.quiz_questions.insert_many(quiz_questions)
        print(f"✅ Added {len(result.inserted_ids)} quiz questions")
        
        print("\n✨ Database population completed successfully!")
        print(f"\n📊 Summary:")
        print(f"   Careers: {db.careers.count_documents({})}")
        print(f"   Courses: {db.courses.count_documents({})}")
        print(f"   Colleges: {db.colleges.count_documents({})}")
        print(f"   Quiz Questions: {db.quiz_questions.count_documents({})}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == '__main__':
    print("🚀 Starting database population...")
    success = populate_database()
    sys.exit(0 if success else 1)