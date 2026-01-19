import React, { useState, useEffect } from 'react';
import { counsellorAPI, paymentAPI } from '../services/api';
import { useNavigate } from 'react-router-dom';
import '../assets/css/BookCounsellor.css';

const BookCounsellor = () => {
  const [counsellors, setCounsellors] = useState([]);
  const [selectedCounsellor, setSelectedCounsellor] = useState(null);
  const [bookingDate, setBookingDate] = useState('');
  const [bookingTime, setBookingTime] = useState('');
  const [duration, setDuration] = useState(1);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetchCounsellors();
    loadRazorpayScript();
  }, []);

  const loadRazorpayScript = () => {
    return new Promise((resolve) => {
      const script = document.createElement('script');
      script.src = 'https://checkout.razorpay.com/v1/checkout.js';
      script.onload = () => resolve(true);
      script.onerror = () => resolve(false);
      document.body.appendChild(script);
    });
  };

  const fetchCounsellors = async () => {
    try {
      const response = await counsellorAPI.getAll();
      setCounsellors(response.data.counsellors || []);
    } catch (error) {
      console.error('Error fetching counsellors:', error);
      alert('Failed to load counsellors');
    }
  };

  const handleBooking = async (counsellor) => {
    setSelectedCounsellor(counsellor);
  };

  const handlePayment = async (e) => {
    e.preventDefault();

    if (!bookingDate || !bookingTime) {
      alert('Please select date and time');
      return;
    }

    setLoading(true);

    try {
      const amount = selectedCounsellor.hourly_rate * duration;

      // Step 1: Create order
      console.log('Creating order...');
      const orderResponse = await paymentAPI.createOrder({
        counsellor_id: selectedCounsellor.id,
        date: bookingDate,
        time: bookingTime,
        duration: duration,
        amount: amount
      });

      const { order_id, amount: orderAmount, key_id } = orderResponse.data;
      console.log('Order created:', order_id);

      // Step 2: Get user details
      const user = JSON.parse(localStorage.getItem('user'));

      // Step 3: Open Razorpay checkout
      const options = {
        key: key_id,
        amount: orderAmount,
        currency: "INR",
        name: "Career Counselling Platform",
        description: `Session with ${selectedCounsellor.name}`,
        order_id: order_id,
        handler: async function (response) {
          console.log('Payment successful:', response);

          // Step 4: Verify payment
          try {
            const verifyResponse = await paymentAPI.verifyPayment({
              razorpay_order_id: response.razorpay_order_id,
              razorpay_payment_id: response.razorpay_payment_id,
              razorpay_signature: response.razorpay_signature
            });

            if (verifyResponse.data.success) {
              alert('✅ Payment successful! Appointment booked.');
              navigate('/my-appointments');
            }
          } catch (error) {
            console.error('Verification error:', error);
            alert('❌ Payment verification failed. Please contact support.');
          }
        },
        prefill: {
          name: user?.name || '',
          email: user?.email || '',
          contact: user?.phone || ''
        },
        theme: {
          color: "#3399cc"
        },
        modal: {
          ondismiss: function() {
            console.log('Payment cancelled');
            setLoading(false);
          }
        }
      };

      const rzp = new window.Razorpay(options);
      
      rzp.on('payment.failed', function (response) {
        console.error('Payment failed:', response.error);
        alert(`Payment failed: ${response.error.description}`);
        setLoading(false);
      });

      rzp.open();
      setLoading(false);

    } catch (error) {
      console.error('Payment error:', error);
      alert(error.response?.data?.error || 'Payment failed. Please try again.');
      setLoading(false);
    }
  };

  return (
    <div className="book-counsellor-container">
      <h1>Book a Counsellor</h1>

      {!selectedCounsellor ? (
        <div className="counsellors-grid">
          {counsellors.map((counsellor) => (
            <div key={counsellor.id} className="counsellor-card">
              <h3>{counsellor.name}</h3>
              <p className="specialization">{counsellor.specialization}</p>
              <p className="experience">Experience: {counsellor.experience}</p>
              <p className="rating">⭐ {counsellor.rating}/5</p>
              <p className="rate">₹{counsellor.hourly_rate}/hour</p>
              <button 
                onClick={() => handleBooking(counsellor)}
                className="book-btn"
              >
                Book Session
              </button>
            </div>
          ))}
        </div>
      ) : (
        <div className="booking-form-container">
          <button 
            onClick={() => setSelectedCounsellor(null)}
            className="back-btn"
          >
            ← Back to Counsellors
          </button>

          <div className="selected-counsellor">
            <h2>Booking with {selectedCounsellor.name}</h2>
            <p>{selectedCounsellor.specialization}</p>
          </div>

          <form onSubmit={handlePayment} className="booking-form">
            <div className="form-group">
              <label>Select Date:</label>
              <input
                type="date"
                value={bookingDate}
                onChange={(e) => setBookingDate(e.target.value)}
                min={new Date().toISOString().split('T')[0]}
                required
              />
            </div>

            <div className="form-group">
              <label>Select Time:</label>
              <input
                type="time"
                value={bookingTime}
                onChange={(e) => setBookingTime(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label>Duration (hours):</label>
              <select 
                value={duration} 
                onChange={(e) => setDuration(Number(e.target.value))}
              >
                <option value={1}>1 hour</option>
                <option value={2}>2 hours</option>
                <option value={3}>3 hours</option>
              </select>
            </div>

            <div className="payment-summary">
              <h3>Payment Summary</h3>
              <p>Rate: ₹{selectedCounsellor.hourly_rate}/hour</p>
              <p>Duration: {duration} hour(s)</p>
              <p className="total">Total: ₹{selectedCounsellor.hourly_rate * duration}</p>
            </div>

            <button 
              type="submit" 
              className="pay-btn"
              disabled={loading}
            >
              {loading ? 'Processing...' : 'Proceed to Payment'}
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default BookCounsellor;