from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from bson import ObjectId
import razorpay
import hmac
import hashlib
import os
import jwt

payment_bp = Blueprint('payment', __name__)

# Initialize Razorpay client
razorpay_client = razorpay.Client(
    auth=(
        os.getenv('RAZORPAY_KEY_ID', 'rzp_test_your_key_here'),
        os.getenv('RAZORPAY_KEY_SECRET', 'your_secret_here')
    )
)


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
    except jwt.ExpiredSignatureError:
        return None, {'error': 'Token expired'}, 401
    except:
        return None, {'error': 'Invalid token'}, 401


@payment_bp.route('/create-order', methods=['POST'])
def create_order():
    """Create Razorpay order"""
    try:
        db = current_app.config['DB']
        data = request.json
        
        # Get user from token
        user_id, error, status = get_user_from_token(request)
        if error:
            return jsonify(error), status
        
        # Validate required fields
        required = ['counsellor_id', 'date', 'time', 'duration', 'amount']
        for field in required:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Get counsellor
        counsellor = db.users.find_one({
            '_id': ObjectId(data['counsellor_id']),
            'role': 'counsellor'
        })
        
        if not counsellor:
            return jsonify({'error': 'Counsellor not found'}), 404
        
        # Calculate amount in paise (Razorpay uses smallest currency unit)
        amount_inr = int(data['amount'])
        amount_paise = amount_inr * 100
        
        # Create Razorpay order
        razorpay_order = razorpay_client.order.create({
            'amount': amount_paise,
            'currency': 'INR',
            'payment_capture': 1,
            'notes': {
                'counsellor_id': data['counsellor_id'],
                'counsellor_name': counsellor['name'],
                'student_id': str(user_id),
                'date': data['date'],
                'time': data['time'],
                'duration': str(data['duration'])
            }
        })
        
        # Save order in database
        order_doc = {
            'razorpay_order_id': razorpay_order['id'],
            'counsellor_id': ObjectId(data['counsellor_id']),
            'counsellor_name': counsellor['name'],
            'student_id': ObjectId(user_id),
            'date': data['date'],
            'time': data['time'],
            'duration': data['duration'],
            'amount': amount_inr,
            'currency': 'INR',
            'status': 'created',
            'created_at': datetime.utcnow()
        }
        
        db.payment_orders.insert_one(order_doc)
        
        print(f"✅ Order created: {razorpay_order['id']}")
        
        return jsonify({
            'order_id': razorpay_order['id'],
            'amount': amount_paise,
            'currency': 'INR',
            'key_id': os.getenv('RAZORPAY_KEY_ID')
        }), 201
        
    except Exception as e:
        print(f"❌ Create order error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@payment_bp.route('/verify-payment', methods=['POST'])
def verify_payment():
    """Verify Razorpay payment signature"""
    try:
        db = current_app.config['DB']
        data = request.json
        
        # Get user from token
        user_id, error, status = get_user_from_token(request)
        if error:
            return jsonify(error), status
        
        # Get payment details
        order_id = data.get('razorpay_order_id')
        payment_id = data.get('razorpay_payment_id')
        signature = data.get('razorpay_signature')
        
        if not all([order_id, payment_id, signature]):
            return jsonify({'error': 'Missing payment details'}), 400
        
        # Verify signature
        message = f"{order_id}|{payment_id}"
        generated_signature = hmac.new(
            os.getenv('RAZORPAY_KEY_SECRET').encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        if generated_signature != signature:
            return jsonify({'error': 'Invalid payment signature'}), 400
        
        # Get order
        order = db.payment_orders.find_one({'razorpay_order_id': order_id})
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        # Verify user owns this order
        if str(order['student_id']) != str(user_id):
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Update order status
        db.payment_orders.update_one(
            {'razorpay_order_id': order_id},
            {
                '$set': {
                    'razorpay_payment_id': payment_id,
                    'razorpay_signature': signature,
                    'status': 'paid',
                    'paid_at': datetime.utcnow()
                }
            }
        )
        
        # Create appointment
        appointment = {
            'student_id': order['student_id'],
            'counsellor_id': order['counsellor_id'],
            'counsellor_name': order['counsellor_name'],
            'appointment_date': datetime.strptime(
                f"{order['date']} {order['time']}", 
                '%Y-%m-%d %H:%M'
            ),
            'duration': int(order['duration']) * 60,  # Convert to minutes
            'status': 'scheduled',
            'meeting_link': None,
            'notes': '',
            'rating': None,
            'feedback': None,
            'payment_status': 'paid',
            'payment_amount': float(order['amount']),
            'payment_id': payment_id,
            'order_id': order_id,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = db.appointments.insert_one(appointment)
        
        print(f"✅ Payment verified and appointment created: {result.inserted_id}")
        
        return jsonify({
            'success': True,
            'message': 'Payment verified successfully',
            'appointment_id': str(result.inserted_id)
        }), 200
        
    except Exception as e:
        print(f"❌ Verify payment error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@payment_bp.route('/my-bookings', methods=['GET'])
def my_bookings():
    """Get user's bookings"""
    try:
        db = current_app.config['DB']
        
        # Get user from token
        user_id, error, status = get_user_from_token(request)
        if error:
            return jsonify(error), status
        
        # Get appointments
        appointments = list(db.appointments.find({
            'student_id': ObjectId(user_id)
        }).sort('created_at', -1))
        
        # Format response
        for apt in appointments:
            apt['_id'] = str(apt['_id'])
            apt['student_id'] = str(apt['student_id'])
            apt['counsellor_id'] = str(apt['counsellor_id'])
            
            if isinstance(apt.get('appointment_date'), datetime):
                apt['appointment_date'] = apt['appointment_date'].isoformat()
            if isinstance(apt.get('created_at'), datetime):
                apt['created_at'] = apt['created_at'].isoformat()
        
        return jsonify({'appointments': appointments}), 200
        
    except Exception as e:
        print(f"❌ My bookings error: {str(e)}")
        return jsonify({'error': str(e)}), 500