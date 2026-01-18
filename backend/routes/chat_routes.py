# chat_routes.py
# Place this in backend/routes/ folder OR directly in backend/ folder

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from bson import ObjectId

# Create Blueprint
chat_bp = Blueprint('chat', __name__)

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
    print("✅ spaCy model loaded successfully")
except:
    print("⚠️ spaCy model not found. Run: python -m spacy download en_core_web_sm")
    nlp = None

# ==================== CAREER DATABASE ====================
CAREER_DATABASE = {
    "software_engineer": {
        "title": "Software Engineer",
        "keywords": ["coding", "programming", "software", "computer", "technology", "app", "website", "algorithm", "developer", "it", "python", "java"],
        "skills": ["problem-solving", "logical", "analytical", "creative", "detail-oriented"],
        "personality": ["introvert", "patient", "curious", "innovative", "focused"],
        "courses": ["Computer Science", "Software Engineering", "Information Technology", "Computer Applications"],
        "description": "Design, develop, and maintain software applications and systems",
        "salary_range": "₹4-15 LPA",
        "growth": "High"
    },
    "data_scientist": {
        "title": "Data Scientist",
        "keywords": ["data", "analysis", "statistics", "machine-learning", "ai", "research", "analytics", "python", "math", "algorithms"],
        "skills": ["analytical", "mathematical", "problem-solving", "programming", "statistical"],
        "personality": ["logical", "curious", "detail-oriented", "patient"],
        "courses": ["Data Science", "Statistics", "Computer Science", "Mathematics", "AI/ML"],
        "description": "Extract insights from complex data using advanced analytics",
        "salary_range": "₹6-20 LPA",
        "growth": "Very High"
    },
    "doctor": {
        "title": "Medical Doctor",
        "keywords": ["medicine", "health", "patient", "care", "biology", "science", "heal", "hospital", "medical", "surgery"],
        "skills": ["empathy", "precision", "communication", "problem-solving", "analytical"],
        "personality": ["caring", "patient", "hardworking", "compassionate", "responsible"],
        "courses": ["MBBS", "Medicine", "Biology", "Pre-Medical Studies"],
        "description": "Diagnose and treat illnesses, provide comprehensive medical care",
        "salary_range": "₹6-25 LPA",
        "growth": "High"
    },
    "teacher": {
        "title": "Teacher/Educator",
        "keywords": ["teaching", "education", "students", "learning", "explain", "knowledge", "school", "tutor", "training"],
        "skills": ["communication", "patience", "creativity", "leadership", "empathy"],
        "personality": ["extrovert", "patient", "caring", "organized", "enthusiastic"],
        "courses": ["Education", "B.Ed", "Subject Specialization", "Teaching Certification"],
        "description": "Educate and inspire students, facilitate learning and development",
        "salary_range": "₹3-10 LPA",
        "growth": "Moderate"
    },
    "business_analyst": {
        "title": "Business Analyst",
        "keywords": ["business", "analysis", "data", "strategy", "management", "finance", "market", "analytics", "consulting"],
        "skills": ["analytical", "communication", "problem-solving", "critical-thinking", "strategic"],
        "personality": ["logical", "detail-oriented", "strategic", "communicative"],
        "courses": ["Business Administration", "Management", "Economics", "Data Analytics", "MBA"],
        "description": "Analyze business processes and data to improve organizational efficiency",
        "salary_range": "₹5-18 LPA",
        "growth": "High"
    },
    "graphic_designer": {
        "title": "Graphic Designer",
        "keywords": ["design", "creative", "art", "visual", "graphics", "illustration", "photoshop", "drawing", "aesthetic"],
        "skills": ["creativity", "visual-thinking", "attention-to-detail", "artistic", "innovative"],
        "personality": ["creative", "artistic", "imaginative", "visual", "expressive"],
        "courses": ["Graphic Design", "Visual Arts", "Fine Arts", "Digital Design", "Animation"],
        "description": "Create visual content for digital and print media",
        "salary_range": "₹3-12 LPA",
        "growth": "Moderate"
    },
    "civil_engineer": {
        "title": "Civil Engineer",
        "keywords": ["construction", "buildings", "infrastructure", "engineering", "structure", "architecture", "design", "planning"],
        "skills": ["problem-solving", "analytical", "precision", "planning", "technical"],
        "personality": ["practical", "detail-oriented", "organized", "systematic"],
        "courses": ["Civil Engineering", "Structural Engineering", "Construction Management"],
        "description": "Design and oversee construction of infrastructure projects",
        "salary_range": "₹4-15 LPA",
        "growth": "Moderate"
    },
    "lawyer": {
        "title": "Lawyer",
        "keywords": ["law", "legal", "court", "justice", "advocate", "attorney", "rights", "litigation"],
        "skills": ["communication", "analytical", "persuasion", "research", "argumentation"],
        "personality": ["confident", "articulate", "logical", "argumentative", "ambitious"],
        "courses": ["Law", "LLB", "Legal Studies", "Criminal Justice"],
        "description": "Represent clients and provide legal advice on various matters",
        "salary_range": "₹4-20 LPA",
        "growth": "High"
    },
    "digital_marketer": {
        "title": "Digital Marketing Specialist",
        "keywords": ["marketing", "social-media", "advertising", "content", "seo", "digital", "branding", "campaigns"],
        "skills": ["creativity", "communication", "analytical", "strategic", "persuasion"],
        "personality": ["extrovert", "creative", "strategic", "adaptable"],
        "courses": ["Marketing", "Digital Marketing", "Business", "Communications", "MBA"],
        "description": "Develop and execute digital marketing strategies across platforms",
        "salary_range": "₹3-15 LPA",
        "growth": "Very High"
    },
    "mechanical_engineer": {
        "title": "Mechanical Engineer",
        "keywords": ["mechanical", "machines", "manufacturing", "engineering", "design", "automotive", "production"],
        "skills": ["problem-solving", "analytical", "technical", "precision", "innovative"],
        "personality": ["practical", "detail-oriented", "logical", "hands-on"],
        "courses": ["Mechanical Engineering", "Automobile Engineering", "Manufacturing"],
        "description": "Design, develop, and test mechanical devices and systems",
        "salary_range": "₹4-14 LPA",
        "growth": "Moderate"
    },
    "psychologist": {
        "title": "Psychologist",
        "keywords": ["psychology", "mental-health", "counseling", "therapy", "behavior", "mind", "emotions"],
        "skills": ["empathy", "listening", "analytical", "communication", "patience"],
        "personality": ["caring", "patient", "understanding", "intuitive", "compassionate"],
        "courses": ["Psychology", "Clinical Psychology", "Counseling", "Mental Health"],
        "description": "Study behavior and mental processes, provide therapeutic support",
        "salary_range": "₹3-12 LPA",
        "growth": "High"
    },
    "chartered_accountant": {
        "title": "Chartered Accountant",
        "keywords": ["accounting", "finance", "taxation", "audit", "numbers", "ca", "financial", "money"],
        "skills": ["analytical", "attention-to-detail", "mathematical", "organized", "ethical"],
        "personality": ["detail-oriented", "logical", "systematic", "responsible"],
        "courses": ["Commerce", "Accounting", "CA", "Finance", "Taxation"],
        "description": "Manage financial records, audits, and provide financial advice",
        "salary_range": "₹6-25 LPA",
        "growth": "High"
    }
}

