"""
Populate Quiz Questions in MongoDB
Run this script to add quiz questions to the database
"""

from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.career_counselling

print("=" * 60)
print("POPULATING QUIZ QUESTIONS")
print("=" * 60)

# Clear existing questions
print("\n1. Clearing existing quiz questions...")
result = db.quiz_questions.delete_many({})
print(f"   Deleted {result.deleted_count} old questions")

# Aptitude Questions
aptitude_questions = [
    {
        'type': 'aptitude',
        'category': 'numerical',
        'question': 'What is 2 + 2?',
        'options': ['3', '4', '5', '6'],
        'correct_answer': 1,  # Index of correct answer
        'skills_tested': ['numerical_reasoning', 'basic_math'],
        'difficulty': 'easy',
        'created_at': datetime.utcnow()
    },
    {
        'type': 'aptitude',
        'category': 'logical',
        'question': 'If 5 machines can produce 5 products in 5 minutes, how many products can 100 machines produce in 100 minutes?',
        'options': ['100', '500', '2000', '10000'],
        'correct_answer': 2,
        'skills_tested': ['logical_reasoning', 'problem_solving'],
        'difficulty': 'medium',
        'created_at': datetime.utcnow()
    },
    {
        'type': 'aptitude',
        'category': 'logical',
        'question': 'What is the next number in the sequence: 2, 6, 12, 20, 30, ?',
        'options': ['38', '40', '42', '44'],
        'correct_answer': 2,
        'skills_tested': ['pattern_recognition', 'logical_reasoning'],
        'difficulty': 'medium',
        'created_at': datetime.utcnow()
    },
    {
        'type': 'aptitude',
        'category': 'numerical',
        'question': 'If A + B = 10 and A - B = 4, what is the value of A?',
        'options': ['6', '7', '8', '9'],
        'correct_answer': 1,
        'skills_tested': ['algebra', 'numerical_reasoning'],
        'difficulty': 'medium',
        'created_at': datetime.utcnow()
    },
    {
        'type': 'aptitude',
        'category': 'verbal',
        'question': 'Choose the synonym of "Eloquent"',
        'options': ['Articulate', 'Hesitant', 'Silent', 'Confused'],
        'correct_answer': 0,
        'skills_tested': ['verbal_reasoning', 'vocabulary'],
        'difficulty': 'easy',
        'created_at': datetime.utcnow()
    },
    {
        'type': 'aptitude',
        'category': 'numerical',
        'question': 'A clock shows 3:15. What is the angle between hour and minute hands?',
        'options': ['0°', '7.5°', '15°', '30°'],
        'correct_answer': 1,
        'skills_tested': ['spatial_reasoning', 'numerical_reasoning'],
        'difficulty': 'hard',
        'created_at': datetime.utcnow()
    },
    {
        'type': 'aptitude',
        'category': 'logical',
        'question': 'Which number comes next in the Fibonacci sequence: 1, 1, 2, 3, 5, 8, 13, ?',
        'options': ['18', '21', '24', '27'],
        'correct_answer': 1,
        'skills_tested': ['pattern_recognition', 'logical_reasoning'],
        'difficulty': 'medium',
        'created_at': datetime.utcnow()
    },
    {
        'type': 'aptitude',
        'category': 'numerical',
        'question': 'What is 15% of 200?',
        'options': ['20', '25', '30', '35'],
        'correct_answer': 2,
        'skills_tested': ['percentage_calculation', 'numerical_reasoning'],
        'difficulty': 'easy',
        'created_at': datetime.utcnow()
    },
    {
        'type': 'aptitude',
        'category': 'verbal',
        'question': 'Choose the antonym of "Optimistic"',
        'options': ['Hopeful', 'Pessimistic', 'Happy', 'Excited'],
        'correct_answer': 1,
        'skills_tested': ['verbal_reasoning', 'vocabulary'],
        'difficulty': 'easy',
        'created_at': datetime.utcnow()
    },
    {
        'type': 'aptitude',
        'category': 'logical',
        'question': 'If all Bloops are Razzies and all Razzies are Lazzies, then all Bloops are:',
        'options': ['Definitely Lazzies', 'Never Lazzies', 'Sometimes Lazzies', 'Cannot determine'],
        'correct_answer': 0,
        'skills_tested': ['logical_reasoning', 'deductive_reasoning'],
        'difficulty': 'medium',
        'created_at': datetime.utcnow()
    },
    {
        'type': 'aptitude',
        'category': 'numerical',
        'question': 'What is the average of 45, 55, 65, and 75?',
        'options': ['55', '60', '65', '70'],
        'correct_answer': 1,
        'skills_tested': ['numerical_reasoning', 'statistics'],
        'difficulty': 'easy',
        'created_at': datetime.utcnow()
    },
    {
        'type': 'aptitude',
        'category': 'verbal',
        'question': 'Which sentence is grammatically correct?',
        'options': [
            "He don't like coffee",
            "He doesn't likes coffee",
            "He doesn't like coffee",
            "He don't likes coffee"
        ],
        'correct_answer': 2,
        'skills_tested': ['grammar', 'verbal_reasoning'],
        'difficulty': 'easy',
        'created_at': datetime.utcnow()
    },
    {
        'type': 'aptitude',
        'category': 'logical',
        'question': 'A bat and a ball cost ₹110 in total. The bat costs ₹100 more than the ball. How much does the ball cost?',
        'options': ['₹5', '₹10', '₹15', '₹20'],
        'correct_answer': 0,
        'skills_tested': ['problem_solving', 'logical_reasoning'],
        'difficulty': 'hard',
        'created_at': datetime.utcnow()
    },
    {
        'type': 'aptitude',
        'category': 'numerical',
        'question': 'If 3x + 5 = 20, what is the value of x?',
        'options': ['3', '4', '5', '6'],
        'correct_answer': 2,
        'skills_tested': ['algebra', 'numerical_reasoning'],
        'difficulty': 'medium',
        'created_at': datetime.utcnow()
    },
    {
        'type': 'aptitude',
        'category': 'logical',
        'question': 'Which shape completes the pattern: Circle, Square, Triangle, Circle, Square, ?',
        'options': ['Circle', 'Square', 'Triangle', 'Rectangle'],
        'correct_answer': 2,
        'skills_tested': ['pattern_recognition', 'spatial_reasoning'],
        'difficulty': 'easy',
        'created_at': datetime.utcnow()
    },
    {
        'type': 'aptitude',
        'category': 'numerical',
        'question': 'A rectangle has length 12 cm and width 5 cm. What is its area?',
        'options': ['50 cm²', '55 cm²', '60 cm²', '65 cm²'],
        'correct_answer': 2,
        'skills_tested': ['geometry', 'numerical_reasoning'],
        'difficulty': 'easy',
        'created_at': datetime.utcnow()
    },
    {
        'type': 'aptitude',
        'category': 'verbal',
        'question': 'Choose the correct idiom: To "_____ the bucket" means to die.',
        'options': ['kick', 'fill', 'carry', 'throw'],
        'correct_answer': 0,
        'skills_tested': ['idioms', 'verbal_reasoning'],
        'difficulty': 'medium',
        'created_at': datetime.utcnow()
    },
    {
        'type': 'aptitude',
        'category': 'numerical',
        'question': 'What is 2³ + 3²?',
        'options': ['15', '16', '17', '18'],
        'correct_answer': 2,
        'skills_tested': ['exponents', 'numerical_reasoning'],
        'difficulty': 'medium',
        'created_at': datetime.utcnow()
    },
    {
        'type': 'aptitude',
        'category': 'logical',
        'question': 'If 5 cats can catch 5 mice in 5 minutes, how many cats are needed to catch 100 mice in 100 minutes?',
        'options': ['5', '10', '20', '100'],
        'correct_answer': 0,
        'skills_tested': ['logical_reasoning', 'problem_solving'],
        'difficulty': 'hard',
        'created_at': datetime.utcnow()
    },
    {
        'type': 'aptitude',
        'category': 'verbal',
        'question': 'Find the correctly spelled word:',
        'options': ['Occassion', 'Occasion', 'Ocassion', 'Ocasion'],
        'correct_answer': 1,
        'skills_tested': ['spelling', 'verbal_reasoning'],
        'difficulty': 'easy',
        'created_at': datetime.utcnow()
    }
]

