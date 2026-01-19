from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
from bson import ObjectId
import jwt

appointment_bp = Blueprint('appointment', __name__)


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
        return payload['user_id'], payload.get('role'), None, None
    except:
        return None, None, {'error': 'Invalid token'}, 401


# ==================== COUNSELLOR ROUTES ====================

@appointment_bp.route('/counsellors', methods=['GET'])
def get_all_counsellors():
    """
    Get all available counsellors
    GET /api/counsellors?specialization=career
    """
    try:
        db = current_app.config['DB']
        
        # Get query parameters
        specialization = request.args.get('specialization')
        available_only = request.args.get('available', 'false').lower() == 'true'
        
        # Build query - find users with role 'counsellor'
        query = {'role': 'counsellor', 'is_active': True}
        
        if specialization:
            query['profile.specialization'] = specialization
        
        # Get counsellors
        counsellors = list(db.users.find(query, {'password': 0}))
        
        # Format response
        counsellor_list = []
        for counsellor in counsellors:
            counsellor_list.append({
                'id': str(counsellor['_id']),
                'name': counsellor['name'],
                'email': counsellor['email'],
                'phone': counsellor.get('phone'),
                'specialization': counsellor.get('profile', {}).get('specialization', 'General'),
                'experience': counsellor.get('profile', {}).get('experience', 'N/A'),
                'rating': counsellor.get('rating', 4.5),
                'sessions_conducted': counsellor.get('sessions_conducted', 0),
                'available_slots': counsellor.get('available_slots', []),
                'hourly_rate': counsellor.get('hourly_rate', 500)
            })
        
        return jsonify({
            'counsellors': counsellor_list,
            'total': len(counsellor_list)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@appointment_bp.route('/counsellors/<counsellor_id>', methods=['GET'])
def get_counsellor_details(counsellor_id):
    """
    Get specific counsellor details
    GET /api/counsellors/<counsellor_id>
    """
    try:
        db = current_app.config['DB']
        
        # For in-memory DB
        if isinstance(db, dict):
            # Find counsellor in users dict
            counsellor = None
            for email, user in db.get('users', {}).items():
                if email == counsellor_id and user.get('role') == 'counsellor':
                    counsellor = user
                    break
            
            if not counsellor:
                return jsonify({'error': 'Counsellor not found'}), 404
        else:
            # For MongoDB
            counsellor = db.users.find_one({
                '_id': ObjectId(counsellor_id),
                'role': 'counsellor'
            }, {'password': 0})
            
            if not counsellor:
                return jsonify({'error': 'Counsellor not found'}), 404
        
        return jsonify({
            'id': counsellor_id,
            'name': counsellor['name'],
            'email': counsellor['email'],
            'phone': counsellor.get('phone'),
            'specialization': counsellor.get('profile', {}).get('specialization', 'General'),
            'experience': counsellor.get('profile', {}).get('experience', 'N/A'),
            'bio': counsellor.get('profile', {}).get('bio', ''),
            'education': counsellor.get('profile', {}).get('education', ''),
            'rating': counsellor.get('rating', 4.5),
            'sessions_conducted': counsellor.get('sessions_conducted', 0),
            'available_slots': counsellor.get('available_slots', []),
            'hourly_rate': counsellor.get('hourly_rate', 500)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@appointment_bp.route('/counsellors/<counsellor_id>/availability', methods=['GET'])
def get_counsellor_availability(counsellor_id):
    """
    Get counsellor's available time slots
    GET /api/counsellors/<counsellor_id>/availability?date=2026-01-10
    """
    try:
        db = current_app.config['DB']
        
        date_str = request.args.get('date')
        if date_str:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            target_date = datetime.utcnow().date()
        
        # Get counsellor's available slots
        # In real implementation, this would check the counsellor's schedule
        # For now, return sample slots
        available_slots = [
            {
                'start_time': '09:00',
                'end_time': '10:00',
                'available': True
            },
            {
                'start_time': '10:00',
                'end_time': '11:00',
                'available': True
            },
            {
                'start_time': '11:00',
                'end_time': '12:00',
                'available': False
            },
            {
                'start_time': '14:00',
                'end_time': '15:00',
                'available': True
            },
            {
                'start_time': '15:00',
                'end_time': '16:00',
                'available': True
            },
            {
                'start_time': '16:00',
                'end_time': '17:00',
                'available': True
            }
        ]
        
        return jsonify({
            'counsellor_id': counsellor_id,
            'date': date_str or target_date.isoformat(),
            'slots': available_slots
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== APPOINTMENT ROUTES ====================

@appointment_bp.route('/appointments', methods=['POST'])
def book_appointment():
    """
    Book an appointment with a counsellor
    POST /api/appointments
    Headers: Authorization: Bearer <token>
    Body: {
        "counsellor_id": "counsellor_email_or_id",
        "appointment_date": "2026-01-10",
        "appointment_time": "14:00",
        "duration": 60,
        "notes": "Need career guidance"
    }
    """
    try:
        db = current_app.config['DB']
        data = request.json
        
        # Get user from token
        user_id, role, error, status = get_user_from_token(request)
        if error:
            return jsonify(error), status
        
        # Validate required fields
        required = ['counsellor_id', 'appointment_date', 'appointment_time']
        for field in required:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Parse appointment datetime
        appointment_datetime = datetime.strptime(
            f"{data['appointment_date']} {data['appointment_time']}", 
            '%Y-%m-%d %H:%M'
        )
        
        # Create appointment
        appointment = {
            'student_id': str(user_id),
            'counsellor_id': data['counsellor_id'],
            'appointment_date': appointment_datetime,
            'duration': data.get('duration', 60),  # Default 60 minutes
            'status': 'scheduled',
            'meeting_link': None,
            'notes': data.get('notes', ''),
            'rating': None,
            'feedback': None,
            'payment_status': 'pending',
            'payment_amount': data.get('amount', 500.0),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        # Store appointment
        if isinstance(db, dict):
            # In-memory storage
            if 'appointments' not in db:
                db['appointments'] = []
            
            appointment['id'] = f"apt_{len(db['appointments']) + 1}"
            db['appointments'].append(appointment)
            appointment_id = appointment['id']
        else:
            # MongoDB
            result = db.appointments.insert_one(appointment)
            appointment_id = str(result.inserted_id)
        
        return jsonify({
            'message': 'Appointment booked successfully',
            'appointment_id': appointment_id,
            'appointment': {
                'id': appointment_id,
                'counsellor_id': appointment['counsellor_id'],
                'date': appointment['appointment_date'].isoformat(),
                'duration': appointment['duration'],
                'status': appointment['status'],
                'amount': appointment['payment_amount']
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@appointment_bp.route('/appointments', methods=['GET'])
def get_user_appointments():
    """
    Get all appointments for logged-in user
    GET /api/appointments?status=scheduled
    Headers: Authorization: Bearer <token>
    """
    try:
        db = current_app.config['DB']
        
        # Get user from token
        user_id, role, error, status = get_user_from_token(request)
        if error:
            return jsonify(error), status
        
        status_filter = request.args.get('status')
        
        # Get appointments
        if isinstance(db, dict):
            # In-memory storage
            appointments = db.get('appointments', [])
            user_appointments = [
                apt for apt in appointments 
                if apt['student_id'] == str(user_id) or apt['counsellor_id'] == str(user_id)
            ]
            
            if status_filter:
                user_appointments = [
                    apt for apt in user_appointments 
                    if apt['status'] == status_filter
                ]
        else:
            # MongoDB
            query = {
                '$or': [
                    {'student_id': str(user_id)},
                    {'counsellor_id': str(user_id)}
                ]
            }
            
            if status_filter:
                query['status'] = status_filter
            
            user_appointments = list(db.appointments.find(query))
        
        # Format appointments
        formatted_appointments = []
        for apt in user_appointments:
            formatted_appointments.append({
                'id': apt.get('id') or str(apt.get('_id')),
                'counsellor_id': apt['counsellor_id'],
                'student_id': apt['student_id'],
                'date': apt['appointment_date'].isoformat() if isinstance(apt['appointment_date'], datetime) else apt['appointment_date'],
                'duration': apt['duration'],
                'status': apt['status'],
                'notes': apt.get('notes'),
                'meeting_link': apt.get('meeting_link'),
                'payment_status': apt['payment_status'],
                'payment_amount': apt['payment_amount']
            })
        
        return jsonify({
            'appointments': formatted_appointments,
            'total': len(formatted_appointments)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
# Add this route to your appointment_routes.py file
# Place it after the get_user_appointments function (around line 270)

@appointment_bp.route('/counsellor/appointments', methods=['GET'])
def get_counsellor_appointments():
    """
    Get all appointments for a counsellor (counsellor only)
    GET /api/counsellor/appointments
    Headers: Authorization: Bearer <token>
    """
    try:
        db = current_app.config['DB']
        
        # Get user from token
        user_id, role, error, status_code = get_user_from_token(request)
        if error:
            return jsonify(error), status_code
        
        # Check if user is a counsellor
        if role != 'counsellor':
            return jsonify({'error': 'Access denied. Counsellors only.'}), 403
        
        # Get appointments where this user is the counsellor
        if isinstance(db, dict):
            # In-memory storage
            appointments = db.get('appointments', [])
            counsellor_appointments = [
                apt for apt in appointments 
                if apt['counsellor_id'] == str(user_id)
            ]
        else:
            # MongoDB
            counsellor_appointments = list(db.appointments.find({
                'counsellor_id': str(user_id)
            }).sort('created_at', -1))  # Most recent first
        
        # Get student details for each appointment
        formatted_appointments = []
        for apt in counsellor_appointments:
            # Get student info
            student_email = apt.get('student_id')
            student_info = None
            
            if isinstance(db, dict):
                student_info = db.get('users', {}).get(student_email, {})
            else:
                try:
                    student = db.users.find_one({'_id': ObjectId(student_email)})
                    if not student:
                        student = db.users.find_one({'email': student_email})
                    student_info = student
                except:
                    student = db.users.find_one({'email': student_email})
                    student_info = student
            
            formatted_appointments.append({
                'id': apt.get('id') or str(apt.get('_id')),
                'student_id': apt['student_id'],
                'student_name': student_info.get('name', 'Unknown Student') if student_info else 'Unknown Student',
                'student_email': student_info.get('email', apt['student_id']) if student_info else apt['student_id'],
                'counsellor_id': apt['counsellor_id'],
                'appointment_date': apt['appointment_date'].isoformat() if isinstance(apt['appointment_date'], datetime) else apt['appointment_date'],
                'duration': apt.get('duration', 60),
                'status': apt.get('status', 'scheduled'),
                'notes': apt.get('notes', ''),
                'meeting_link': apt.get('meeting_link'),
                'payment_status': apt.get('payment_status', 'pending'),
                'amount': apt.get('payment_amount', 500),
                'rating': apt.get('rating'),
                'feedback': apt.get('feedback'),
                'created_at': apt['created_at'].isoformat() if isinstance(apt.get('created_at'), datetime) else str(apt.get('created_at', ''))
            })
        
        return jsonify({
            'success': True,
            'appointments': formatted_appointments,
            'total': len(formatted_appointments)
        }), 200
        
    except Exception as e:
        print(f'Error fetching counsellor appointments: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to fetch appointments',
            'message': str(e)
        }), 500

@appointment_bp.route('/appointments/<appointment_id>', methods=['GET'])
def get_appointment_details(appointment_id):
    """
    Get specific appointment details
    GET /api/appointments/<appointment_id>
    Headers: Authorization: Bearer <token>
    """
    try:
        db = current_app.config['DB']
        
        # Get user from token
        user_id, role, error, status = get_user_from_token(request)
        if error:
            return jsonify(error), status
        
        # Get appointment
        if isinstance(db, dict):
            appointment = next(
                (apt for apt in db.get('appointments', []) if apt.get('id') == appointment_id),
                None
            )
        else:
            appointment = db.appointments.find_one({'_id': ObjectId(appointment_id)})
        
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        # Check authorization
        if appointment['student_id'] != str(user_id) and appointment['counsellor_id'] != str(user_id):
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify({
            'id': appointment.get('id') or str(appointment.get('_id')),
            'counsellor_id': appointment['counsellor_id'],
            'student_id': appointment['student_id'],
            'date': appointment['appointment_date'].isoformat() if isinstance(appointment['appointment_date'], datetime) else appointment['appointment_date'],
            'duration': appointment['duration'],
            'status': appointment['status'],
            'notes': appointment.get('notes'),
            'meeting_link': appointment.get('meeting_link'),
            'rating': appointment.get('rating'),
            'feedback': appointment.get('feedback'),
            'payment_status': appointment['payment_status'],
            'payment_amount': appointment['payment_amount']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@appointment_bp.route('/appointments/<appointment_id>/cancel', methods=['PUT'])
def cancel_appointment(appointment_id):
    """
    Cancel an appointment
    PUT /api/appointments/<appointment_id>/cancel
    Headers: Authorization: Bearer <token>
    """
    try:
        db = current_app.config['DB']
        
        # Get user from token
        user_id, role, error, status = get_user_from_token(request)
        if error:
            return jsonify(error), status
        
        # Update appointment status
        if isinstance(db, dict):
            appointment = next(
                (apt for apt in db.get('appointments', []) if apt.get('id') == appointment_id),
                None
            )
            if appointment:
                appointment['status'] = 'cancelled'
                appointment['updated_at'] = datetime.utcnow()
        else:
            result = db.appointments.update_one(
                {'_id': ObjectId(appointment_id)},
                {
                    '$set': {
                        'status': 'cancelled',
                        'updated_at': datetime.utcnow()
                    }
                }
            )
            
            if result.matched_count == 0:
                return jsonify({'error': 'Appointment not found'}), 404
        
        return jsonify({'message': 'Appointment cancelled successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@appointment_bp.route('/appointments/<appointment_id>/complete', methods=['PUT'])
def complete_appointment(appointment_id):
    """
    Mark appointment as completed (counsellor only)
    PUT /api/appointments/<appointment_id>/complete
    Headers: Authorization: Bearer <token>
    Body: {
        "notes": "Session notes",
        "meeting_link": "https://meet.google.com/xxx"
    }
    """
    try:
        db = current_app.config['DB']
        data = request.json
        
        # Get user from token
        user_id, role, error, status = get_user_from_token(request)
        if error:
            return jsonify(error), status
        
        # Update appointment
        if isinstance(db, dict):
            appointment = next(
                (apt for apt in db.get('appointments', []) if apt.get('id') == appointment_id),
                None
            )
            if appointment:
                appointment['status'] = 'completed'
                appointment['notes'] = data.get('notes', appointment.get('notes'))
                appointment['meeting_link'] = data.get('meeting_link')
                appointment['updated_at'] = datetime.utcnow()
        else:
            result = db.appointments.update_one(
                {'_id': ObjectId(appointment_id)},
                {
                    '$set': {
                        'status': 'completed',
                        'notes': data.get('notes'),
                        'meeting_link': data.get('meeting_link'),
                        'updated_at': datetime.utcnow()
                    }
                }
            )
            
            if result.matched_count == 0:
                return jsonify({'error': 'Appointment not found'}), 404
        
        return jsonify({'message': 'Appointment marked as completed'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@appointment_bp.route('/appointments/<appointment_id>/rate', methods=['POST'])
def rate_appointment(appointment_id):
    """
    Rate and review an appointment (student only, after completion)
    POST /api/appointments/<appointment_id>/rate
    Headers: Authorization: Bearer <token>
    Body: {
        "rating": 5,
        "feedback": "Great session!"
    }
    """
    try:
        db = current_app.config['DB']
        data = request.json
        
        # Get user from token
        user_id, role, error, status = get_user_from_token(request)
        if error:
            return jsonify(error), status
        
        # Validate rating
        rating = data.get('rating')
        if not rating or rating < 1 or rating > 5:
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        
        # Update appointment
        if isinstance(db, dict):
            appointment = next(
                (apt for apt in db.get('appointments', []) if apt.get('id') == appointment_id),
                None
            )
            if appointment:
                appointment['rating'] = rating
                appointment['feedback'] = data.get('feedback', '')
                appointment['updated_at'] = datetime.utcnow()
        else:
            result = db.appointments.update_one(
                {'_id': ObjectId(appointment_id), 'student_id': str(user_id)},
                {
                    '$set': {
                        'rating': rating,
                        'feedback': data.get('feedback', ''),
                        'updated_at': datetime.utcnow()
                    }
                }
            )
            
            if result.matched_count == 0:
                return jsonify({'error': 'Appointment not found or unauthorized'}), 404
        
        return jsonify({'message': 'Rating submitted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500