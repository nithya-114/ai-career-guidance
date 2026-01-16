"""
EXACT REPLACEMENT for your chat_routes.py
This matches your current structure exactly
"""

from flask import Blueprint, request, jsonify
from datetime import datetime

chat_bp = Blueprint('chat', __name__)


def get_chatbot_response(message: str, user_profile=None) -> dict:
    """
    Main function that returns chatbot response
    This is the EXACT function your code is calling
    """
    
    message_lower = message.lower()
    
    # Greeting
    if any(word in message_lower for word in ['hi', 'hello', 'hey', 'good morning', 'good afternoon']):
        return {
            'response': """Hello! 👋 I'm your AI Career Counsellor!

I can help you with:
🎯 **Career Guidance** - Find careers that match your interests
🏛️ **College Information** - Best colleges in Kerala  
📚 **Course Selection** - What to study after 10th/12th
💡 **Career Planning** - Personalized roadmaps

**Try asking:**
• "What career suits me?"
• "I like programming, what should I do?"
• "Engineering colleges in Kerala"
• "What to study after 12th?"

How can I help you today? 😊""",
            'intent': 'greeting',
            'suggestions': ['Career advice', 'Find colleges', 'Courses']
        }
    
    # Career inquiry
    elif any(phrase in message_lower for phrase in ['career', 'suit me', 'best for me', 'job', 'profession']):
        
        # Programming/Tech
        if any(word in message_lower for word in ['programming', 'coding', 'software', 'tech', 'computer']):
            return {
                'response': """Excellent! Technology is a fantastic field! 💻

**Top Tech Careers:**

**1. Software Engineer** ⭐
• Build applications and software
• Starting Salary: ₹3-15 lakhs/year
• Experienced: ₹15-50+ lakhs/year
• Companies: Google, Microsoft, Amazon

**2. Web Developer** 🌐
• Create websites and web apps
• Salary: ₹2.5-10 lakhs/year
• High freelance potential

**3. Data Scientist** 📊
• Analyze data, build ML models
• Starting: ₹5-20 lakhs/year
• Experienced: ₹20-80+ lakhs

**Education Path:**
• After 12th → B.Tech CSE (4 years)
• Entrance: JEE Main, KEAM

**Top Colleges in Kerala:**
• IIT Palakkad
• NIT Calicut
• Government Engineering Colleges

Want details about colleges or courses?""",
                'intent': 'career_advice',
                'suggestions': ['Engineering colleges', 'JEE preparation', 'B.Tech courses']
            }
        
        # Medical
        elif any(word in message_lower for word in ['doctor', 'medical', 'mbbs', 'health']):
            return {
                'response': """Great choice! Medical field is noble and rewarding! ⚕️

**Medical Careers:**

**1. MBBS (Doctor)** 👨‍⚕️
• Duration: 5.5 years
• Starting Salary: ₹6-20 lakhs/year
• Specialist: ₹50 lakhs - 2 crore+
• Entrance: NEET (competitive!)

**2. BDS (Dentist)** 🦷
• Duration: 5 years
• Salary: ₹3-10 lakhs/year
• Can open private practice

**3. Nursing** 👩‍⚕️
• Duration: 4 years
• Salary: ₹2-8 lakhs/year
• Can work abroad

**Requirements:**
• 12th with PCB
• NEET exam (600+ for govt colleges)

**Top Medical Colleges in Kerala:**
• Thiruvananthapuram Medical College
• Kottayam Medical College
• Amrita Institute

Want NEET preparation tips?""",
                'intent': 'career_advice',
                'suggestions': ['Medical colleges', 'NEET preparation', 'PCB stream']
            }
        
        # General career
        else:
            return {
                'response': """Let's find the perfect career for you! 🎯

**Popular Career Fields:**

💻 **Technology** - Software, IT, Data Science
• Salary: ₹4-50+ lakhs

⚕️ **Medical** - Doctor, Dentist, Nurse
• Salary: ₹6-80+ lakhs

⚙️ **Engineering** - Mechanical, Civil, Electrical
• Salary: ₹3-40+ lakhs

💼 **Business** - MBA, CA, Finance
• Salary: ₹5-50+ lakhs

🎨 **Creative** - Design, Architecture
• Salary: ₹3-30+ lakhs

**Tell me:**
• What subjects do you enjoy?
• What are you passionate about?

Or try saying:
• "I like programming"
• "I want to help people"
• "I'm good at math"

What interests you?""",
                'intent': 'career_inquiry',
                'suggestions': ['Technology careers', 'Medical careers', 'Take career quiz']
            }
    
    # College inquiry
    elif any(word in message_lower for word in ['college', 'university', 'institute']):
        
        if 'engineering' in message_lower:
            return {
                'response': """🏛️ **Engineering Colleges in Kerala**

**🥇 Premier Institutions:**

**IIT Palakkad**
• Branches: CSE, EE, ME, Civil
• Entrance: JEE Advanced
• Placements: ₹15-45 lakhs

**NIT Calicut**
• Branches: CSE, ECE, ME, Civil
• Entrance: JEE Main
• Placements: ₹10-30 lakhs

**🥈 Government Colleges:**

**CET Trivandrum**
• All major branches
• Entrance: KEAM
• Fees: ₹30,000/year

**GEC Thrissur**
• Strong placement record
• Fees: ₹35,000/year

**Entrance Exams:**
• JEE Main - For NITs
• JEE Advanced - For IITs
• KEAM - For Kerala colleges

Want admission details?""",
                'intent': 'college_info',
                'suggestions': ['JEE preparation', 'KEAM details', 'Fees structure']
            }
        
        elif 'medical' in message_lower:
            return {
                'response': """🏥 **Medical Colleges in Kerala**

**Government:**
• Thiruvananthapuram Medical College
• Kottayam Medical College
• Kozhikode Medical College

**Private:**
• Amrita Medical College, Kochi
• Believers Church Medical College

**Admission:**
• NEET exam (mandatory)
• Cutoff: 600+ for govt colleges

**Fees:**
• Govt: ₹4-5 lakhs (total)
• Private: ₹50 lakhs - 1 crore

Want NEET preparation tips?""",
                'intent': 'college_info',
                'suggestions': ['NEET preparation', 'Medical courses', 'PCB stream']
            }
        
        else:
            return {
                'response': """🎓 **College Information**

I can help with:
• **Engineering Colleges** - IIT, NIT, Govt colleges
• **Medical Colleges** - MBBS, BDS colleges
• **Arts & Science** - BA, B.Sc colleges
• **Management** - MBA, BBA colleges

Which field are you interested in?

Try asking:
• "Engineering colleges in Kerala"
• "Medical colleges"
• "Best colleges for CSE"""",
                'intent': 'college_inquiry',
                'suggestions': ['Engineering colleges', 'Medical colleges', 'Arts colleges']
            }
    
    # Course/Stream
    elif any(word in message_lower for word in ['course', 'stream', 'study', 'after 10', 'after 12']):
        
        if '10' in message or 'tenth' in message_lower:
            return {
                'response': """📚 **After 10th - Stream Selection**

**Science (PCM)**
• For: Engineering, Tech careers
• Leads to: B.Tech, BCA

**Science (PCB)**
• For: Medical careers
• Leads to: MBBS, BDS, Nursing

**Commerce**
• For: Business careers
• Leads to: CA, MBA, B.Com

**Arts**
• For: Creative, Law careers
• Leads to: BA, Design, Law

**How to choose?**
✓ Based on your interests
✓ Career goals
✓ Subjects you enjoy

What are you interested in?""",
                'intent': 'course_guidance',
                'suggestions': ['Science stream', 'Commerce stream', 'Career options']
            }
        
        else:
            return {
                'response': """🎓 **Course Options**

**After 12th Science:**
• B.Tech (Engineering)
• MBBS (Medical)
• B.Sc (Pure Science)

**After 12th Commerce:**
• B.Com
• BBA
• CA

**After 12th Arts:**
• BA
• Law (5 year)
• Design

What's your stream?""",
                'intent': 'course_guidance',
                'suggestions': ['Engineering', 'Medical', 'Commerce courses']
            }
    
    # Salary
    elif any(word in message_lower for word in ['salary', 'earn', 'income', 'pay']):
        return {
            'response': """💰 **Salary Information**

**Technology:**
• Software Engineer: ₹3-15 lakhs → ₹50+ lakhs

**Medical:**
• Doctor: ₹6-20 lakhs → ₹80+ lakhs

**Engineering:**
• Engineers: ₹3-8 lakhs → ₹40+ lakhs

**Business:**
• MBA: ₹8-25 lakhs
• CA: ₹6-20 lakhs → ₹80+ lakhs

**Factors:**
• Company (MNCs pay more)
• Location (metros pay 30-50% more)
• Skills and experience

Which field's salary do you want to know?""",
            'intent': 'salary_info',
            'suggestions': ['Software salary', 'Doctor salary', 'MBA salary']
        }
    
    # Confused
    elif any(word in message_lower for word in ['confused', "don't know", 'help', 'not sure']):
        return {
            'response': """Don't worry! Feeling confused is normal! 🤗

**Step-by-step approach:**

**1. Self-Assessment**
• What subjects do you enjoy?
• What activities make you happy?
• What are your strengths?

**2. Take Career Quiz** 📋
• 10-minute personality test
• Get matched with careers
• Free and personalized!

**3. Explore Options**
• Browse different careers
• Read about professions

**4. Talk to Expert** 👨‍💼
• Book counsellor session
• Get personalized guidance

**Right now:**
Tell me your interests!
Example: "I like programming"

What would you like to do?""",
            'intent': 'help_confused',
            'suggestions': ['Take quiz', 'Career options', 'Book counsellor']
        }
    
    # Thanks
    elif 'thank' in message_lower:
        return {
            'response': """You're welcome! 😊

Happy to help anytime with:
• Career guidance
• College information
• Course selection
• Study tips

Feel free to ask more questions!

Best wishes! 🌟""",
            'intent': 'thanks',
            'suggestions': ['Career quiz', 'Browse careers', 'Find colleges']
        }
    
    # Default
    else:
        return {
            'response': """I can help with:

🎯 **Career Guidance**
• Career recommendations
• Salary information

🏛️ **College Info**
• Find colleges in Kerala
• Admission details

📚 **Course Selection**
• After 10th/12th options
• Entrance exams

**Try asking:**
• "What career suits me?"
• "Engineering colleges in Kerala"
• "I like programming"
• "What after 12th?"

How can I help? 😊""",
            'intent': 'general',
            'suggestions': ['Career advice', 'Find colleges', 'Courses']
        }


