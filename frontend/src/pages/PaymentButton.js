import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PaymentButton = ({ counsellor, onSuccess }) => {
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [date, setDate] = useState('');
  const [time, setTime] = useState('');
  const [duration, setDuration] = useState(1);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

  // Load Razorpay script
  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://checkout.razorpay.com/v1/checkout.js';
    script.async = true;
    document.body.appendChild(script);

    return () => {
      if (document.body.contains(script)) {
        document.body.removeChild(script);
      }
    };
  }, []);

  const handleBooking = async () => {
    if (!date || !time) {
      alert('Please select date and time');
      return;
    }

    setLoading(true);

    try {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('user_id');

      console.log('🔐 Auth Check:');
      console.log('Token exists:', !!token);
      console.log('User ID:', userId);

      if (!token) {
        alert('Please login to book a session');
        window.location.href = '/login';
        return;
      }

      // Calculate total amount
      const hourlyRate = counsellor.profile?.hourly_rate || counsellor.hourly_rate || 500;
      const totalAmount = hourlyRate * duration;

      const orderData = {
        counsellor_id: counsellor._id || counsellor.id,
        student_id: userId,
        date: date,
        time: time,
        duration: duration,
        amount: totalAmount
      };

      console.log('📤 Creating payment order:', orderData);

      // Create Razorpay order
      const response = await axios.post(
        `${API_URL}/payment/create-order`,
        orderData,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      console.log('✅ Order created:', response.data);

      const { order_id, amount, currency, key_id } = response.data;

      // Configure Razorpay options
      const options = {
        key: key_id,
        amount: amount,
        currency: currency,
        order_id: order_id,
        name: 'Career Counselling Platform',
        description: `Session with ${counsellor.name}`,
        image: '/logo192.png',
        handler: async (paymentResponse) => {
          await verifyPayment(paymentResponse);
        },
        prefill: {
          name: localStorage.getItem('user_name') || '',
          email: localStorage.getItem('user_email') || '',
        },
        theme: {
          color: '#0d6efd'
        },
        modal: {
          ondismiss: () => {
            setLoading(false);
            console.log('Payment cancelled by user');
          }
        }
      };

      // Open Razorpay payment modal
      const rzp = new window.Razorpay(options);
      rzp.open();

    } catch (error) {
      setLoading(false);

      console.error('❌ Booking error:', error);
      console.error('Error response:', error.response?.data);
      console.error('Error status:', error.response?.status);

      let errorMessage = 'Booking failed: ';

      if (error.response) {
        errorMessage += error.response.data?.error || error.response.statusText;
      } else if (error.request) {
        errorMessage += 'No response from server. Is the backend running?';
      } else {
        errorMessage += error.message;
      }

      alert(errorMessage);
    }
  };

  const verifyPayment = async (paymentResponse) => {
    try {
      console.log('🔍 Verifying payment:', paymentResponse);

      const token = localStorage.getItem('token');

      const verifyData = {
        razorpay_order_id: paymentResponse.razorpay_order_id,
        razorpay_payment_id: paymentResponse.razorpay_payment_id,
        razorpay_signature: paymentResponse.razorpay_signature
      };

      const response = await axios.post(
        `${API_URL}/payment/verify-payment`,
        verifyData,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      console.log('✅ Payment verified:', response.data);

      setLoading(false);
      setShowModal(false);

      // Success!
      alert(`✅ Booking successful! Appointment ID: ${response.data.appointment_id}\n\nCounsellor will contact you via email.`);

      if (onSuccess) {
        onSuccess(response.data);
      }

    } catch (error) {
      console.error('❌ Payment verification error:', error);
      setLoading(false);

      alert('Payment verification failed. Please contact support with your payment ID.');
    }
  };

  // Get minimum date (tomorrow)
  const getMinDate = () => {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    return tomorrow.toISOString().split('T')[0];
  };

  // Calculate total price
  const calculateTotal = () => {
    const hourlyRate = counsellor.profile?.hourly_rate || counsellor.hourly_rate || 500;
    return hourlyRate * duration;
  };

  return (
    <>
      <button
        className="btn btn-primary w-100"
        onClick={() => setShowModal(true)}
        style={{
          borderRadius: '8px',
          padding: '12px',
          fontWeight: '600'
        }}
      >
        📅 Book Session
      </button>

      {/* Booking Modal */}
      {showModal && (
        <div
          className="modal show d-block"
          style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}
          onClick={() => !loading && setShowModal(false)}
        >
          <div
            className="modal-dialog modal-dialog-centered"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="modal-content" style={{ borderRadius: '12px' }}>
              <div className="modal-header" style={{ borderBottom: '2px solid #f0f0f0' }}>
                <h5 className="modal-title">📅 Book Session with {counsellor.name}</h5>
                <button
                  type="button"
                  className="btn-close"
                  onClick={() => setShowModal(false)}
                  disabled={loading}
                ></button>
              </div>

              <div className="modal-body p-4">
                {/* Counsellor Info Card */}
                <div className="card mb-3 bg-light">
                  <div className="card-body py-2">
                    <div className="d-flex justify-content-between align-items-center">
                      <div>
                        <strong>{counsellor.name}</strong>
                        <br />
                        <small className="text-muted">
                          {counsellor.profile?.specialization || counsellor.specialization}
                        </small>
                      </div>
                      <div className="text-end">
                        <span className="badge bg-primary">
                          ⭐ {counsellor.rating || 4.5}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Date Selection */}
                <div className="mb-3">
                  <label className="form-label fw-bold">
                    Select Date <span className="text-danger">*</span>
                  </label>
                  <input
                    type="date"
                    className="form-control"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                    min={getMinDate()}
                    disabled={loading}
                    required
                  />
                  <small className="text-muted">Minimum booking: 1 day in advance</small>
                </div>

                {/* Time Selection */}
                <div className="mb-3">
                  <label className="form-label fw-bold">
                    Select Time <span className="text-danger">*</span>
                  </label>
                  <select
                    className="form-select"
                    value={time}
                    onChange={(e) => setTime(e.target.value)}
                    disabled={loading}
                    required
                  >
                    <option value="">Choose time slot</option>
                    <option value="09:00">09:00 AM</option>
                    <option value="10:00">10:00 AM</option>
                    <option value="11:00">11:00 AM</option>
                    <option value="12:00">12:00 PM</option>
                    <option value="14:00">02:00 PM</option>
                    <option value="15:00">03:00 PM</option>
                    <option value="16:00">04:00 PM</option>
                    <option value="17:00">05:00 PM</option>
                  </select>
                </div>

                {/* Duration Selection */}
                <div className="mb-3">
                  <label className="form-label fw-bold">Duration</label>
                  <select
                    className="form-select"
                    value={duration}
                    onChange={(e) => setDuration(parseInt(e.target.value))}
                    disabled={loading}
                  >
                    <option value="1">1 hour</option>
                    <option value="2">2 hours</option>
                  </select>
                </div>

                {/* Price Summary */}
                <div className="card bg-primary bg-opacity-10 border-primary">
                  <div className="card-body">
                    <h6 className="card-title mb-3">💰 Price Summary</h6>
                    <div className="d-flex justify-content-between mb-2">
                      <span>Hourly Rate:</span>
                      <strong>₹{counsellor.profile?.hourly_rate || counsellor.hourly_rate || 500}</strong>
                    </div>
                    <div className="d-flex justify-content-between mb-2">
                      <span>Duration:</span>
                      <strong>{duration} hour(s)</strong>
                    </div>
                    <hr />
                    <div className="d-flex justify-content-between">
                      <strong className="fs-5">Total:</strong>
                      <strong className="fs-5 text-primary">₹{calculateTotal()}</strong>
                    </div>
                  </div>
                </div>

                {/* Info Note */}
                <div className="alert alert-info mt-3 mb-0">
                  <small>
                    ℹ️ <strong>Next Steps:</strong>
                    <ul className="mb-0 mt-2 ps-3">
                      <li>Complete payment securely via Razorpay</li>
                      <li>Counsellor will confirm via email</li>
                      <li>Meeting link will be shared before session</li>
                    </ul>
                  </small>
                </div>
              </div>

              <div className="modal-footer" style={{ borderTop: '2px solid #f0f0f0' }}>
                <button
                  className="btn btn-secondary"
                  onClick={() => setShowModal(false)}
                  disabled={loading}
                >
                  Cancel
                </button>
                <button
                  className="btn btn-primary px-4"
                  onClick={handleBooking}
                  disabled={loading || !date || !time}
                >
                  {loading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2"></span>
                      Processing...
                    </>
                  ) : (
                    <>
                      💳 Proceed to Payment
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default PaymentButton;