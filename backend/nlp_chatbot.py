# nlp_chatbot_improved.py
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import spacy
from datetime import datetime
import re

# Create Blueprint
chatbot_bp = Blueprint('chatbot', __name__)

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
    print("✅ SpaCy model loaded successfully")
except:
    print("⚠️ Please install: python -m spacy download en_core_web_sm")
    nlp = None

# ==================== CAREER DATABASE ====================
CAREER_DATABASE = {
    "software_engineer": {
        "title": "Software Engineer",
        "keywords": ["coding", "programming", "software", "computer", "technology", "app", "website", 
                     "algorithm", "developer", "it", "python", "java", "code", "tech", "build"],
        "skills": ["problem-solving", "logical", "analytical", "creative", "detail-oriented"],
        "personality": ["introvert", "patient", "curious", "innovative", "focused"],
        "courses": ["Computer Science", "Software Engineering", "Information Technology", "Computer Applications"],
        "description": "Design, develop, and maintain software applications and systems",
        "salary_range": "₹4-15 LPA",
        "growth": "High"
    },
    "data_scientist": {
        "title": "Data Scientist",
        "keywords": ["data", "analysis", "statistics", "machine-learning", "ai", "research", "analytics", 
                     "python", "math", "algorithms", "ml", "artificial intelligence"],
        "skills": ["analytical", "mathematical", "problem-solving", "programming", "statistical"],
        "personality": ["logical", "curious", "detail-oriented", "patient"],
        "courses": ["Data Science", "Statistics", "Computer Science", "Mathematics", "AI/ML"],
        "description": "Extract insights from complex data using advanced analytics",
        "salary_range": "₹6-20 LPA",
        "growth": "Very High"
    },
    "doctor": {
        "title": "Medical Doctor",
        "keywords": ["medicine", "health", "patient", "care", "biology", "science", "heal", "hospital", 
                     "medical", "surgery", "doctor", "physician", "treatment"],
        "skills": ["empathy", "precision", "communication", "problem-solving", "analytical"],
        "personality": ["caring", "patient", "hardworking", "compassionate", "responsible"],
        "courses": ["MBBS", "Medicine", "Biology", "Pre-Medical Studies"],
        "description": "Diagnose and treat illnesses, provide comprehensive medical care",
        "salary_range": "₹6-25 LPA",
        "growth": "High"
    },
    "teacher": {
        "title": "Teacher/Educator",
        "keywords": ["teaching", "education", "students", "learning", "explain", "knowledge", "school", 
                     "tutor", "training", "teach", "professor", "instructor"],
        "skills": ["communication", "patience", "creativity", "leadership", "empathy"],
        "personality": ["extrovert", "patient", "caring", "organized", "enthusiastic"],
        "courses": ["Education", "B.Ed", "Subject Specialization", "Teaching Certification"],
        "description": "Educate and inspire students, facilitate learning and development",
        "salary_range": "₹3-10 LPA",
        "growth": "Moderate"
    },
    "business_analyst": {
        "title": "Business Analyst",
        "keywords": ["business", "analysis", "data", "strategy", "management", "finance", "market", 
                     "analytics", "consulting", "commerce", "economics"],
        "skills": ["analytical", "communication", "problem-solving", "critical-thinking", "strategic"],
        "personality": ["logical", "detail-oriented", "strategic", "communicative"],
        "courses": ["Business Administration", "Management", "Economics", "Data Analytics", "MBA"],
        "description": "Analyze business processes and data to improve organizational efficiency",
        "salary_range": "₹5-18 LPA",
        "growth": "High"
    },
    "graphic_designer": {
        "title": "Graphic Designer",
        "keywords": ["design", "creative", "art", "visual", "graphics", "illustration", "photoshop", 
                     "drawing", "aesthetic", "ui", "ux", "creative", "artist"],
        "skills": ["creativity", "visual-thinking", "attention-to-detail", "artistic", "innovative"],
        "personality": ["creative", "artistic", "imaginative", "visual", "expressive"],
        "courses": ["Graphic Design", "Visual Arts", "Fine Arts", "Digital Design", "Animation"],
        "description": "Create visual content for digital and print media",
        "salary_range": "₹3-12 LPA",
        "growth": "Moderate"
    },
    "civil_engineer": {
        "title": "Civil Engineer",
        "keywords": ["construction", "buildings", "infrastructure", "engineering", "structure", 
                     "architecture", "design", "planning", "civil", "bridge", "road"],
        "skills": ["problem-solving", "analytical", "precision", "planning", "technical"],
        "personality": ["practical", "detail-oriented", "organized", "systematic"],
        "courses": ["Civil Engineering", "Structural Engineering", "Construction Management"],
        "description": "Design and oversee construction of infrastructure projects",
        "salary_range": "₹4-15 LPA",
        "growth": "Moderate"
    },
    "lawyer": {
        "title": "Lawyer",
        "keywords": ["law", "legal", "court", "justice", "advocate", "attorney", "rights", 
                     "litigation", "lawyer", "judge", "case"],
        "skills": ["communication", "analytical", "persuasion", "research", "argumentation"],
        "personality": ["confident", "articulate", "logical", "argumentative", "ambitious"],
        "courses": ["Law", "LLB", "Legal Studies", "Criminal Justice"],
        "description": "Represent clients and provide legal advice on various matters",
        "salary_range": "₹4-20 LPA",
        "growth": "High"
    },
    "digital_marketer": {
        "title": "Digital Marketing Specialist",
        "keywords": ["marketing", "social-media", "advertising", "content", "seo", "digital", 
                     "branding", "campaigns", "social media", "online"],
        "skills": ["creativity", "communication", "analytical", "strategic", "persuasion"],
        "personality": ["extrovert", "creative", "strategic", "adaptable"],
        "courses": ["Marketing", "Digital Marketing", "Business", "Communications", "MBA"],
        "description": "Develop and execute digital marketing strategies across platforms",
        "salary_range": "₹3-15 LPA",
        "growth": "Very High"
    },
    "mechanical_engineer": {
        "title": "Mechanical Engineer",
        "keywords": ["mechanical", "machines", "manufacturing", "engineering", "design", "automotive", 
                     "production", "engine", "machinery"],
        "skills": ["problem-solving", "analytical", "technical", "precision", "innovative"],
        "personality": ["practical", "detail-oriented", "logical", "hands-on"],
        "courses": ["Mechanical Engineering", "Automobile Engineering", "Manufacturing"],
        "description": "Design, develop, and test mechanical devices and systems",
        "salary_range": "₹4-14 LPA",
        "growth": "Moderate"
    },
    "psychologist": {
        "title": "Psychologist",
        "keywords": ["psychology", "mental-health", "counseling", "therapy", "behavior", "mind", 
                     "emotions", "mental", "therapist", "counselor"],
        "skills": ["empathy", "listening", "analytical", "communication", "patience"],
        "personality": ["caring", "patient", "understanding", "intuitive", "compassionate"],
        "courses": ["Psychology", "Clinical Psychology", "Counseling", "Mental Health"],
        "description": "Study behavior and mental processes, provide therapeutic support",
        "salary_range": "₹3-12 LPA",
        "growth": "High"
    },
    "chartered_accountant": {
        "title": "Chartered Accountant",
        "keywords": ["accounting", "finance", "taxation", "audit", "numbers", "ca", "financial", 
                     "money", "accounts", "tax"],
        "skills": ["analytical", "attention-to-detail", "mathematical", "organized", "ethical"],
        "personality": ["detail-oriented", "logical", "systematic", "responsible"],
        "courses": ["Commerce", "Accounting", "CA", "Finance", "Taxation"],
        "description": "Manage financial records, audits, and provide financial advice",
        "salary_range": "₹6-25 LPA",
        "growth": "High"
    }
}