@chat_bp.route('/message', methods=['POST'])
def send_message():
    """Send message endpoint - matches your current code"""
    try:
        from app import get_current_user, db
        
        data = request.json
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message required'}), 400
        
        # Get user profile if logged in
        user = get_current_user()
        user_profile = None
        if user:
            user_profile = {
                'class': user.get('class_level'),
                'interests': user.get('interests', [])
            }
        
        # Get response from chatbot
        response_data = get_chatbot_response(message, user_profile)
        
        # Save to database
        try:
            if user:
                conversation = {
                    'user_id': user['_id'],
                    'messages': [
                        {'role': 'user', 'content': message, 'timestamp': datetime.utcnow()},
                        {'role': 'assistant', 'content': response_data['response'], 'timestamp': datetime.utcnow()}
                    ],
                    'created_at': datetime.utcnow()
                }
                db.conversations.insert_one(conversation)
        except Exception as e:
            print(f"DB save error: {e}")
        
        return jsonify({
            'message': response_data['response'],
            'intent': response_data.get('intent', 'general'),
            'suggestions': response_data.get('suggestions', []),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        print(f"Chat error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'message': "I'm here to help! Ask me about careers, colleges, or courses.",
            'timestamp': datetime.utcnow().isoformat()
        }), 200


@chat_bp.route('/history', methods=['GET'])
def get_chat_history():
    """Get chat history"""
    try:
        from app import get_current_user, db
        
        user = get_current_user()
        if not user:
            return jsonify({'messages': []}), 200
        
        conversations = list(
            db.conversations
            .find({'user_id': user['_id']})
            .sort('created_at', -1)
            .limit(50)
        )
        
        messages = []
        for conv in conversations:
            for msg in conv.get('messages', []):
                messages.append({
                    'role': msg['role'],
                    'content': msg['content'],
                    'timestamp': msg['timestamp'].isoformat()
                })
        
        return jsonify({'messages': messages}), 200
    except Exception as e:
        print(f"History error: {e}")
        return jsonify({'messages': []}), 200


@chat_bp.route('/clear', methods=['DELETE'])
def clear_history():
    """Clear chat history"""
    try:
        from app import get_current_user, db
        
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Not authenticated'}), 401
        
        db.conversations.delete_many({'user_id': user['_id']})
        return jsonify({'message': 'Chat cleared'}), 200
    except Exception as e:
        print(f"Clear error: {e}")
        return jsonify({'error': 'Could not clear'}), 500


@chat_bp.route('/suggestions', methods=['GET'])
def get_suggestions():
    """Get suggested questions"""
    suggestions = [
        "What career suits me?",
        "Engineering colleges in Kerala",
        "I like programming",
        "What to study after 12th?",
        "How much do software engineers earn?",
        "Medical colleges in Kerala",
        "I'm confused about my career",
        "Stream selection after 10th"
    ]
    return jsonify({'suggestions': suggestions}), 200