"""
NLP Chatbot Module for Career Counselling
Uses pattern matching and keyword detection for intent classification
No heavy ML libraries needed - lightweight and fast!
"""

import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class CareerChatbot:
    """
    Intelligent chatbot for career counselling using NLP techniques
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
                r'\b(interest|like|enjoy|love|passionate|hobby|hobbies)\b',
                r'\bwhat\s+do\s+i\s+like\b',
            ],
            'skills': [
                r'\b(skill|talent|good\s+at|strength|ability|abilities)\b',
            ],
            'careers': [
                r'\b(career|job|profession|occupation|work|field)\b',
                r'\bwhat\s+(should|can)\s+i\s+(be|do|become)\b',
            ],
            'education': [
                r'\b(college|university|course|degree|study|education|school)\b',
            ],
            'quiz': [
                r'\b(test|quiz|assessment|aptitude|personality)\b',
            ],
            'counsellor': [
                r'\b(counsellor|counselor|expert|advisor|mentor|guide)\b',
                r'\bbook\s+(appointment|session)\b',
            ],
            'help': [
                r'\b(help|assist|support|guide|confused|lost)\b',
            ],
            'current_education': [
                r'\b(10th|12th|undergraduate|graduate|diploma|studying)\b',
            ],
            'stream': [
                r'\b(science|commerce|arts|engineering|medical|humanities)\b',
            ],
        }
        
        # Interest keywords
        self.interest_keywords = {
            'technology': ['computer', 'programming', 'coding', 'software', 'tech', 'ai', 'ml', 'app', 'website'],
            'science': ['physics', 'chemistry', 'biology', 'science', 'research', 'experiment', 'lab'],
            'mathematics': ['math', 'mathematics', 'numbers', 'calculation', 'algebra', 'geometry'],
            'arts': ['art', 'drawing', 'painting', 'creative', 'design', 'music', 'dance'],
            'business': ['business', 'management', 'marketing', 'sales', 'entrepreneur'],
            'healthcare': ['medicine', 'doctor', 'health', 'hospital', 'patient', 'medical'],
            'teaching': ['teaching', 'education', 'teacher', 'professor', 'training'],
            'sports': ['sports', 'fitness', 'athlete', 'exercise', 'physical'],
            'writing': ['writing', 'author', 'journalism', 'content', 'blog'],
        }
        
        # Skill keywords
        self.skill_keywords = {
            'analytical': ['analysis', 'analytical', 'data', 'research', 'investigate'],
            'creative': ['creative', 'imagination', 'innovative', 'artistic', 'design'],
            'communication': ['communication', 'speaking', 'presentation', 'writing'],
            'leadership': ['leadership', 'management', 'team', 'organize', 'coordinate'],
            'technical': ['technical', 'programming', 'engineering', 'building'],
            'problem-solving': ['problem', 'solve', 'solution', 'fix', 'debug'],
        }
    
    def preprocess_text(self, text: str) -> str:
        """Clean and normalize text"""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', ' ', text)  # Remove punctuation
        text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
        return text
    
    def detect_intent(self, text: str) -> str:
        """Detect user intent from text"""
        text = self.preprocess_text(text)
        
        # Check each intent pattern
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
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from user message"""
        text = self.preprocess_text(text)
        skills = []
        
        for skill, keywords in self.skill_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    skills.append(skill)
                    break
        
        return list(set(skills))
    
    def generate_response(self, user_message: str, user_profile: Optional[Dict] = None) -> Dict:
        """
        Generate intelligent response based on user message and context
        
        Args:
            user_message: User's message
            user_profile: User's profile data (interests, skills, education)
        
        Returns:
            Dict with response, intent, and extracted info
        """
        # Detect intent
        intent = self.detect_intent(user_message)
        
        # Extract interests and skills
        interests = self.extract_interests(user_message)
        skills = self.extract_skills(user_message)
        
        # Update context
        if interests:
            self.context['detected_interests'] = interests
        if skills:
            self.context['detected_skills'] = skills
        
        # Generate response based on intent
        response = self._generate_intent_response(intent, user_message, user_profile)
        
        # Add to conversation history
        self.conversation_history.append({
            'user_message': user_message,
            'bot_response': response,
            'intent': intent,
            'interests': interests,
            'skills': skills,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        return {
            'response': response,
            'intent': intent,
            'detected_interests': interests,
            'detected_skills': skills,
            'suggestions': self._get_quick_replies(intent)
        }
    
    def _generate_intent_response(self, intent: str, message: str, user_profile: Optional[Dict]) -> str:
        """Generate response based on detected intent"""
        
        responses = {
            'greeting': [
                "Hello! I'm your AI Career Counselor. I'm here to help you discover your perfect career path. What would you like to explore today?",
                "Hi there! Welcome to your career guidance journey. How can I assist you in finding your ideal career?",
                "Hey! Great to see you. Let's work together to find the career that's perfect for you. Where should we start?"
            ],
            
            'goodbye': [
                "Goodbye! Feel free to come back anytime you need career guidance. Best of luck with your journey!",
                "Take care! Remember, I'm always here to help with your career questions.",
                "See you later! Don't hesitate to reach out when you need more guidance."
            ],
            
            'interests': [
                "Understanding your interests is crucial for finding the right career! Tell me more about what you're passionate about. For example:\n\n"
                "• What subjects do you enjoy in school?\n"
                "• What do you do in your free time?\n"
                "• What topics make you excited to learn more?\n\n"
                "Share as much as you'd like, and I'll help match you with suitable careers!",
                
                "Great question about interests! Your passions are key indicators of career satisfaction. "
                "Are you drawn to technology, sciences, arts, business, or helping people? "
                "Or maybe a combination? Tell me what makes you feel energized!"
            ],
            
            'skills': [
                "Skills are your superpowers! Let's identify what you're naturally good at. Consider these areas:\n\n"
                "• Analytical thinking (solving problems, working with data)\n"
                "• Creative thinking (designing, innovating, imagining)\n"
                "• Communication (speaking, writing, presenting)\n"
                "• Leadership (organizing, coordinating, managing)\n"
                "• Technical abilities (building, programming, engineering)\n\n"
                "Which of these resonate with you?",
                
                "Excellent! Knowing your skills helps us find careers where you'll excel. "
                "Think about tasks that come naturally to you or that you perform better than others. "
                "What would you say is your strongest skill?"
            ],
            
            'careers': [
                "I'd love to help you explore career options! To give you the most relevant suggestions, "
                "I need to understand you better. Have you:\n\n"
                "1. Taken our aptitude test? (Helps identify your strengths)\n"
                "2. Completed the personality assessment? (Matches your work style)\n"
                "3. Shared your interests with me?\n\n"
                "The more I know about you, the better recommendations I can provide!",
                
                "Finding the right career is exciting! Based on what you've told me so far, "
                "I can suggest some career paths. But first, could you tell me:\n\n"
                "• What's your current education level?\n"
                "• What subjects do you enjoy most?\n"
                "• Do you prefer working with people, data, things, or ideas?"
            ],
            
            'education': [
                "Education is a crucial step in your career journey! Let me help you find the right path. "
                "Could you tell me:\n\n"
                "• What level are you at? (10th, 12th, Undergraduate, etc.)\n"
                "• What stream interests you? (Science, Commerce, Arts)\n"
                "• Any specific courses you're considering?\n\n"
                "I can suggest the best colleges and courses for your career goals!",
                
                "Great that you're thinking about education! Your choice of course can significantly impact your career. "
                "What's your preferred field of study? I can recommend courses and colleges that align with your interests."
            ],
            
            'quiz': [
                "Our assessments are designed to help you understand yourself better! We offer:\n\n"
                "📝 Aptitude Test: Measures your abilities in different areas\n"
                "🧠 Personality Assessment: Identifies your work style and preferences\n\n"
                "Both tests take about 15-20 minutes each. Would you like to start with the aptitude test or personality assessment?",
                
                "Taking our assessments is highly recommended! They provide valuable insights that help us give you "
                "personalized career recommendations. The results will show your strengths and ideal work environments. "
                "Ready to begin?"
            ],
            
            'counsellor': [
                "Connecting with a professional counsellor is a great idea! Our expert counsellors can provide:\n\n"
                "• One-on-one guidance sessions\n"
                "• In-depth career planning\n"
                "• Industry insights\n"
                "• Education pathway advice\n\n"
                "You can browse available counsellors and book a session that fits your schedule. "
                "Would you like to see available counsellors?",
                
                "Our certified career counsellors are here to help! They bring years of experience in career guidance. "
                "Sessions are available via video call or phone. To book an appointment, "
                "head to the 'Book Counsellor' section. Any specific area you'd like to discuss with them?"
            ],
            
            'help': [
                "I'm here to help you every step of the way! Here's what I can assist you with:\n\n"
                "🎯 Career Exploration: Discover careers that match your profile\n"
                "📊 Assessments: Take aptitude and personality tests\n"
                "🎓 Education: Find courses and colleges\n"
                "💬 Counselling: Book sessions with experts\n"
                "📝 Profile Building: Complete your career profile\n\n"
                "What would you like to start with?",
                
                "No worries, I'm here to guide you! Career planning can feel overwhelming, but we'll break it down into simple steps. "
                "Let's start with understanding your interests. What subjects or activities do you enjoy?"
            ],
            
            'general': [
                "I'm here to help you with your career planning! I can assist you with:\n\n"
                "• Discovering careers that match your interests and skills\n"
                "• Suggesting courses and colleges\n"
                "• Providing information about different professions\n"
                "• Helping you prepare for career decisions\n\n"
                "What specific aspect would you like to explore?",
                
                "Thanks for reaching out! To provide you with the best guidance, could you tell me more about "
                "what you're looking for? Are you interested in exploring career options, understanding required courses, "
                "or learning about specific professions?"
            ]
        }
        
        # Get appropriate response
        import random
        response_list = responses.get(intent, responses['general'])
        response = random.choice(response_list)
        
        # Personalize with detected interests/skills
        if self.context.get('detected_interests'):
            response += f"\n\n💡 I noticed you mentioned interest in: {', '.join(self.context['detected_interests'])}. That's great!"
        
        if self.context.get('detected_skills'):
            response += f"\n\n⭐ I see you have skills in: {', '.join(self.context['detected_skills'])}. These are valuable!"
        
        return response
    
    def _get_quick_replies(self, intent: str) -> List[str]:
        """Generate quick reply suggestions based on intent"""
        
        suggestions = {
            'greeting': [
                "Tell me about your interests",
                "What are my skills?",
                "Suggest careers for me",
                "I want to take a quiz"
            ],
            'interests': [
                "I like technology",
                "I enjoy science",
                "I'm creative and artistic",
                "I want to help people"
            ],
            'skills': [
                "I'm good at problem-solving",
                "I'm a creative person",
                "I have leadership skills",
                "I'm analytical"
            ],
            'careers': [
                "Suggest careers for me",
                "Tell me about engineering",
                "What about medical field?",
                "I need to take assessments"
            ],
            'education': [
                "I'm in 12th grade",
                "Show me engineering courses",
                "Suggest good colleges",
                "What stream should I choose?"
            ],
            'quiz': [
                "Start aptitude test",
                "Take personality test",
                "Tell me about assessments",
                "Skip to recommendations"
            ],
            'help': [
                "How does this work?",
                "What should I do first?",
                "Tell me about careers",
                "Book a counsellor"
            ]
        }
        
        return suggestions.get(intent, [
            "Tell me about your interests",
            "What careers suit me?",
            "I need help",
            "Book a counsellor"
        ])
    
    def get_conversation_summary(self) -> Dict:
        """Get summary of conversation for analysis"""
        all_interests = []
        all_skills = []
        
        for entry in self.conversation_history:
            all_interests.extend(entry.get('interests', []))
            all_skills.extend(entry.get('skills', []))
        
        return {
            'total_messages': len(self.conversation_history),
            'detected_interests': list(set(all_interests)),
            'detected_skills': list(set(all_skills)),
            'conversation_history': self.conversation_history
        }


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