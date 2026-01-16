"""
Enhanced NLP Chatbot Module for Career Counselling
Detailed, helpful responses for students
"""

import re
from datetime import datetime
from typing import Dict, List, Optional
import random

class CareerChatbot:
    """
    Enhanced chatbot for career counselling with detailed responses
    """
    
    def __init__(self):
        self.context = {}
        self.conversation_history = []
        
        # Intent patterns
        self.intent_patterns = {
            'greeting': [
                r'\b(hi|hello|hey|good\s+(morning|afternoon|evening)|greetings)\b',
            ],
            'goodbye': [
                r'\b(bye|goodbye|see\s+you|talk\s+later|exit|quit)\b',
            ],
            'interests': [
                r'\b(interest|like|enjoy|love|passionate|hobby)\b',
            ],
            'careers': [
                r'\b(career|job|profession|suit\s+me|best\s+for\s+me)\b',
            ],
            'education': [
                r'\b(college|university|course|degree|study)\b',
            ],
            'confused': [
                r'\b(confused|don\'t\s+know|help|lost|not\s+sure)\b',
            ],
            'salary': [
                r'\b(salary|earn|income|pay)\b',
            ],
        }
        
        # Interest keywords
        self.interest_keywords = {
            'technology': ['computer', 'programming', 'coding', 'software', 'tech', 'ai', 'app', 'website'],
            'medical': ['medicine', 'doctor', 'health', 'hospital', 'patient', 'medical'],
            'engineering': ['engineer', 'mechanical', 'civil', 'electrical', 'building'],
            'business': ['business', 'management', 'marketing', 'entrepreneur'],
        }
    
    def preprocess_text(self, text: str) -> str:
        """Clean and normalize text"""
        return text.lower().strip()
    
    def detect_intent(self, text: str) -> str:
        """Detect user intent from text"""
        text = self.preprocess_text(text)
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return intent
        
        return 'general'
    
    def extract_interests(self, text: str) -> List[str]:
        """Extract interests from user message"""
        text = self.preprocess_text(text)
        interests = []
        
        for interest, keywords in self.interest_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    interests.append(interest)
                    break
        
        return list(set(interests))
    
    def generate_response(self, user_message: str, user_profile: Optional[Dict] = None) -> Dict:
        """Generate intelligent response"""
        
        intent = self.detect_intent(user_message)
        interests = self.extract_interests(user_message)
        
        response = self._generate_intent_response(intent, user_message, interests)
        
        return {
            'response': response,
            'intent': intent,
            'suggestions': self._get_quick_replies(intent)
        }
    
    def _generate_intent_response(self, intent: str, message: str, interests: List[str]) -> str:
        """Generate detailed response based on intent"""
        
        message_lower = message.lower()
        
        # GREETING
        if intent == 'greeting':
            return """Hello! 👋 I'm your AI Career Counsellor!

I can help you with:
🎯 **Career Guidance** - Discover careers matching your interests
🏛️ **College Information** - Best colleges in Kerala
📚 **Course Selection** - What to study after 10th/12th
💡 **Career Planning** - Personalized roadmaps

**Try asking:**
• "What career suits me?"
• "I like programming, what should I do?"
• "Engineering colleges in Kerala"
• "What to study after 12th?"

How can I help you today? 😊"""
        
        # CAREERS - with specific interest
        elif intent == 'careers' or interests:
            
            # Technology/Programming
            if 'technology' in interests or any(word in message_lower for word in ['programming', 'coding', 'software', 'tech', 'computer']):
                return """Excellent! Technology is an amazing field! 💻

**🌟 Top Technology Careers:**

**1. Software Engineer** ⭐
• Build applications and software systems
• Starting Salary: ₹3-15 lakhs/year
• Experienced: ₹15-50+ lakhs/year
• Top Companies: Google, Microsoft, Amazon, Infosys

**2. Web Developer** 🌐
• Create websites and web applications
• Salary: ₹2.5-10 lakhs/year
• High freelance potential!

**3. Data Scientist** 📊
• Analyze data, build ML models
• Starting: ₹5-20 lakhs/year
• Experienced: ₹20-80+ lakhs/year

**4. Mobile App Developer** 📱
• Create iOS/Android apps
• Salary: ₹3-12 lakhs/year

**📚 Education Path:**
After 12th → B.Tech Computer Science (4 years)
**Entrance:** JEE Main, KEAM (Kerala)

**🏛️ Top Colleges in Kerala:**
• IIT Palakkad - JEE Advanced
• NIT Calicut - JEE Main
• Government Engineering Colleges - KEAM

**💡 Next Steps:**
1. Learn programming basics (Python recommended!)
2. Build projects for portfolio
3. Prepare for JEE/KEAM
4. Join coding communities

Want to know about colleges or entrance exams?"""
            
            # Medical
            elif 'medical' in interests or any(word in message_lower for word in ['doctor', 'medical', 'mbbs', 'health']):
                return """Wonderful! Medical field is noble and rewarding! ⚕️

**🏥 Medical Career Options:**

**1. MBBS (Doctor)** 👨‍⚕️
• Duration: 5.5 years (+ 1 year internship)
• Starting Salary: ₹6-20 lakhs/year
• Specialist: ₹50 lakhs - 2 crore+/year
• **Entrance:** NEET (competitive!)

**2. BDS (Dentist)** 🦷
• Duration: 5 years
• Salary: ₹3-10 lakhs/year
• Can open private practice

**3. B.Sc Nursing** 👩‍⚕️
• Duration: 4 years
• Salary: ₹2-8 lakhs/year
• Can work abroad (USA, UK, Middle East)

**4. Pharmacy** 💊
• Duration: 4 years (B.Pharm)
• Salary: ₹3-8 lakhs/year
• Can open pharmacy

**📋 Requirements:**
• 12th with Physics, Chemistry, Biology
• NEET exam (600+ for govt colleges)

**🏛️ Medical Colleges in Kerala:**
**Government:**
• Thiruvananthapuram Medical College
• Kottayam Medical College
• Kozhikode Medical College

**Private:**
• Amrita Medical College, Kochi

**💰 Fees:**
• Govt: ₹4-5 lakhs (total MBBS)
• Private: ₹50 lakhs - 1 crore

**📚 NEET Preparation:**
• Start in Class 11
• NCERT is crucial (80% from NCERT!)
• Join coaching if possible
• Target: 650+ for govt college

Want NEET preparation tips or college details?"""
            
            # Engineering
            elif 'engineering' in interests or 'engineer' in message_lower:
                return """Great! Engineering offers diverse opportunities! ⚙️

**🔧 Engineering Branches:**

**1. Computer Science** 💻 Highest Demand
• Software, AI, ML, App Development
• Starting: ₹4-15 lakhs/year
• Experienced: ₹20-50+ lakhs

**2. Mechanical** ⚙️
• Design, Manufacturing, Automobiles
• Starting: ₹3-8 lakhs/year

**3. Civil** 🏗️
• Construction, Infrastructure
• Starting: ₹3-7 lakhs/year

**4. Electrical** ⚡
• Power systems, Electronics
• Starting: ₹3-8 lakhs/year

**📚 Education:**
• Duration: 4 years (B.Tech)
• After 12th with PCM
• **Entrance:** JEE Main, JEE Advanced, KEAM

**🏛️ Top Colleges in Kerala:**
• **IIT Palakkad** - JEE Advanced
• **NIT Calicut** - JEE Main
• **CET Trivandrum** - KEAM
• **GEC Thrissur** - KEAM

**💰 Fees:**
• Govt: ₹30,000-50,000/year
• Private: ₹80,000-2 lakhs/year

Which branch interests you?"""
            
            # General career inquiry
            else:
                return """Let me help you find the perfect career! 🎯

**🌟 Popular Career Fields:**

**Technology 💻**
• Software Engineer, Data Scientist
• Salary: ₹4-50+ lakhs

**Medical ⚕️**
• Doctor, Dentist, Nurse
• Salary: ₹6-80+ lakhs

**Engineering ⚙️**
• CS, Mechanical, Civil, Electrical
• Salary: ₹3-40+ lakhs

**Business 💼**
• MBA, CA, Finance
• Salary: ₹5-50+ lakhs

**Creative 🎨**
• Design, Architecture
• Salary: ₹3-30+ lakhs

**📋 To recommend better, tell me:**
• What subjects do you enjoy?
• What are you passionate about?
• Current class (10th/12th)?

Try saying:
• "I like programming"
• "I want to help people"
• "I'm good at math"

What interests you?"""
        
        # EDUCATION - College inquiry
        elif intent == 'education':
            if 'engineering' in message_lower:
                return """🏛️ **Engineering Colleges in Kerala**

**🥇 Premier Institutions:**

**IIT Palakkad**
• Branches: CSE, EE, ME, Civil
• Entrance: JEE Advanced
• Average Package: ₹15-45 lakhs

**NIT Calicut**
• Branches: CSE, ECE, ME, Civil
• Entrance: JEE Main
• Average Package: ₹10-30 lakhs

**🥈 Government Colleges:**

**CET Trivandrum**
• All major branches
• Entrance: KEAM
• Fees: ₹30,000/year

**GEC Thrissur**
• Strong placements
• Fees: ₹35,000/year

**TKM Kollam**
• Good faculty
• Fees: ₹40,000/year

**📋 Admission:**
• **IIT:** JEE Advanced
• **NIT:** JEE Main (98+ percentile)
• **Govt:** KEAM (Rank <5000)

**💰 Fees:**
• IIT/NIT: ₹1-2.5 lakhs/year
• Govt: ₹30-50k/year
• Private: ₹80k-2 lakhs/year

Want admission process details?"""
            
            elif 'medical' in message_lower:
                return """🏥 **Medical Colleges in Kerala**

**Government Medical Colleges:**
• Thiruvananthapuram Medical College
• Kottayam Medical College
• Kozhikode Medical College
• Thrissur Medical College
• Alappuzha Medical College

**Private Medical Colleges:**
• Amrita Institute, Kochi
• Believers Church Medical College

**📋 NEET & Admission:**
• **Cutoff:** 600-650+ (Govt colleges)
• **Private:** 450-550
• **All India Quota:** 15% seats
• **State Quota:** 85% seats

**💰 Complete Cost:**
• **Govt:** ₹4-5 lakhs (entire MBBS)
• **Private:** ₹50 lakhs - 1 crore

**⏰ Duration:**
• 5.5 years (4.5 years + 1 year internship)

Want NEET preparation guidance?"""
            
            else:
                return """🎓 **College Information**

I can help with:

**Engineering Colleges** 🏗️
• IIT, NIT, Government colleges
→ Ask: "Engineering colleges in Kerala"

**Medical Colleges** 🏥
• MBBS, BDS colleges
→ Ask: "Medical colleges in Kerala"

**Arts & Science** 📚
• BA, B.Sc, B.Com programs

**Management** 💼
• MBA, BBA colleges

Which field are you interested in?"""
        
        # CONFUSED
        elif intent == 'confused':
            return """Don't worry! Feeling confused is totally normal! 🤗

**Step-by-step approach:**

**🔍 Step 1: Self-Assessment**
• What subjects do you enjoy?
• What activities make you happy?
• What are your strengths?

**📋 Step 2: Take Career Quiz**
• 10-minute personality test
• Get matched with careers
• Free and personalized!
→ Go to /quiz

**💼 Step 3: Explore Options**
• Browse different careers
• Read about professions

**👨‍💼 Step 4: Expert Guidance**
• Book counsellor session
• Get personalized advice
→ Go to /counsellors

**Right now:**
Tell me your interests!

Examples:
• "I like programming"
• "I enjoy science"
• "I'm creative"

What do you enjoy doing?"""
        
        # SALARY
        elif intent == 'salary':
            return """💰 **Salary Information by Career**

**💻 Technology/IT:**
• Software Engineer: ₹3-15 lakhs → ₹50+ lakhs
• Data Scientist: ₹5-20 lakhs → ₹80+ lakhs

**⚕️ Medical:**
• Doctor (MBBS): ₹6-20 lakhs → ₹80+ lakhs
• Specialist: ₹50 lakhs - 2 crore

**⚙️ Engineering:**
• Computer Science: ₹4-15 lakhs → ₹50+ lakhs
• Mechanical: ₹3-8 lakhs → ₹30+ lakhs
• Civil: ₹3-7 lakhs → ₹25+ lakhs

**💼 Business:**
• MBA (IIM): ₹15-50+ lakhs
• CA: ₹6-15 lakhs → ₹80+ lakhs

**📊 Factors Affecting Salary:**
• Company (MNCs pay 30-50% more)
• Location (metros pay higher)
• Skills and certifications
• Experience

Which field's salary details do you want?"""
        
        # GOODBYE
        elif intent == 'goodbye':
            return """Goodbye! 👋

Thank you for chatting! Remember:
• I'm available 24/7
• Come back anytime for guidance
• Take the career quiz!

Best wishes for your future! ✨"""
        
        # GENERAL/DEFAULT
        else:
            return """I'm your AI Career Counsellor! 🎯

**What I can help with:**

**Career Guidance** 💼
• Discover matching careers
• Salary information

**College Info** 🏛️
• Find colleges in Kerala
• Admission details

**Course Selection** 📚
• After 10th/12th options
• Entrance exams

**Try asking:**
• "What career suits me?"
• "Engineering colleges in Kerala"
• "I like programming"
• "What after 12th science?"
• "How much do engineers earn?"

**Quick Actions:**
📋 Take Career Quiz → /quiz
💼 Browse Careers → /careers
🏛️ Find Colleges → /colleges
👨‍💼 Book Counsellor → /counsellors

How can I help you? 😊"""
    
    def _get_quick_replies(self, intent: str) -> List[str]:
        """Generate quick reply suggestions"""
        
        suggestions = {
            'greeting': [
                "What career suits me?",
                "I like programming",
                "Engineering colleges",
                "Take career quiz"
            ],
            'careers': [
                "Technology careers",
                "Medical field",
                "Engineering options",
                "Business careers"
            ],
            'education': [
                "Engineering colleges",
                "Medical colleges",
                "Admission process",
                "Course options"
            ],
            'confused': [
                "Tell me about careers",
                "I like technology",
                "Take career quiz",
                "Book counsellor"
            ]
        }
        
        return suggestions.get(intent, [
            "What career suits me?",
            "Find colleges",
            "Take quiz",
            "I need help"
        ])


# Singleton instance
chatbot_instance = CareerChatbot()


def get_chatbot_response(message: str, user_profile: Optional[Dict] = None) -> Dict:
    """
    Main function to get chatbot response
    """
    try:
        return chatbot_instance.generate_response(message, user_profile)
    except Exception as e:
        print(f"Chatbot error: {e}")
        return {
            'response': "I'm here to help! Ask me about careers, colleges, or courses.",
            'intent': 'error',
            'suggestions': ['Career advice', 'Find colleges', 'Courses']
        }