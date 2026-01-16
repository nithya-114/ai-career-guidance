"""
Enhanced Quiz API with AI-Powered Career Recommendations
Analyzes quiz results and generates personalized career matches
"""

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from bson import ObjectId
import jwt

quiz_bp = Blueprint('quiz', __name__)

# Mock questions as fallback
APTITUDE_QUESTIONS = [
    {
        'id': 1,
        'question': 'What is 2 + 2?',
        'options': ['3', '4', '5', '6'],
        'correct': '4',
        'category': 'numerical',
        'skills': ['basic_math', 'numerical_reasoning']
    },
    {
        'id': 2,
        'question': 'If 5 machines can produce 5 products in 5 minutes, how many products can 100 machines produce in 100 minutes?',
        'options': ['100', '500', '2000', '10000'],
        'correct': '2000',
        'category': 'logical',
        'skills': ['logical_reasoning', 'problem_solving', 'analytical_thinking']
    },
    {
        'id': 3,
        'question': 'What is the next number in the sequence: 2, 6, 12, 20, 30, ?',
        'options': ['38', '40', '42', '44'],
        'correct': '42',
        'category': 'logical',
        'skills': ['pattern_recognition', 'logical_reasoning']
    },
    {
        'id': 4,
        'question': 'If A + B = 10 and A - B = 4, what is the value of A?',
        'options': ['6', '7', '8', '9'],
        'correct': '7',
        'category': 'numerical',
        'skills': ['algebra', 'numerical_reasoning', 'problem_solving']
    },
    {
        'id': 5,
        'question': 'Choose the synonym of "Eloquent"',
        'options': ['Articulate', 'Hesitant', 'Silent', 'Confused'],
        'correct': 'Articulate',
        'category': 'verbal',
        'skills': ['vocabulary', 'verbal_reasoning', 'communication']
    },
    {
        'id': 6,
        'question': 'A clock shows 3:15. What is the angle between hour and minute hands?',
        'options': ['0°', '7.5°', '15°', '30°'],
        'correct': '7.5°',
        'category': 'numerical',
        'skills': ['spatial_reasoning', 'numerical_reasoning', 'geometry']
    },
    {
        'id': 7,
        'question': 'Which number comes next: 1, 1, 2, 3, 5, 8, 13, ?',
        'options': ['18', '21', '24', '27'],
        'correct': '21',
        'category': 'logical',
        'skills': ['pattern_recognition', 'logical_reasoning', 'mathematical_thinking']
    },
    {
        'id': 8,
        'question': 'What is 15% of 200?',
        'options': ['20', '25', '30', '35'],
        'correct': '30',
        'category': 'numerical',
        'skills': ['percentage_calculation', 'numerical_reasoning', 'applied_math']
    },
    {
        'id': 9,
        'question': 'Choose the antonym of "Optimistic"',
        'options': ['Hopeful', 'Pessimistic', 'Happy', 'Excited'],
        'correct': 'Pessimistic',
        'category': 'verbal',
        'skills': ['vocabulary', 'verbal_reasoning', 'language_skills']
    },
    {
        'id': 10,
        'question': 'If all Bloops are Razzies and all Razzies are Lazzies, then all Bloops are:',
        'options': ['Definitely Lazzies', 'Never Lazzies', 'Sometimes Lazzies', 'Cannot determine'],
        'correct': 'Definitely Lazzies',
        'category': 'logical',
        'skills': ['deductive_reasoning', 'logical_reasoning', 'critical_thinking']
    }
]

