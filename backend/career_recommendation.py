"""
Career Recommendation Engine
Matches users with suitable careers based on interests, skills, and personality
"""

from typing import Dict, List, Tuple
import math


class CareerRecommendationEngine:
    """
    Intelligent career recommendation system
    """
    
    def __init__(self):
        # Career database with detailed matching criteria
        self.career_database = {
            'Software Engineer': {
                'interests': ['technology', 'mathematics', 'problem-solving'],
                'skills': ['analytical', 'technical', 'problem-solving', 'creative'],
                'personality': {
                    'introverted': 0.6,
                    'analytical': 0.9,
                    'creative': 0.7,
                    'detail-oriented': 0.8,
                    'independent': 0.7
                },
                'education': ['B.Tech Computer Science', 'B.Sc Computer Science', 'BCA'],
                'work_environment': 'office/remote',
                'salary_range': '₹4-25 LPA',
                'growth_prospects': 'excellent',
                'description': 'Design, develop, and maintain software applications'
            },
            
            'Data Scientist': {
                'interests': ['mathematics', 'technology', 'analysis'],
                'skills': ['analytical', 'technical', 'problem-solving'],
                'personality': {
                    'introverted': 0.5,
                    'analytical': 1.0,
                    'creative': 0.6,
                    'detail-oriented': 0.9,
                    'independent': 0.8
                },
                'education': ['B.Tech', 'B.Sc Statistics', 'B.Sc Mathematics'],
                'work_environment': 'office/remote',
                'salary_range': '₹6-30 LPA',
                'growth_prospects': 'excellent'
            },
            
            'Doctor': {
                'interests': ['healthcare', 'science', 'helping-people'],
                'skills': ['analytical', 'communication', 'problem-solving'],
                'personality': {
                    'extroverted': 0.7,
                    'empathetic': 1.0,
                    'analytical': 0.8,
                    'detail-oriented': 0.9,
                    'patient': 0.9
                },
                'education': ['MBBS', 'MD', 'MS'],
                'work_environment': 'hospital/clinic',
                'salary_range': '₹6-50 LPA',
                'growth_prospects': 'very good'
            },
            
            'Teacher': {
                'interests': ['teaching', 'helping-people', 'knowledge-sharing'],
                'skills': ['communication', 'leadership', 'patience'],
                'personality': {
                    'extroverted': 0.8,
                    'empathetic': 0.9,
                    'patient': 1.0,
                    'organized': 0.7,
                    'creative': 0.6
                },
                'education': ['B.Ed', 'M.Ed', 'B.A/B.Sc + B.Ed'],
                'work_environment': 'school/college',
                'salary_range': '₹3-8 LPA',
                'growth_prospects': 'good'
            },
            
            'Graphic Designer': {
                'interests': ['arts', 'creative', 'design'],
                'skills': ['creative', 'technical', 'visual-thinking'],
                'personality': {
                    'creative': 1.0,
                    'artistic': 0.9,
                    'detail-oriented': 0.7,
                    'independent': 0.7,
                    'innovative': 0.8
                },
                'education': ['B.Des', 'B.F.A', 'Diploma in Design'],
                'work_environment': 'office/remote/freelance',
                'salary_range': '₹3-15 LPA',
                'growth_prospects': 'good'
            },
            
            'Business Analyst': {
                'interests': ['business', 'analysis', 'problem-solving'],
                'skills': ['analytical', 'communication', 'problem-solving'],
                'personality': {
                    'analytical': 0.9,
                    'logical': 0.8,
                    'communication': 0.8,
                    'detail-oriented': 0.7,
                    'strategic': 0.8
                },
                'education': ['MBA', 'BBA', 'B.Tech'],
                'work_environment': 'office',
                'salary_range': '₹5-20 LPA',
                'growth_prospects': 'excellent'
            },
            
            'Civil Engineer': {
                'interests': ['engineering', 'building', 'problem-solving'],
                'skills': ['technical', 'analytical', 'problem-solving'],
                'personality': {
                    'practical': 0.9,
                    'analytical': 0.7,
                    'detail-oriented': 0.8,
                    'systematic': 0.8,
                    'outdoor': 0.6
                },
                'education': ['B.Tech Civil Engineering', 'Diploma in Civil'],
                'work_environment': 'field/office',
                'salary_range': '₹3-15 LPA',
                'growth_prospects': 'good'
            },
            
            'Content Writer': {
                'interests': ['writing', 'creative', 'communication'],
                'skills': ['creative', 'communication', 'research'],
                'personality': {
                    'creative': 0.9,
                    'introverted': 0.6,
                    'imaginative': 0.8,
                    'detail-oriented': 0.7,
                    'independent': 0.8
                },
                'education': ['B.A English', 'B.A Journalism', 'Any Graduate'],
                'work_environment': 'remote/office',
                'salary_range': '₹2-10 LPA',
                'growth_prospects': 'good'
            },
            
            'Chartered Accountant': {
                'interests': ['finance', 'numbers', 'analysis'],
                'skills': ['analytical', 'detail-oriented', 'systematic'],
                'personality': {
                    'analytical': 0.9,
                    'detail-oriented': 1.0,
                    'systematic': 0.9,
                    'patient': 0.7,
                    'precise': 0.9
                },
                'education': ['CA', 'B.Com + CA'],
                'work_environment': 'office',
                'salary_range': '₹6-30 LPA',
                'growth_prospects': 'excellent'
            },
            
            'Psychologist': {
                'interests': ['psychology', 'helping-people', 'human-behavior'],
                'skills': ['communication', 'empathy', 'analytical'],
                'personality': {
                    'empathetic': 1.0,
                    'patient': 0.9,
                    'analytical': 0.7,
                    'good-listener': 0.9,
                    'compassionate': 0.9
                },
                'education': ['B.A Psychology', 'M.A Psychology'],
                'work_environment': 'clinic/hospital/school',
                'salary_range': '₹3-12 LPA',
                'growth_prospects': 'good'
            }
        }
    
    def calculate_interest_match(self, user_interests: List[str], career: Dict) -> float:
        """Calculate match score based on interests"""
        if not user_interests:
            return 0.0
        
        career_interests = career['interests']
        matches = len(set(user_interests) & set(career_interests))
        max_possible = len(career_interests)
        
        return (matches / max_possible) if max_possible > 0 else 0.0
    
    def calculate_skill_match(self, user_skills: List[str], career: Dict) -> float:
        """Calculate match score based on skills"""
        if not user_skills:
            return 0.0
        
        career_skills = career['skills']
        matches = len(set(user_skills) & set(career_skills))
        max_possible = len(career_skills)
        
        return (matches / max_possible) if max_possible > 0 else 0.0
    
    def calculate_personality_match(self, user_personality: Dict, career: Dict) -> float:
        """Calculate match score based on personality traits"""
        if not user_personality:
            return 0.0
        
        career_personality = career['personality']
        
        # Calculate similarity using cosine similarity
        common_traits = set(user_personality.keys()) & set(career_personality.keys())
        
        if not common_traits:
            return 0.0
        
        dot_product = sum(
            user_personality[trait] * career_personality[trait]
            for trait in common_traits
        )
        
        user_magnitude = math.sqrt(sum(v**2 for v in user_personality.values()))
        career_magnitude = math.sqrt(sum(v**2 for v in career_personality.values()))
        
        if user_magnitude == 0 or career_magnitude == 0:
            return 0.0
        
        return dot_product / (user_magnitude * career_magnitude)
    
    def get_recommendations(
        self,
        user_interests: List[str] = None,
        user_skills: List[str] = None,
        user_personality: Dict = None,
        top_n: int = 5
    ) -> List[Dict]:
        """
        Get top N career recommendations for user
        
        Args:
            user_interests: List of user interests
            user_skills: List of user skills
            user_personality: Dict of personality traits with scores (0-1)
            top_n: Number of recommendations to return
        
        Returns:
            List of career recommendations with match scores
        """
        recommendations = []
        
        for career_name, career_data in self.career_database.items():
            # Calculate individual scores
            interest_score = self.calculate_interest_match(
                user_interests or [], career_data
            )
            skill_score = self.calculate_skill_match(
                user_skills or [], career_data
            )
            personality_score = self.calculate_personality_match(
                user_personality or {}, career_data
            )
            
            # Weighted final score
            weights = {
                'interests': 0.4,
                'skills': 0.35,
                'personality': 0.25
            }
            
            final_score = (
                interest_score * weights['interests'] +
                skill_score * weights['skills'] +
                personality_score * weights['personality']
            )
            
            # Generate reasons
            reasons = []
            if interest_score > 0.5:
                matched_interests = set(user_interests or []) & set(career_data['interests'])
                reasons.append(f"Matches your interests in {', '.join(matched_interests)}")
            
            if skill_score > 0.5:
                matched_skills = set(user_skills or []) & set(career_data['skills'])
                reasons.append(f"Aligns with your {', '.join(matched_skills)} skills")
            
            if personality_score > 0.5:
                reasons.append("Good personality fit for this role")
            
            if not reasons:
                reasons.append("Based on your overall profile")
            
            recommendations.append({
                'career_name': career_name,
                'match_score': round(final_score * 100, 2),
                'interest_score': round(interest_score * 100, 2),
                'skill_score': round(skill_score * 100, 2),
                'personality_score': round(personality_score * 100, 2),
                'reasons': reasons,
                'education': career_data['education'],
                'salary_range': career_data['salary_range'],
                'growth_prospects': career_data['growth_prospects'],
                'work_environment': career_data['work_environment'],
                'description': career_data.get('description', '')
            })
        
        # Sort by match score
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        
        return recommendations[:top_n]
    
    def get_career_details(self, career_name: str) -> Dict:
        """Get detailed information about a specific career"""
        if career_name not in self.career_database:
            return None
        
        return self.career_database[career_name]
    
    def analyze_quiz_results(self, quiz_results: Dict) -> Dict:
        """
        Analyze quiz results and extract user profile
        
        Args:
            quiz_results: Dict with quiz type and responses
        
        Returns:
            User profile dict with interests, skills, personality
        """
        profile = {
            'interests': [],
            'skills': [],
            'personality': {}
        }
        
        if quiz_results.get('quiz_type') == 'aptitude':
            # Extract skills from aptitude test
            score = quiz_results.get('score', 0)
            total = quiz_results.get('total_questions', 20)
            
            if score / total > 0.7:
                profile['skills'].extend(['analytical', 'problem-solving'])
            
        elif quiz_results.get('quiz_type') == 'personality':
            # Extract personality traits
            personality_traits = quiz_results.get('personality_traits', {})
            
            # Normalize scores to 0-1 scale
            max_score = max(personality_traits.values()) if personality_traits else 1
            profile['personality'] = {
                trait: score / max_score
                for trait, score in personality_traits.items()
            }
        
        return profile


# Singleton instance
recommendation_engine = CareerRecommendationEngine()


def get_career_recommendations(
    interests: List[str] = None,
    skills: List[str] = None,
    personality: Dict = None,
    top_n: int = 5
) -> List[Dict]:
    """
    Main function to get career recommendations
    
    Usage:
        recommendations = get_career_recommendations(
            interests=['technology', 'problem-solving'],
            skills=['analytical', 'technical'],
            personality={'introverted': 0.7, 'analytical': 0.9},
            top_n=5
        )
        
        for rec in recommendations:
            print(f"{rec['career_name']}: {rec['match_score']}%")
            print(f"Reasons: {', '.join(rec['reasons'])}")
    """
    return recommendation_engine.get_recommendations(interests, skills, personality, top_n)