# Session storage (in production, use MongoDB)
chat_sessions = {}

class ChatSession:
    def __init__(self, session_id, user_id=None):
        self.session_id = session_id
        self.user_id = user_id
        self.conversation_history = []
        self.user_profile = {
            "interests": [],
            "skills": [],
            "personality": [],
            "subjects": [],
            "hobbies": []
        }
        self.current_stage = "greeting"
        self.question_count = 0
        self.max_questions = 8
        self.created_at = datetime.utcnow()
        
    def add_message(self, role, content):
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })

# ==================== NLP FUNCTIONS ====================

def extract_keywords(text):
    """Extract keywords using spaCy"""
    if not nlp:
        return text.lower().split()
    
    doc = nlp(text.lower())
    keywords = []
    
    for token in doc:
        if token.pos_ in ['NOUN', 'VERB', 'ADJ'] and not token.is_stop:
            keywords.append(token.lemma_)
    
    return keywords if keywords else text.lower().split()

def calculate_career_match(user_profile):
    """Calculate match score for each career"""
    scores = {}
    
    for career_id, career_data in CAREER_DATABASE.items():
        score = 0
        
        # Match interests
        for interest in user_profile['interests']:
            if interest in career_data['keywords']:
                score += 3
        
        # Match skills
        for skill in user_profile['skills']:
            if skill in career_data['skills']:
                score += 2
        
        # Match personality
        for trait in user_profile['personality']:
            if trait in career_data['personality']:
                score += 2
        
        # Match subjects/hobbies
        for item in user_profile['subjects'] + user_profile['hobbies']:
            if item in career_data['keywords']:
                score += 1.5
        
        scores[career_id] = score
    
    sorted_careers = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_careers

def get_next_question(session):
    """Generate next question"""
    questions = {
        "greeting": "Hello! I'm your AI Career Counsellor. What's your name?",
        "interests": "Great! Let's explore your interests. What subjects or activities do you enjoy?",
        "skills": "What are your strongest skills? (e.g., problem-solving, creativity, communication)",
        "personality": "How would you describe your personality? Introverted or extroverted? Detail-oriented?",
        "hobbies": "What do you like to do in your free time?",
        "favorite_subjects": "Which academic subjects interest you most?",
        "work_preference": "Do you prefer working with people, technology, or creative tasks?",
        "future_vision": "Where do you see yourself in 5-10 years?",
        "analyze": "Let me analyze your responses and suggest careers..."
    }
    
    stages = ["greeting", "interests", "skills", "personality", "hobbies", 
              "favorite_subjects", "work_preference", "future_vision", "analyze"]
    
    if session.current_stage in stages:
        idx = stages.index(session.current_stage)
        if idx < len(stages) - 1:
            session.current_stage = stages[idx + 1]
            return questions[stages[idx + 1]]
    
    return questions.get(session.current_stage, "Tell me more.")