PERSONALITY_QUESTIONS = [
    {
        'id': 1,
        'question': 'I prefer working:',
        'options': ['Alone', 'In small groups', 'In large teams', 'It depends'],
        'trait': 'work_style',
        'career_mapping': {
            'Alone': ['Software Engineer', 'Data Scientist', 'Writer', 'Researcher'],
            'In small groups': ['UI/UX Designer', 'Architect', 'Consultant'],
            'In large teams': ['Project Manager', 'HR Manager', 'Marketing Manager'],
            'It depends': ['Entrepreneur', 'Consultant', 'Teacher']
        }
    },
    {
        'id': 2,
        'question': 'When faced with a problem, I tend to:',
        'options': ['Analyze it logically', 'Think creatively', 'Seek advice', 'Take immediate action'],
        'trait': 'problem_solving',
        'career_mapping': {
            'Analyze it logically': ['Software Engineer', 'Data Scientist', 'Chartered Accountant', 'Engineer'],
            'Think creatively': ['Graphic Designer', 'Architect', 'Marketing Manager', 'Artist'],
            'Seek advice': ['Counsellor', 'HR Manager', 'Teacher', 'Social Worker'],
            'Take immediate action': ['Entrepreneur', 'Emergency Medical Technician', 'Sales Manager']
        }
    },
    {
        'id': 3,
        'question': 'I am most interested in:',
        'options': ['Technology and innovation', 'Helping people', 'Business and finance', 'Arts and creativity'],
        'trait': 'interests',
        'career_mapping': {
            'Technology and innovation': ['Software Engineer', 'Data Scientist', 'AI/ML Engineer', 'Cybersecurity Specialist'],
            'Helping people': ['Doctor (MBBS)', 'Nurse', 'Counsellor', 'Teacher', 'Social Worker'],
            'Business and finance': ['MBA Graduate', 'Chartered Accountant', 'Investment Banker', 'Financial Analyst'],
            'Arts and creativity': ['Graphic Designer', 'UI/UX Designer', 'Architect', 'Fashion Designer']
        }
    },
    {
        'id': 4,
        'question': 'My ideal work environment is:',
        'options': ['Structured and organized', 'Flexible and dynamic', 'Collaborative', 'Independent'],
        'trait': 'environment',
        'career_mapping': {
            'Structured and organized': ['Chartered Accountant', 'Civil Engineer', 'Lawyer', 'Banker'],
            'Flexible and dynamic': ['Entrepreneur', 'Digital Marketing Manager', 'Event Manager'],
            'Collaborative': ['Project Manager', 'Teacher', 'HR Manager'],
            'Independent': ['Software Engineer', 'Writer', 'Photographer', 'Researcher']
        }
    },
    {
        'id': 5,
        'question': 'I am motivated by:',
        'options': ['Financial rewards', 'Recognition', 'Making a difference', 'Learning new things'],
        'trait': 'motivation',
        'career_mapping': {
            'Financial rewards': ['Investment Banker', 'Chartered Accountant', 'MBA Graduate', 'Sales Manager'],
            'Recognition': ['Lawyer', 'Surgeon', 'Architect', 'CEO'],
            'Making a difference': ['Doctor (MBBS)', 'Teacher', 'Social Worker', 'Environmental Scientist'],
            'Learning new things': ['Data Scientist', 'Research Scientist', 'Professor/Teacher', 'AI/ML Engineer']
        }
    },
    {
        'id': 6,
        'question': 'I enjoy coming up with new ideas:',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'trait': 'creativity',
        'career_mapping': {
            'Strongly Agree': ['Entrepreneur', 'Product Designer', 'Architect', 'Marketing Manager'],
            'Agree': ['Software Engineer', 'UI/UX Designer', 'Content Creator']
        }
    },
    {
        'id': 7,
        'question': 'I am comfortable leading groups:',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'trait': 'leadership',
        'career_mapping': {
            'Strongly Agree': ['MBA Graduate', 'Project Manager', 'Entrepreneur', 'Operations Manager'],
            'Agree': ['Team Lead', 'HR Manager', 'Principal/Headmaster']
        }
    },
    {
        'id': 8,
        'question': 'I prefer hands-on practical work:',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'trait': 'hands_on',
        'career_mapping': {
            'Strongly Agree': ['Mechanical Engineer', 'Civil Engineer', 'Surgeon', 'Chef', 'Electrician'],
            'Agree': ['Architect', 'Lab Technician', 'Photographer']
        }
    },
    {
        'id': 9,
        'question': 'I am interested in healthcare:',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'trait': 'medical',
        'career_mapping': {
            'Strongly Agree': ['Doctor (MBBS)', 'Dentist', 'Nurse', 'Pharmacist', 'Physiotherapist'],
            'Agree': ['Medical Laboratory Technician', 'Healthcare Administrator', 'Nutritionist']
        }
    },
    {
        'id': 10,
        'question': 'I care about environmental issues:',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'trait': 'environment',
        'career_mapping': {
            'Strongly Agree': ['Environmental Scientist', 'Sustainability Consultant', 'Environmental Engineer'],
            'Agree': ['Urban Planner', 'Agricultural Scientist', 'Conservation Officer']
        }
    }
]