# Personality Questions
personality_questions = [
    {
        'type': 'personality',
        'category': 'work_style',
        'question': 'I prefer working:',
        'options': ['Alone', 'In small groups', 'In large teams', 'It depends on the task'],
        'trait_mapping': {
            '0': {'introversion': 3, 'independence': 3},
            '1': {'teamwork': 2, 'collaboration': 2},
            '2': {'extraversion': 3, 'teamwork': 3},
            '3': {'adaptability': 3, 'flexibility': 2}
        },
        'created_at': datetime.utcnow()
    },
    {
        'type': 'personality',
        'category': 'problem_solving',
        'question': 'When faced with a problem, I tend to:',
        'options': ['Analyze it logically', 'Think creatively', 'Seek advice from others', 'Take immediate action'],
        'trait_mapping': {
            '0': {'analytical': 3, 'logical_thinking': 3},
            '1': {'creativity': 3, 'innovation': 3},
            '2': {'collaboration': 3, 'communication': 2},
            '3': {'decisive': 3, 'action_oriented': 3}
        },
        'created_at': datetime.utcnow()
    },
    {
        'type': 'personality',
        'category': 'interests',
        'question': 'I am most interested in:',
        'options': ['Technology and innovation', 'Helping people', 'Business and finance', 'Arts and creativity'],
        'trait_mapping': {
            '0': {'technical': 3, 'innovative': 3},
            '1': {'empathy': 3, 'helping': 3},
            '2': {'business_oriented': 3, 'analytical': 2},
            '3': {'creative': 3, 'artistic': 3}
        },
        'created_at': datetime.utcnow()
    },
    {
        'type': 'personality',
        'category': 'work_environment',
        'question': 'My ideal work environment is:',
        'options': ['Structured and organized', 'Flexible and dynamic', 'Collaborative and social', 'Independent and quiet'],
        'trait_mapping': {
            '0': {'organized': 3, 'detail_oriented': 2},
            '1': {'adaptable': 3, 'flexible': 3},
            '2': {'social': 3, 'teamwork': 3},
            '3': {'independent': 3, 'focused': 2}
        },
        'created_at': datetime.utcnow()
    },
    {
        'type': 'personality',
        'category': 'motivation',
        'question': 'I am motivated by:',
        'options': ['Financial rewards', 'Recognition and status', 'Making a positive impact', 'Learning new things'],
        'trait_mapping': {
            '0': {'money_motivated': 3, 'ambitious': 2},
            '1': {'recognition_seeking': 3, 'competitive': 2},
            '2': {'altruistic': 3, 'purpose_driven': 3},
            '3': {'curious': 3, 'growth_oriented': 3}
        },
        'created_at': datetime.utcnow()
    },
    {
        'type': 'personality',
        'category': 'creativity',
        'question': 'I enjoy coming up with new and innovative ideas:',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'trait_mapping': {
            '0': {'traditional': 2},
            '1': {'traditional': 1},
            '2': {'balanced': 2},
            '3': {'creative': 2, 'innovative': 2},
            '4': {'creative': 3, 'innovative': 3}
        },
        'created_at': datetime.utcnow()
    },
    {
        'type': 'personality',
        'category': 'leadership',
        'question': 'I am comfortable taking charge and leading groups:',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'trait_mapping': {
            '0': {'follower': 2},
            '1': {'follower': 1},
            '2': {'balanced': 2},
            '3': {'leadership': 2, 'confident': 2},
            '4': {'leadership': 3, 'confident': 3}
        },
        'created_at': datetime.utcnow()
    },
    {
        'type': 'personality',
        'category': 'work_preference',
        'question': 'I prefer hands-on practical work over theoretical work:',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'trait_mapping': {
            '0': {'theoretical': 3},
            '1': {'theoretical': 2},
            '2': {'balanced': 2},
            '3': {'practical': 2, 'hands_on': 2},
            '4': {'practical': 3, 'hands_on': 3}
        },
        'created_at': datetime.utcnow()
    },
    {
        'type': 'personality',
        'category': 'career_interest',
        'question': 'I am interested in healthcare and helping sick people:',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'trait_mapping': {
            '0': {},
            '1': {},
            '2': {'healthcare_interest': 1},
            '3': {'healthcare_interest': 2, 'empathy': 2},
            '4': {'healthcare_interest': 3, 'empathy': 3}
        },
        'created_at': datetime.utcnow()
    },
    {
        'type': 'personality',
        'category': 'values',
        'question': 'I care deeply about environmental and social issues:',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'trait_mapping': {
            '0': {},
            '1': {},
            '2': {'socially_conscious': 1},
            '3': {'socially_conscious': 2, 'altruistic': 2},
            '4': {'socially_conscious': 3, 'altruistic': 3}
        },
        'created_at': datetime.utcnow()
    },
    {
        'type': 'personality',
        'category': 'organization',
        'question': 'I am very organized and keep things tidy:',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'trait_mapping': {
            '0': {'spontaneous': 2},
            '1': {'spontaneous': 1},
            '2': {'balanced': 2},
            '3': {'organized': 2, 'detail_oriented': 2},
            '4': {'organized': 3, 'detail_oriented': 3}
        },
        'created_at': datetime.utcnow()
    },
    {
        'type': 'personality',
        'category': 'social',
        'question': 'I enjoy being around people and making new friends:',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'trait_mapping': {
            '0': {'introversion': 3},
            '1': {'introversion': 2},
            '2': {'balanced': 2},
            '3': {'extraversion': 2, 'social': 2},
            '4': {'extraversion': 3, 'social': 3}
        },
        'created_at': datetime.utcnow()
    },
    {
        'type': 'personality',
        'category': 'risk',
        'question': 'I am comfortable taking calculated risks:',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'trait_mapping': {
            '0': {'risk_averse': 3},
            '1': {'risk_averse': 2},
            '2': {'balanced': 2},
            '3': {'risk_taking': 2, 'entrepreneurial': 2},
            '4': {'risk_taking': 3, 'entrepreneurial': 3}
        },
        'created_at': datetime.utcnow()
    },
    {
        'type': 'personality',
        'category': 'communication',
        'question': 'I enjoy explaining concepts and teaching others:',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'trait_mapping': {
            '0': {},
            '1': {},
            '2': {'communication': 1},
            '3': {'teaching': 2, 'communication': 2},
            '4': {'teaching': 3, 'communication': 3}
        },
        'created_at': datetime.utcnow()
    },
    {
        'type': 'personality',
        'category': 'detail',
        'question': 'I pay attention to details and strive for perfection:',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'trait_mapping': {
            '0': {'big_picture': 2},
            '1': {'big_picture': 1},
            '2': {'balanced': 2},
            '3': {'detail_oriented': 2, 'perfectionist': 2},
            '4': {'detail_oriented': 3, 'perfectionist': 3}
        },
        'created_at': datetime.utcnow()
    },
    {
        'type': 'personality',
        'category': 'adaptability',
        'question': 'I adapt quickly to new situations and changes:',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'trait_mapping': {
            '0': {'routine_oriented': 2},
            '1': {'routine_oriented': 1},
            '2': {'balanced': 2},
            '3': {'adaptable': 2, 'flexible': 2},
            '4': {'adaptable': 3, 'flexible': 3}
        },
        'created_at': datetime.utcnow()
    },
    {
        'type': 'personality',
        'category': 'stress',
        'question': 'I remain calm under pressure and handle stress well:',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'trait_mapping': {
            '0': {'stress_prone': 2},
            '1': {'stress_prone': 1},
            '2': {'balanced': 2},
            '3': {'stress_resistant': 2, 'calm': 2},
            '4': {'stress_resistant': 3, 'calm': 3}
        },
        'created_at': datetime.utcnow()
    },
    {
        'type': 'personality',
        'category': 'independence',
        'question': 'I can work independently without much supervision:',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'trait_mapping': {
            '0': {'needs_guidance': 2},
            '1': {'needs_guidance': 1},
            '2': {'balanced': 2},
            '3': {'independent': 2, 'self_directed': 2},
            '4': {'independent': 3, 'self_directed': 3}
        },
        'created_at': datetime.utcnow()
    },
    {
        'type': 'personality',
        'category': 'competitive',
        'question': 'I enjoy competing and being the best:',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'trait_mapping': {
            '0': {'cooperative': 2},
            '1': {'cooperative': 1},
            '2': {'balanced': 2},
            '3': {'competitive': 2, 'ambitious': 2},
            '4': {'competitive': 3, 'ambitious': 3}
        },
        'created_at': datetime.utcnow()
    },
    {
        'type': 'personality',
        'category': 'technology',
        'question': 'I am interested in understanding how technology works:',
        'options': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'trait_mapping': {
            '0': {},
            '1': {},
            '2': {'technical_interest': 1},
            '3': {'technical_interest': 2, 'technical': 2},
            '4': {'technical_interest': 3, 'technical': 3}
        },
        'created_at': datetime.utcnow()
    }
]

# Insert questions
print("\n2. Inserting aptitude questions...")
result = db.quiz_questions.insert_many(aptitude_questions)
print(f"   Inserted {len(result.inserted_ids)} aptitude questions")

print("\n3. Inserting personality questions...")
result = db.quiz_questions.insert_many(personality_questions)
print(f"   Inserted {len(result.inserted_ids)} personality questions")

# Verify
print("\n4. Verifying...")
aptitude_count = db.quiz_questions.count_documents({'type': 'aptitude'})
personality_count = db.quiz_questions.count_documents({'type': 'personality'})

print(f"   ✓ Aptitude questions: {aptitude_count}")
print(f"   ✓ Personality questions: {personality_count}")
print(f"   ✓ Total questions: {aptitude_count + personality_count}")

print("\n" + "=" * 60)
print("✅ QUIZ QUESTIONS POPULATED SUCCESSFULLY!")
print("=" * 60)
print("\nYou can now use the quiz feature!")
print("Test it at: http://localhost:3000/quiz")
print("=" * 60)