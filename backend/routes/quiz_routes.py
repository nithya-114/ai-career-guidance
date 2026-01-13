from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from bson import ObjectId
import jwt

quiz_bp = Blueprint('quiz', __name__)


# Helper function to get user from token
def get_user_from_token(request):
    """Extract user ID from JWT token"""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return None, {'error': 'No token provided'}, 401
    
    token = auth_header.split(' ')[1]
    
    try:
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        return payload['user_id'], None, None
    except:
        return None, {'error': 'Invalid token'}, 401


@quiz_bp.route('/quiz/<quiz_type>/questions', methods=['GET'])
def get_quiz_questions(quiz_type):
    """
    Get quiz questions
    GET /api/quiz/aptitude/questions
    GET /api/quiz/personality/questions
    """
    try:
        db = current_app.config['DB']
        
        if quiz_type not in ['aptitude', 'personality']:
            return jsonify({'error': 'Invalid quiz type'}), 400
        
        # Get questions
        questions = list(db.quiz_questions.find({'type': quiz_type}).limit(20))
        
        # Convert ObjectId and remove correct answers
        for question in questions:
            question['_id'] = str(question['_id'])
            if quiz_type == 'aptitude':
                # Don't send correct answer to client
                question.pop('correct_answer', None)
        
        return jsonify({
            'quiz_type': quiz_type,
            'questions': questions,
            'total_questions': len(questions)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@quiz_bp.route('/quiz/submit', methods=['POST'])
def submit_quiz():
    """
    Submit quiz answers
    POST /api/quiz/submit
    Headers: Authorization: Bearer <token>
    Body: {
        "quiz_type": "aptitude",
        "answers": [
            {"question_id": "q1", "answer": 0},
            {"question_id": "q2", "answer": 2}
        ],
        "time_taken": 1200
    }
    """
    try:
        db = current_app.config['DB']
        data = request.json
        
        # Get user from token
        user_id, error, status = get_user_from_token(request)
        if error:
            return jsonify(error), status
        
        quiz_type = data.get('quiz_type')
        answers = data.get('answers', [])
        time_taken = data.get('time_taken', 0)
        
        if quiz_type not in ['aptitude', 'personality']:
            return jsonify({'error': 'Invalid quiz type'}), 400
        
        # Calculate results
        score = 0
        personality_traits = {}
        skills = []
        
        if quiz_type == 'aptitude':
            # Calculate score for aptitude test
            for answer in answers:
                question = db.quiz_questions.find_one({
                    '_id': ObjectId(answer['question_id'])
                })
                if question and question.get('correct_answer') == answer.get('answer'):
                    score += 1
                    skills.extend(question.get('skills_tested', []))
        
        else:  # personality test
            # Aggregate personality traits
            for answer in answers:
                question = db.quiz_questions.find_one({
                    '_id': ObjectId(answer['question_id'])
                })
                if question and 'trait_mapping' in question:
                    trait_map = question['trait_mapping'].get(str(answer['answer']), {})
                    for trait, value in trait_map.items():
                        personality_traits[trait] = personality_traits.get(trait, 0) + value
        
        # Save quiz result
        quiz_result = {
            'user_id': str(user_id),
            'quiz_type': quiz_type,
            'questions': answers,
            'score': score if quiz_type == 'aptitude' else None,
            'personality_traits': personality_traits if quiz_type == 'personality' else None,
            'identified_skills': list(set(skills)) if skills else [],
            'completed_at': datetime.utcnow(),
            'time_taken': time_taken
        }
        
        result = db.quiz_results.insert_one(quiz_result)
        
        # Update user profile with identified skills
        if skills:
            db.users.update_one(
                {'_id': ObjectId(user_id)},
                {
                    '$addToSet': {
                        'profile.skills': {'$each': list(set(skills))}
                    }
                }
            )
        
        return jsonify({
            'message': 'Quiz submitted successfully',
            'result_id': str(result.inserted_id),
            'score': score if quiz_type == 'aptitude' else None,
            'personality_traits': personality_traits if quiz_type == 'personality' else None,
            'skills_identified': list(set(skills))
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@quiz_bp.route('/quiz/results/<user_id>', methods=['GET'])
def get_quiz_results(user_id):
    """
    Get all quiz results for a user
    GET /api/quiz/results/<user_id>
    """
    try:
        db = current_app.config['DB']
        
        results = list(db.quiz_results.find({'user_id': user_id}).sort('completed_at', -1))
        
        for result in results:
            result['_id'] = str(result['_id'])
            result['completed_at'] = result['completed_at'].isoformat()
        
        return jsonify({
            'results': results,
            'total': len(results)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500