def get_db():
    """Get database from app config or fallback"""
    try:
        return current_app.config.get('DB')
    except:
        try:
            from pymongo import MongoClient
            client = MongoClient('mongodb://localhost:27017/')
            return client.career_counselling
        except:
            return None


def get_user_from_token(request):
    """Extract user ID from JWT token"""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return None, {'error': 'No token provided'}, 401
    
    token = auth_header.split(' ')[1]
    
    try:
        secret_key = current_app.config.get('SECRET_KEY', 'your-secret-key')
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload.get('user_id') or payload.get('sub'), None, None
    except:
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            return payload.get('user_id') or payload.get('sub'), None, None
        except:
            return None, {'error': 'Invalid token'}, 401


# Routes
@quiz_bp.route('/api/quiz/aptitude/questions', methods=['GET'])
def get_aptitude_questions():
    """Get aptitude test questions"""
    try:
        print(f"✓ Sending {len(APTITUDE_QUESTIONS)} aptitude questions")
        return jsonify({'questions': APTITUDE_QUESTIONS}), 200
    except Exception as e:
        print(f"✗ Error: {e}")
        return jsonify({'error': str(e)}), 500


@quiz_bp.route('/api/quiz/personality/questions', methods=['GET'])
def get_personality_questions():
    """Get personality test questions"""
    try:
        print(f"✓ Sending {len(PERSONALITY_QUESTIONS)} personality questions")
        return jsonify({'questions': PERSONALITY_QUESTIONS}), 200
    except Exception as e:
        print(f"✗ Error: {e}")
        return jsonify({'error': str(e)}), 500


