import React, { useState } from 'react';
import axios from 'axios';

const PaymentButton = ({ counsellor, onSuccess }) => {
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [date, setDate] = useState('');
  const [time, setTime] = useState('');
  const [duration, setDuration] = useState(1);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

  const handleBooking = async () => {
  if (!date || !time) {
    alert('Please select date and time');
    return;
  }

  setLoading(true);

  try {
    const token = localStorage.getItem('token');
    
    console.log('📍 Booking Details:');
    console.log('API URL:', API_URL);
    console.log('Token exists:', !!token);
    console.log('Counsellor ID:', counsellor._id || counsellor.id);
    console.log('Date:', date);
    console.log('Time:', time);
    
    if (!token) {
      alert('Please login to book a session');
      window.location.href = '/login';
      return;
    }

    const bookingData = {
      counsellor_id: counsellor._id || counsellor.id,
      appointment_date: date,
      appointment_time: time,
      duration: duration * 60,
      notes: 'Booking via web app',
      amount: counsellor.profile?.hourly_rate || counsellor.hourly_rate || 500
    };

    console.log('📤 Sending booking data:', bookingData);

    const response = await axios.post(
      `${API_URL}/appointments`,
      bookingData,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    );

    console.log('✅ Booking response:', response.data);

    setLoading(false);
    setShowModal(false);
    
    if (onSuccess) {
      onSuccess(response.data);
    } else {
      alert(`✅ Booking confirmed! Appointment ID: ${response.data.appointment_id}`);
    }
  } catch (error) {
    setLoading(false);
    
    console.error('❌ Booking error:', error);
    console.error('Error response:', error.response?.data);
    console.error('Error status:', error.response?.status);
    
    let errorMessage = 'Booking failed: ';
    
    if (error.response) {
      // Backend responded with error
      errorMessage += error.response.data?.error || error.response.statusText;
    } else if (error.request) {
      // Request made but no response
      errorMessage += 'No response from server. Is the backend running?';
    } else {
      // Error setting up request
      errorMessage += error.message;
    }
    
    alert(errorMessage);
  }
};
  // Get minimum date (today)
  const getMinDate = () => {
    const today = new Date();
    return today.toISOString().split('T')[0];
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
        💳 Book Session
      </button>

      {/* Booking Modal */}
      {showModal && (
        <div 
          className="modal show d-block" 
          style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}
          onClick={() => setShowModal(false)}
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
                ></button>
              </div>
              <div className="modal-body p-4">
                {/* Date Selection */}
                <div className="mb-3">
                  <label className="form-label fw-bold">Select Date</label>
                  <input
                    type="date"
                    className="form-control"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                    min={getMinDate()}
                    required
                  />
                </div>

                {/* Time Selection */}
                <div className="mb-3">
                  <label className="form-label fw-bold">Select Time</label>
                  <select
                    className="form-select"
                    value={time}
                    onChange={(e) => setTime(e.target.value)}
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
                  >
                    <option value="1">1 hour</option>
                    <option value="2">2 hours</option>
                  </select>
                </div>

                {/* Price Summary */}
                <div className="alert alert-info" style={{ background: '#e3f2fd' }}>
                  <h6 className="mb-2">💰 Price Summary</h6>
                  <p className="mb-1">
                    <strong>Rate:</strong> ₹{counsellor.profile?.hourly_rate || counsellor.hourly_rate || 500}/hour
                  </p>
                  <p className="mb-0">
                    <strong>Total:</strong> ₹{(counsellor.profile?.hourly_rate || counsellor.hourly_rate || 500) * duration}
                  </p>
                </div>

                {/* Note */}
                <p className="text-muted small mb-0">
                  ℹ️ Counsellor will contact you via email to confirm the session.
                </p>
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
                  className="btn btn-primary"
                  onClick={handleBooking}
                  disabled={loading || !date || !time}
                >
                  {loading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2"></span>
                      Processing...
                    </>
                  ) : (
                    '✅ Confirm Booking'
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