# ==================== SESSION STORAGE ====================
chat_sessions = {}

class ChatSession:
    def __init__(self, session_id):
        self.session_id = session_id
        self.conversation_history = []
        self.user_profile = {
            "interests": [],
            "skills": [],
            "personality": [],
            "subjects": [],
            "hobbies": [],
            "dislikes": []
        }
        self.context = "greeting"
        self.has_basic_info = False
        
    def add_message(self, role, content):
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

# ==================== IMPROVED NLP PROCESSING ====================
def extract_keywords_advanced(text):
    """Extract meaningful keywords using spaCy with better filtering"""
    if not nlp:
        return text.lower().split()
    
    doc = nlp(text.lower())
    keywords = []
    
    # Extract nouns, verbs, adjectives, and proper nouns
    for token in doc:
        if token.pos_ in ['NOUN', 'VERB', 'ADJ', 'PROPN'] and not token.is_stop and len(token.text) > 2:
            keywords.append(token.lemma_)
    
    # Also extract noun chunks (multi-word phrases)
    for chunk in doc.noun_chunks:
        if len(chunk.text.split()) > 1:  # Multi-word phrases
            keywords.append(chunk.text.lower())
    
    return keywords if keywords else text.lower().split()

def detect_intent(text):
    """Detect user intent from message"""
    text_lower = text.lower()
    
    # Greeting intents
    if any(word in text_lower for word in ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon']):
        return 'greeting'
    
    # Question intents
    if any(word in text_lower for word in ['what is', 'what are', 'tell me about', 'explain', 'how to', 'can you']):
        return 'question'
    
    # Recommendation intents
    if any(phrase in text_lower for phrase in ['recommend', 'suggest', 'which career', 'what career', 
                                                 'best career', 'job for', 'which job', 'what should i',
                                                 'help me choose', 'career options']):
        return 'recommend'
    
    # Details intent
    if any(phrase in text_lower for phrase in ['more about', 'details', 'tell me more', 'information about',
                                                 'learn more', 'know more']):
        return 'details'
    
    # Interest/skill sharing
    if any(word in text_lower for word in ['like', 'love', 'enjoy', 'interested', 'good at', 'skilled', 'passion']):
        return 'sharing_interest'
    
    # Dislike sharing
    if any(word in text_lower for word in ['hate', 'dislike', 'not good at', 'boring', 'don\'t like']):
        return 'sharing_dislike'
    
    # Affirmation
    if text_lower in ['yes', 'yeah', 'yep', 'sure', 'ok', 'okay', 'definitely', 'of course']:
        return 'affirmation'
    
    # Negation
    if text_lower in ['no', 'nope', 'nah', 'not really', 'i don\'t think so']:
        return 'negation'
    
    return 'general'

def extract_entities(text):
    """Extract named entities like subjects, skills, hobbies"""
    entities = {
        'subjects': [],
        'skills': [],
        'hobbies': [],
        'personality': []
    }
    
    text_lower = text.lower()
    
    # Subject detection
    subjects = ['math', 'mathematics', 'physics', 'chemistry', 'biology', 'history', 'geography', 
                'english', 'computer', 'science', 'economics', 'commerce', 'arts', 'literature',
                'political science', 'sociology', 'psychology']
    for subject in subjects:
        if subject in text_lower:
            entities['subjects'].append(subject)
    
    # Skills detection
    skills = ['programming', 'coding', 'communication', 'leadership', 'problem-solving', 'analytical',
              'creative', 'writing', 'speaking', 'designing', 'drawing', 'teamwork', 'management',
              'organization', 'planning', 'research']
    for skill in skills:
        if skill in text_lower or skill.replace('-', ' ') in text_lower:
            entities['skills'].append(skill)
    
    # Hobby detection
    hobbies = ['reading', 'writing', 'painting', 'drawing', 'music', 'singing', 'dancing', 'sports',
               'football', 'cricket', 'basketball', 'coding', 'gaming', 'photography', 'cooking',
               'gardening', 'traveling', 'volunteering']
    for hobby in hobbies:
        if hobby in text_lower:
            entities['hobbies'].append(hobby)
    
    # Personality traits
    traits = ['introvert', 'extrovert', 'creative', 'logical', 'organized', 'spontaneous', 'patient',
              'ambitious', 'detail-oriented', 'big-picture', 'analytical', 'emotional', 'practical']
    for trait in traits:
        if trait in text_lower:
            entities['personality'].append(trait)
    
    return entities

def calculate_career_match(user_profile):
    """Calculate match score for each career based on user profile"""
    scores = {}
    
    for career_id, career_data in CAREER_DATABASE.items():
        score = 0
        
        # Match interests with keywords (high weight)
        for interest in user_profile['interests']:
            if any(interest in keyword or keyword in interest for keyword in career_data['keywords']):
                score += 5
        
        # Match skills (medium weight)
        for skill in user_profile['skills']:
            if any(skill in s or s in skill for s in career_data['skills']):
                score += 3
        
        # Match personality (medium weight)
        for trait in user_profile['personality']:
            if any(trait in p or p in trait for p in career_data['personality']):
                score += 3
        
        # Match subjects (low-medium weight)
        for subject in user_profile['subjects']:
            if any(subject in keyword or keyword in subject for keyword in career_data['keywords']):
                score += 2
        
        # Match hobbies (low weight)
        for hobby in user_profile['hobbies']:
            if any(hobby in keyword or keyword in hobby for keyword in career_data['keywords']):
                score += 1.5
        
        # Penalty for dislikes
        for dislike in user_profile['dislikes']:
            if any(dislike in keyword or keyword in dislike for keyword in career_data['keywords']):
                score -= 2
        
        scores[career_id] = max(score, 0)  # Don't allow negative scores
    
    # Sort by score
    sorted_careers = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_careers

def generate_natural_response(session, user_message, intent):
    """Generate natural, context-aware responses"""
    
    # Update user profile based on message
    keywords = extract_keywords_advanced(user_message)
    entities = extract_entities(user_message)
    
    # Add extracted entities to profile
    session.user_profile['interests'].extend(keywords[:5])  # Limit to avoid too many
    session.user_profile['subjects'].extend(entities['subjects'])
    session.user_profile['skills'].extend(entities['skills'])
    session.user_profile['hobbies'].extend(entities['hobbies'])
    session.user_profile['personality'].extend(entities['personality'])
    
    # Remove duplicates
    for key in session.user_profile:
        session.user_profile[key] = list(set(session.user_profile[key]))
    
    # Check if we have enough info
    total_info = sum(len(v) for v in session.user_profile.values())
    session.has_basic_info = total_info >= 5
    
    # Response based on intent
    if intent == 'greeting':
        return "Hello! I'm here to help you explore career options. Tell me, what are you interested in? What subjects do you enjoy or what are you passionate about?"
    
    elif intent == 'recommend':
        if not session.has_basic_info:
            return "I'd love to recommend careers! But first, tell me a bit more about yourself. What subjects do you like? What are you good at? What do you enjoy doing?"
        
        career_matches = calculate_career_match(session.user_profile)
        top_careers = career_matches[:3]
        
        if top_careers[0][1] == 0:  # No matches
            return "I need a bit more information to make good recommendations. What are your favorite subjects or activities?"
        
        response = "Based on what you've told me, here are some careers that might suit you:\n\n"
        for i, (career_id, score) in enumerate(top_careers, 1):
            if score > 0:
                career = CAREER_DATABASE[career_id]
                response += f"{i}. **{career['title']}** - {career['description']}\n"
                response += f"   Salary: {career['salary_range']} | Growth: {career['growth']}\n\n"
        
        response += "Would you like to know more about any of these careers?"
        session.context = 'recommendations_given'
        return response
    
    elif intent == 'details':
        # Check if asking about a specific career
        for career_id, career_data in CAREER_DATABASE.items():
            if career_data['title'].lower() in user_message.lower():
                career = career_data
                response = f"**{career['title']}**\n\n"
                response += f"{career['description']}\n\n"
                response += f"💰 Salary Range: {career['salary_range']}\n"
                response += f"📈 Growth Potential: {career['growth']}\n"
                response += f"📚 Recommended Courses: {', '.join(career['courses'][:3])}\n"
                response += f"🎯 Key Skills: {', '.join(career['skills'][:3])}\n\n"
                response += "Would you like to know about other career options?"
                return response
        
        return "Which career would you like to know more about? Just mention the name!"
    
    elif intent == 'sharing_interest':
        if entities['subjects'] or entities['skills'] or entities['hobbies']:
            return "That's great! " + (
                f"So you're interested in {', '.join(entities['subjects'] + entities['skills'] + entities['hobbies'][:2])}. " if entities['subjects'] or entities['skills'] or entities['hobbies'] else ""
            ) + "What else do you enjoy or excel at? Or would you like me to suggest some careers based on what I know so far?"
        return "Interesting! Tell me more about what you like or what you're good at."
    
    elif intent == 'question':
        # Try to answer general career questions
        if 'salary' in user_message.lower() or 'pay' in user_message.lower():
            return "Salaries vary by career, experience, and location. For example, Software Engineers typically earn ₹4-15 LPA, while Data Scientists can earn ₹6-20 LPA. Would you like salary information for a specific career?"
        
        if 'course' in user_message.lower() or 'study' in user_message.lower():
            return "The courses you should take depend on your career goal. Tell me what career interests you, and I can suggest the right courses!"
        
        return "That's a good question! To help you better, tell me about your interests and what you enjoy doing, and I can suggest careers that align with them."
    
    else:  # general intent
        if not session.has_basic_info:
            return "Thanks for sharing! To give you the best career suggestions, tell me more about what subjects you like, what you're good at, or what you enjoy doing in your free time."
        else:
            return "Got it! Would you like me to recommend some careers based on what you've told me? Or is there anything else you'd like to share?"

# ==================== API ENDPOINTS ====================
@chatbot_bp.route('/chat/start', methods=['POST'])
@cross_origin()
def start_chat():
    """Initialize a new chat session"""
    try:
        data = request.json or {}
        session_id = data.get('session_id') or f"session_{datetime.now().timestamp()}"
        
        # Create new session
        session = ChatSession(session_id)
        chat_sessions[session_id] = session
        
        greeting = "Hi! I'm your AI Career Guide. I'm here to help you discover careers that match your interests and skills. What subjects or activities do you enjoy?"
        session.add_message("bot", greeting)
        
        return jsonify({
            "success": True,
            "session_id": session_id,
            "message": greeting
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@chatbot_bp.route('/chat/message', methods=['POST'])
@cross_origin()
def send_message():
    """Handle user message and generate intelligent response"""
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
        
        # Detect intent and generate response
        intent = detect_intent(user_message)
        response = generate_natural_response(session, user_message, intent)
        
        session.add_message("bot", response)
        
        # Generate recommendations if requested
        recommendations = []
        if intent == 'recommend' and session.has_basic_info:
            career_matches = calculate_career_match(session.user_profile)
            for career_id, score in career_matches[:3]:
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
        
        return jsonify({
            "success": True,
            "message": response,
            "session_id": session_id,
            "intent": intent,
            "has_basic_info": session.has_basic_info,
            "recommendations": recommendations if recommendations else []
        })
        
    except Exception as e:
        print(f"Error in send_message: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

@chatbot_bp.route('/chat/history/<session_id>', methods=['GET'])
@cross_origin()
def get_history(session_id):
    """Get conversation history"""
    try:
        if session_id not in chat_sessions:
            return jsonify({"success": False, "error": "Session not found"}), 404
        
        session = chat_sessions[session_id]
        
        return jsonify({
            "success": True,
            "history": session.conversation_history,
            "profile": session.user_profile
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@chatbot_bp.route('/chat/end/<session_id>', methods=['POST'])
@cross_origin()
def end_chat(session_id):
    """End chat session"""
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
            })
        
        return jsonify({"success": False, "error": "Session not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@chatbot_bp.route('/chat/career-details/<career_id>', methods=['GET'])
@cross_origin()
def get_career_details(career_id):
    """Get detailed information about a specific career"""
    try:
        if career_id in CAREER_DATABASE:
            career = CAREER_DATABASE[career_id]
            return jsonify({
                "success": True,
                "career": career
            })
        
        return jsonify({"success": False, "error": "Career not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Export blueprint
def init_chatbot(app):
    """Initialize chatbot with Flask app"""
    app.register_blueprint(chatbot_bp, url_prefix='/api')
    print("✅ Improved chatbot module initialized")