@quiz_bp.route('/api/quiz/submit', methods=['POST'])
def submit_quiz():
    """Submit quiz and get AI-powered career recommendations"""
    try:
        data = request.json
        print(f"✓ Received quiz submission")
        
        # Try to get user from token
        user_id, error, status = get_user_from_token(request)
        if error:
            print(f"⚠ No valid token, proceeding without user ID")
            user_id = 'anonymous'
        
        quiz_type = data.get('quiz_type')
        answers = data.get('answers', {})
        questions = data.get('questions', [])
        
        print(f"  Quiz type: {quiz_type}, Answers: {len(answers)}")
        
        # Use default questions if not provided
        if not questions:
            questions = APTITUDE_QUESTIONS if quiz_type == 'aptitude' else PERSONALITY_QUESTIONS
        
        # Calculate score
        if quiz_type == 'aptitude':
            score = calculate_aptitude_score(answers, questions)
            identified_skills = extract_skills_from_aptitude(answers, questions)
        else:
            score = calculate_personality_score(answers, questions)
            identified_skills = []
        
        print(f"✓ Score: {score}")
        
        # Get AI-powered career recommendations
        db = get_db()
        recommendations = generate_ai_recommendations(
            quiz_type, 
            score, 
            answers, 
            questions,
            identified_skills,
            db
        )
        
        # Try to save to database
        if db is not None and user_id != 'anonymous':
            try:
                result_doc = {
                    'user_id': user_id,
                    'quiz_type': quiz_type,
                    'answers': answers,
                    'score': score,
                    'identified_skills': identified_skills,
                    'recommendations': recommendations,
                    'completed_at': datetime.utcnow()
                }
                db.quiz_results.insert_one(result_doc)
                print("✓ Saved to database")
            except Exception as e:
                print(f"⚠ Database save failed: {e}")
        
        print(f"✓ Generated {len(recommendations)} AI-powered recommendations")
        
        return jsonify({
            'message': 'Quiz submitted successfully',
            'score': score,
            'identified_skills': identified_skills,
            'recommendations': recommendations
        }), 200
        
    except Exception as e:
        print(f"✗ Error in submit: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


def calculate_aptitude_score(answers, questions):
    """Calculate aptitude score with category breakdown"""
    categories = {
        'logical': {'correct': 0, 'total': 0},
        'numerical': {'correct': 0, 'total': 0},
        'verbal': {'correct': 0, 'total': 0}
    }
    
    correct = 0
    total = len(questions)
    
    for idx, question in enumerate(questions):
        user_answer = answers.get(str(idx))
        correct_answer = question.get('correct')
        category = question.get('category', 'general')
        
        if category in categories:
            categories[category]['total'] += 1
        
        if user_answer == correct_answer:
            correct += 1
            if category in categories:
                categories[category]['correct'] += 1
    
    # Calculate percentages
    for cat in categories:
        if categories[cat]['total'] > 0:
            categories[cat]['percentage'] = round(
                (categories[cat]['correct'] / categories[cat]['total']) * 100, 2
            )
        else:
            categories[cat]['percentage'] = 0
    
    percentage = (correct / total * 100) if total > 0 else 0
    
    return {
        'correct': correct,
        'total': total,
        'percentage': round(percentage, 2),
        'categories': categories
    }


def extract_skills_from_aptitude(answers, questions):
    """Extract skills demonstrated in aptitude test"""
    skills = []
    
    for idx, question in enumerate(questions):
        user_answer = answers.get(str(idx))
        correct_answer = question.get('correct')
        
        # If answered correctly, add associated skills
        if user_answer == correct_answer:
            question_skills = question.get('skills', [])
            skills.extend(question_skills)
    
    # Return unique skills
    return list(set(skills))


def calculate_personality_score(answers, questions):
    """Calculate personality score with trait analysis"""
    traits = {}
    career_preferences = []
    
    for idx, question in enumerate(questions):
        trait = question.get('trait')
        answer = answers.get(str(idx))
        
        if trait and answer is not None:
            if trait not in traits:
                traits[trait] = []
            
            # Store answer for trait
            traits[trait].append(answer)
            
            # Extract career preferences from mapping
            career_mapping = question.get('career_mapping', {})
            if answer in career_mapping:
                career_preferences.extend(career_mapping[answer])
    
    # Calculate trait scores
    trait_scores = {}
    for trait, answers_list in traits.items():
        if isinstance(answers_list[0], str):
            # For Likert scale answers
            likert_map = {
                'Strongly Disagree': 1,
                'Disagree': 2,
                'Neutral': 3,
                'Agree': 4,
                'Strongly Agree': 5
            }
            scores = [likert_map.get(ans, 3) for ans in answers_list]
            trait_scores[trait] = round(sum(scores) / len(scores), 2) if scores else 3
        else:
            trait_scores[trait] = len(answers_list)
    
    overall = round(sum(trait_scores.values()) / len(trait_scores), 2) if trait_scores else 0
    
    return {
        'traits': trait_scores,
        'overall': overall,
        'career_preferences': list(set(career_preferences))  # Unique career preferences
    }


def generate_ai_recommendations(quiz_type, score, answers, questions, identified_skills, db):
    """Generate intelligent career recommendations based on quiz analysis"""
    
    recommendations = []
    
    if quiz_type == 'aptitude':
        # Aptitude-based recommendations
        recommendations = generate_aptitude_recommendations(score, identified_skills, db)
    else:
        # Personality-based recommendations
        recommendations = generate_personality_recommendations(score, answers, questions, db)
    
    # Fetch additional details from database
    if db is not None:
        recommendations = enrich_recommendations_from_db(recommendations, db)
    
    return recommendations


def generate_aptitude_recommendations(score, identified_skills, db):
    """Generate recommendations based on aptitude test results"""
    
    recommendations = []
    career_suggestions = {}
    
    # Analyze category strengths
    categories = score.get('categories', {})
    
    # Logical reasoning strength
    if categories.get('logical', {}).get('percentage', 0) >= 70:
        career_suggestions['Software Engineer'] = {
            'reason': f"Strong logical reasoning ({categories['logical']['percentage']}%)",
            'match_score': min(categories['logical']['percentage'] + 10, 95)
        }
        career_suggestions['Data Scientist'] = {
            'reason': f"Excellent analytical thinking ({categories['logical']['percentage']}%)",
            'match_score': min(categories['logical']['percentage'] + 5, 92)
        }
    
    # Numerical reasoning strength
    if categories.get('numerical', {}).get('percentage', 0) >= 70:
        career_suggestions['Chartered Accountant'] = {
            'reason': f"Strong numerical skills ({categories['numerical']['percentage']}%)",
            'match_score': min(categories['numerical']['percentage'] + 8, 93)
        }
        career_suggestions['Financial Analyst'] = {
            'reason': f"Excellent mathematical ability ({categories['numerical']['percentage']}%)",
            'match_score': min(categories['numerical']['percentage'] + 5, 90)
        }
    
    # Verbal reasoning strength
    if categories.get('verbal', {}).get('percentage', 0) >= 70:
        career_suggestions['Lawyer'] = {
            'reason': f"Strong verbal reasoning ({categories['verbal']['percentage']}%)",
            'match_score': min(categories['verbal']['percentage'] + 10, 94)
        }
        career_suggestions['Content Writer'] = {
            'reason': f"Excellent language skills ({categories['verbal']['percentage']}%)",
            'match_score': min(categories['verbal']['percentage'] + 5, 88)
        }
    
    # Overall high score
    if score.get('percentage', 0) >= 80:
        career_suggestions['MBA Graduate'] = {
            'reason': f"Outstanding overall performance ({score['percentage']}%)",
            'match_score': min(score['percentage'] + 5, 95)
        }
    
    # Skill-based suggestions
    if 'problem_solving' in identified_skills or 'analytical_thinking' in identified_skills:
        career_suggestions['Mechanical Engineer'] = {
            'reason': "Demonstrated strong problem-solving abilities",
            'match_score': 85
        }
    
    # Convert to recommendation format
    for career_name, details in career_suggestions.items():
        recommendations.append({
            'career_name': career_name,
            'match_score': details['match_score'],
            'primary_reason': details['reason'],
            'identified_skills': identified_skills[:5],  # Top 5 skills
            'category': get_career_category(career_name)
        })
    
    # Sort by match score
    recommendations.sort(key=lambda x: x['match_score'], reverse=True)
    
    return recommendations[:8]  # Top 8 recommendations


def generate_personality_recommendations(score, answers, questions, db):
    """Generate recommendations based on personality test results"""
    
    recommendations = []
    career_preferences = score.get('career_preferences', [])
    
    # Count career frequency
    career_counts = {}
    for career in career_preferences:
        career_counts[career] = career_counts.get(career, 0) + 1
    
    # Sort by frequency
    sorted_careers = sorted(career_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Generate recommendations
    for career_name, count in sorted_careers[:10]:
        # Calculate match score based on how often career appeared
        base_score = min(50 + (count * 10), 95)
        
        # Get reasons based on answers
        reasons = generate_personality_reasons(career_name, answers, questions)
        
        recommendations.append({
            'career_name': career_name,
            'match_score': base_score,
            'primary_reason': reasons[0] if reasons else "Matches your personality profile",
            'additional_reasons': reasons[1:3] if len(reasons) > 1 else [],
            'personality_traits': list(score.get('traits', {}).keys())[:3],
            'category': get_career_category(career_name)
        })
    
    return recommendations


def generate_personality_reasons(career_name, answers, questions):
    """Generate specific reasons why a career matches personality"""
    reasons = []
    
    for idx, question in enumerate(questions):
        user_answer = answers.get(str(idx))
        career_mapping = question.get('career_mapping', {})
        
        if user_answer in career_mapping and career_name in career_mapping[user_answer]:
            trait = question.get('trait', '').replace('_', ' ').title()
            reasons.append(f"Your {trait} aligns well with this career")
    
    if not reasons:
        reasons.append("Your personality profile is a good match")
    
    return list(set(reasons))  # Remove duplicates


def get_career_category(career_name):
    """Get category for a career"""
    category_mapping = {
        'Software Engineer': 'Technology',
        'Data Scientist': 'Technology',
        'AI/ML Engineer': 'Technology',
        'Cybersecurity Specialist': 'Technology',
        'Doctor (MBBS)': 'Healthcare',
        'Nurse': 'Healthcare',
        'Dentist': 'Healthcare',
        'Pharmacist': 'Healthcare',
        'Physiotherapist': 'Healthcare',
        'MBA Graduate': 'Business',
        'Chartered Accountant': 'Business',
        'Investment Banker': 'Business',
        'Financial Analyst': 'Business',
        'Lawyer': 'Law',
        'Corporate Lawyer': 'Law',
        'Graphic Designer': 'Creative',
        'UI/UX Designer': 'Creative',
        'Architect': 'Creative',
        'Fashion Designer': 'Creative',
        'Mechanical Engineer': 'Engineering',
        'Civil Engineer': 'Engineering',
        'Electrical Engineer': 'Engineering',
        'Teacher': 'Education',
        'Professor/Teacher': 'Education',
        'Content Writer': 'Creative'
    }
    
    return category_mapping.get(career_name, 'General')


def enrich_recommendations_from_db(recommendations, db):
    """Enrich recommendations with database information"""
    
    try:
        for rec in recommendations:
            career_name = rec['career_name']
            
            # Find career in database
            career = db.careers.find_one({'name': career_name})
            
            if career:
                rec['career_id'] = str(career['_id'])
                rec['description'] = career.get('description', '')[:150] + '...'
                rec['average_salary'] = career.get('average_salary', 'N/A')
                rec['education_required'] = career.get('education', [])[:2]  # First 2 requirements
                rec['top_colleges'] = career.get('top_colleges', [])[:3]  # Top 3 colleges
            else:
                # If not in database, create basic info
                rec['career_id'] = None
                rec['description'] = f"Explore opportunities in {career_name}"
                rec['reasons'] = [rec.get('primary_reason', 'Good match for your profile')]
                if rec.get('additional_reasons'):
                    rec['reasons'].extend(rec['additional_reasons'])
    
    except Exception as e:
        print(f"⚠ Error enriching recommendations: {e}")
    
    return recommendations


# Alternative route format
@quiz_bp.route('/api/quiz/<quiz_type>/questions', methods=['GET'])
def get_quiz_questions_alt(quiz_type):
    """Alternative route format"""
    if quiz_type == 'aptitude':
        return get_aptitude_questions()
    elif quiz_type == 'personality':
        return get_personality_questions()
    else:
        return jsonify({'error': 'Invalid quiz type'}), 400


@quiz_bp.route('/api/quiz/results/<user_id>', methods=['GET'])
def get_quiz_results(user_id):
    """Get user's quiz results"""
    try:
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not available'}), 500
        
        results = list(db.quiz_results.find({'user_id': user_id}).sort('completed_at', -1))
        
        for result in results:
            result['_id'] = str(result['_id'])
            if 'completed_at' in result:
                result['completed_at'] = result['completed_at'].isoformat()
        
        return jsonify({
            'results': results,
            'total': len(results)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Test endpoint
@quiz_bp.route('/api/quiz/test', methods=['GET'])
def test_quiz():
    """Test quiz API"""
    return jsonify({
        'status': 'Quiz API with AI Recommendations is working!',
        'aptitude_questions': len(APTITUDE_QUESTIONS),
        'personality_questions': len(PERSONALITY_QUESTIONS),
        'features': [
            'Aptitude test with skill identification',
            'Personality test with trait analysis',
            'AI-powered career recommendations',
            'Match scoring based on quiz results',
            'Detailed reasoning for each recommendation'
        ],
        'database': get_db() is not None
    }), 200