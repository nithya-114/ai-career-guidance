from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from bson import ObjectId
import razorpay
import hmac
import hashlib
import os

payment_bp = Blueprint('payment', __name__)

# Initialize Razorpay client
razorpay_client = razorpay.Client(
    auth=(
        os.getenv('RAZORPAY_KEY_ID'),
        os.getenv('RAZORPAY_KEY_SECRET')
    )
)


@payment_bp.route('/create-order', methods=['POST', 'OPTIONS'])
def create_order():
    """
    Create Razorpay order for counsellor booking
    POST /api/payment/create-order
    Body: {
        "counsellor_id": "...",
        "date": "2026-01-20",
        "time": "10:00",
        "duration": 1,  # hours
        "amount": 500
    }
    """
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        db = current_app.config['DB']
        data = request.json
        
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
        
        # Calculate amount (in paise - Razorpay uses smallest currency unit)
        amount_inr = int(data['amount'])
        amount_paise = amount_inr * 100
        
        # Create Razorpay order
        razorpay_order = razorpay_client.order.create({
            'amount': amount_paise,
            'currency': 'INR',
            'payment_capture': 1,  # Auto capture
            'notes': {
                'counsellor_id': data['counsellor_id'],
                'counsellor_name': counsellor['name'],
                'date': data['date'],
                'time': data['time'],
                'duration': data['duration']
            }
        })
        
        # Save order in database
        order_doc = {
            'razorpay_order_id': razorpay_order['id'],
            'counsellor_id': ObjectId(data['counsellor_id']),
            'counsellor_name': counsellor['name'],
            'student_id': ObjectId(data.get('student_id')) if data.get('student_id') else None,
            'date': data['date'],
            'time': data['time'],
            'duration': data['duration'],
            'amount': amount_inr,
            'currency': 'INR',
            'status': 'created',
            'created_at': datetime.utcnow()
        }
        
        db.payment_orders.insert_one(order_doc)
        
        return jsonify({
            'order_id': razorpay_order['id'],
            'amount': amount_paise,
            'currency': 'INR',
            'key_id': os.getenv('RAZORPAY_KEY_ID')
        }), 201
        
    except Exception as e:
        print(f"❌ Create order error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@payment_bp.route('/verify-payment', methods=['POST', 'OPTIONS'])
def verify_payment():
    """
    Verify Razorpay payment signature
    POST /api/payment/verify-payment
    Body: {
        "razorpay_order_id": "...",
        "razorpay_payment_id": "...",
        "razorpay_signature": "..."
    }
    """
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        db = current_app.config['DB']
        data = request.json
        
        # Get required fields
        order_id = data.get('razorpay_order_id')
        payment_id = data.get('razorpay_payment_id')
        signature = data.get('razorpay_signature')
        
        if not all([order_id, payment_id, signature]):
            return jsonify({'error': 'Missing payment details'}), 400
        
        # Verify signature
        try:
            # Create signature string
            message = f"{order_id}|{payment_id}"
            
            # Generate signature
            generated_signature = hmac.new(
                os.getenv('RAZORPAY_KEY_SECRET').encode('utf-8'),
                message.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            # Compare signatures
            if generated_signature != signature:
                return jsonify({'error': 'Invalid payment signature'}), 400
            
        except Exception as e:
            print(f"❌ Signature verification error: {e}")
            return jsonify({'error': 'Payment verification failed'}), 400
        
        # Payment is valid - update order
        order = db.payment_orders.find_one({'razorpay_order_id': order_id})
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
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
            'date': order['date'],
            'time': order['time'],
            'duration': order['duration'],
            'amount_paid': order['amount'],
            'payment_id': payment_id,
            'order_id': order_id,
            'status': 'scheduled',
            'created_at': datetime.utcnow(),
            'notes': ''
        }
        
        result = db.appointments.insert_one(appointment)
        
        return jsonify({
            'success': True,
            'message': 'Payment verified successfully',
            'appointment_id': str(result.inserted_id)
        }), 200
        
    except Exception as e:
        print(f"❌ Verify payment error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@payment_bp.route('/payment-status/<order_id>', methods=['GET', 'OPTIONS'])
def payment_status(order_id):
    """
    Check payment status
    GET /api/payment/payment-status/<order_id>
    """
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        db = current_app.config['DB']
        
        order = db.payment_orders.find_one({'razorpay_order_id': order_id})
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        order['_id'] = str(order['_id'])
        if 'counsellor_id' in order:
            order['counsellor_id'] = str(order['counsellor_id'])
        if 'student_id' in order:
            order['student_id'] = str(order['student_id'])
        
        return jsonify(order), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@payment_bp.route('/my-bookings', methods=['GET', 'OPTIONS'])
def my_bookings():
    """
    Get user's bookings (requires authentication)
    GET /api/payment/my-bookings
    Headers: Authorization: Bearer <token>
    """
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        db = current_app.config['DB']
        
        # Get user from token (implement your auth logic)
        # user_id = get_user_from_token()
        
        # For now, get from query param
        user_id = request.args.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        # Get appointments
        appointments = list(db.appointments.find({'student_id': ObjectId(user_id)}))
        
        for apt in appointments:
            apt['_id'] = str(apt['_id'])
            apt['student_id'] = str(apt['student_id'])
            apt['counsellor_id'] = str(apt['counsellor_id'])
        
        return jsonify({'appointments': appointments}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500