def process_response(session, user_message):
    """Process user response"""
    keywords = extract_keywords(user_message)
    stage = session.current_stage
    
    if stage == "interests":
        session.user_profile['interests'].extend(keywords)
    elif stage == "skills":
        session.user_profile['skills'].extend(keywords)
    elif stage == "personality":
        session.user_profile['personality'].extend(keywords)
    elif stage == "hobbies":
        session.user_profile['hobbies'].extend(keywords)
    elif stage == "favorite_subjects":
        session.user_profile['subjects'].extend(keywords)
    elif stage in ["work_preference", "future_vision"]:
        session.user_profile['interests'].extend(keywords)
    
    session.question_count += 1

def generate_recommendations(session):
    """Generate career recommendations"""
    career_matches = calculate_career_match(session.user_profile)
    top_careers = career_matches[:3]
    
    recommendations = []
    for career_id, score in top_careers:
        if score > 0:
            career = CAREER_DATABASE[career_id]
            recommendations.append({
                "career_id": career_id,
                "title": career['title'],
                "description": career['description'],
                "match_score": round(score, 2),
                "courses": career['courses'],
                "salary_range": career['salary_range'],
                "growth_potential": career['growth']
            })
    
    return recommendations

# ==================== ROUTES ====================

@chat_bp.route('/chat/start', methods=['POST', 'OPTIONS'])
def start_chat():
    """Start new chat session"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.json or {}
        session_id = data.get('session_id') or f"session_{datetime.now().timestamp()}"
        user_id = data.get('user_id')
        
        session = ChatSession(session_id, user_id)
        chat_sessions[session_id] = session
        
        greeting = get_next_question(session)
        session.add_message("bot", greeting)
        
        print(f"✅ Chat session started: {session_id}")
        
        return jsonify({
            "success": True,
            "session_id": session_id,
            "message": greeting,
            "stage": session.current_stage
        }), 200
        
    except Exception as e:
        print(f"❌ Start chat error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@chat_bp.route('/chat/message', methods=['POST', 'OPTIONS'])
def send_message():
    """Send message to chatbot"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.json
        session_id = data.get('session_id')
        user_message = data.get('message', '').strip()
        
        if not session_id or session_id not in chat_sessions:
            return jsonify({"success": False, "error": "Invalid session"}), 400
        
        if not user_message:
            return jsonify({"success": False, "error": "Message is empty"}), 400
        
        session = chat_sessions[session_id]
        session.add_message("user", user_message)
        
        process_response(session, user_message)
        
        # Check if ready for recommendations
        if session.current_stage == "analyze" or session.question_count >= session.max_questions:
            recommendations = generate_recommendations(session)
            
            if recommendations:
                response = "Based on our conversation, here are my top career recommendations:\n\n"
                for i, rec in enumerate(recommendations, 1):
                    response += f"{i}. **{rec['title']}** (Match: {rec['match_score']})\n"
                    response += f"   {rec['description']}\n"
                    response += f"   💰 {rec['salary_range']} | 📈 {rec['growth_potential']}\n\n"
                
                response += "Would you like more details or to speak with a counsellor?"
            else:
                response = "I need more information. What are you passionate about?"
                session.current_stage = "interests"
            
            session.add_message("bot", response)
            
            return jsonify({
                "success": True,
                "message": response,
                "recommendations": recommendations,
                "stage": "recommendations",
                "session_id": session_id
            }), 200
        
        # Get next question
        next_question = get_next_question(session)
        session.add_message("bot", next_question)
        
        progress = round((session.question_count / session.max_questions) * 100)
        
        return jsonify({
            "success": True,
            "message": next_question,
            "stage": session.current_stage,
            "session_id": session_id,
            "progress": progress
        }), 200
        
    except Exception as e:
        print(f"❌ Send message error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

@chat_bp.route('/chat/history/<session_id>', methods=['GET', 'OPTIONS'])
def get_history(session_id):
    """Get chat history"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        if session_id not in chat_sessions:
            return jsonify({"success": False, "error": "Session not found"}), 404
        
        session = chat_sessions[session_id]
        
        return jsonify({
            "success": True,
            "history": session.conversation_history,
            "profile": session.user_profile
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@chat_bp.route('/chat/end/<session_id>', methods=['POST', 'OPTIONS'])
def end_chat(session_id):
    """End chat session"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        if session_id in chat_sessions:
            session = chat_sessions[session_id]
            history = session.conversation_history
            profile = session.user_profile
            
            del chat_sessions[session_id]
            
            return jsonify({
                "success": True,
                "message": "Session ended",
                "history": history,
                "profile": profile
            }), 200
        
        return jsonify({"success": False, "error": "Session not found"}), 404
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@chat_bp.route('/chat/career-details/<career_id>', methods=['GET', 'OPTIONS'])
def get_career_details(career_id):
    """Get career details"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        if career_id in CAREER_DATABASE:
            return jsonify({
                "success": True,
                "career": CAREER_DATABASE[career_id]
            }), 200
        
        return jsonify({"success": False, "error": "Career not found"}), 404
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

print("✅ Chat routes module loaded")