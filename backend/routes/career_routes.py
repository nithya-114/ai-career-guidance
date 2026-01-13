from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId

career_bp = Blueprint('career', __name__)


@career_bp.route('/careers', methods=['GET'])
def get_careers():
    """
    Get all careers or filter by category
    GET /api/careers?category=Technology&limit=10&skip=0
    """
    try:
        db = current_app.config['DB']
        
        # Get query parameters
        category = request.args.get('category')
        limit = int(request.args.get('limit', 50))
        skip = int(request.args.get('skip', 0))
        search = request.args.get('search')
        
        # Build query
        query = {}
        if category:
            query['category'] = category
        if search:
            query['name'] = {'$regex': search, '$options': 'i'}
        
        # Get careers
        careers = list(db.careers.find(query).skip(skip).limit(limit))
        
        # Convert ObjectId to string
        for career in careers:
            career['_id'] = str(career['_id'])
            if 'created_at' in career:
                career['created_at'] = career['created_at'].isoformat()
            if 'updated_at' in career:
                career['updated_at'] = career['updated_at'].isoformat()
        
        total = db.careers.count_documents(query)
        
        return jsonify({
            'careers': careers,
            'total': total,
            'limit': limit,
            'skip': skip
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@career_bp.route('/careers/<career_id>', methods=['GET'])
def get_career_by_id(career_id):
    """
    Get specific career by ID
    GET /api/careers/<career_id>
    """
    try:
        db = current_app.config['DB']
        
        career = db.careers.find_one({'_id': ObjectId(career_id)})
        
        if not career:
            return jsonify({'error': 'Career not found'}), 404
        
        career['_id'] = str(career['_id'])
        if 'created_at' in career:
            career['created_at'] = career['created_at'].isoformat()
        if 'updated_at' in career:
            career['updated_at'] = career['updated_at'].isoformat()
        
        return jsonify(career), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@career_bp.route('/careers/categories', methods=['GET'])
def get_career_categories():
    """
    Get list of all career categories
    GET /api/careers/categories
    """
    try:
        db = current_app.config['DB']
        
        categories = db.careers.distinct('category')
        
        return jsonify({'categories': categories}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@career_bp.route('/courses', methods=['GET'])
def get_courses():
    """
    Get all courses or filter by career/type
    GET /api/courses?career=Software Engineer&type=Engineering
    """
    try:
        db = current_app.config['DB']
        
        # Get query parameters
        career = request.args.get('career')
        course_type = request.args.get('type')
        limit = int(request.args.get('limit', 50))
        skip = int(request.args.get('skip', 0))
        
        # Build query
        query = {}
        if career:
            query['career'] = career
        if course_type:
            query['type'] = course_type
        
        # Get courses
        courses = list(db.courses.find(query).skip(skip).limit(limit))
        
        # Convert ObjectId to string
        for course in courses:
            course['_id'] = str(course['_id'])
            if 'created_at' in course:
                course['created_at'] = course['created_at'].isoformat()
            if 'updated_at' in course:
                course['updated_at'] = course['updated_at'].isoformat()
        
        total = db.courses.count_documents(query)
        
        return jsonify({
            'courses': courses,
            'total': total,
            'limit': limit,
            'skip': skip
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@career_bp.route('/courses/<course_id>', methods=['GET'])
def get_course_by_id(course_id):
    """
    Get specific course by ID
    GET /api/courses/<course_id>
    """
    try:
        db = current_app.config['DB']
        
        course = db.courses.find_one({'_id': ObjectId(course_id)})
        
        if not course:
            return jsonify({'error': 'Course not found'}), 404
        
        course['_id'] = str(course['_id'])
        if 'created_at' in course:
            course['created_at'] = course['created_at'].isoformat()
        if 'updated_at' in course:
            course['updated_at'] = course['updated_at'].isoformat()
        
        return jsonify(course), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@career_bp.route('/colleges', methods=['GET'])
def get_colleges():
    """
    Get all colleges or filter by location/courses
    GET /api/colleges?state=Karnataka&location=Bangalore&course=B.Tech Computer Science
    """
    try:
        db = current_app.config['DB']
        
        # Get query parameters
        state = request.args.get('state')
        location = request.args.get('location')
        course = request.args.get('course')
        college_type = request.args.get('type')
        limit = int(request.args.get('limit', 50))
        skip = int(request.args.get('skip', 0))
        
        # Build query
        query = {}
        if state:
            query['state'] = state
        if location:
            query['location'] = {'$regex': location, '$options': 'i'}
        if course:
            query['courses'] = course
        if college_type:
            query['type'] = college_type
        
        # Get colleges
        colleges = list(db.colleges.find(query).sort('ranking', 1).skip(skip).limit(limit))
        
        # Convert ObjectId to string
        for college in colleges:
            college['_id'] = str(college['_id'])
            if 'created_at' in college:
                college['created_at'] = college['created_at'].isoformat()
            if 'updated_at' in college:
                college['updated_at'] = college['updated_at'].isoformat()
        
        total = db.colleges.count_documents(query)
        
        return jsonify({
            'colleges': colleges,
            'total': total,
            'limit': limit,
            'skip': skip
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@career_bp.route('/colleges/<college_id>', methods=['GET'])
def get_college_by_id(college_id):
    """
    Get specific college by ID
    GET /api/colleges/<college_id>
    """
    try:
        db = current_app.config['DB']
        
        college = db.colleges.find_one({'_id': ObjectId(college_id)})
        
        if not college:
            return jsonify({'error': 'College not found'}), 404
        
        college['_id'] = str(college['_id'])
        if 'created_at' in college:
            college['created_at'] = college['created_at'].isoformat()
        if 'updated_at' in college:
            college['updated_at'] = college['updated_at'].isoformat()
        
        return jsonify(college), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@career_bp.route('/colleges/states', methods=['GET'])
def get_states():
    """
    Get list of all states with colleges
    GET /api/colleges/states
    """
    try:
        db = current_app.config['DB']
        
        states = db.colleges.distinct('state')
        
        return jsonify({'states': sorted(states)}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500