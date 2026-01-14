import React, { useState } from 'react';
import axios from 'axios';

const PaymentButton = ({ counsellor, onSuccess }) => {
  const [loading, setLoading] = useState(false);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

  const handlePayment = async () => {
    setLoading(true);

    try {
      // Step 1: Create order on backend
      const orderResponse = await axios.post(`${API_URL}/payment/create-order`, {
        counsellor_id: counsellor._id,
        date: '2026-01-20', // Get from date picker
        time: '10:00',      // Get from time picker
        duration: 1,         // 1 hour session
        amount: counsellor.profile.hourly_rate || 500
      });

      const { order_id, amount, currency, key_id } = orderResponse.data;

      // Step 2: Open Razorpay checkout
      const options = {
        key: key_id,
        amount: amount,
        currency: currency,
        name: 'AI Career Counselling',
        description: `Session with ${counsellor.name}`,
        order_id: order_id,
        handler: async function (response) {
          // Step 3: Verify payment on backend
          try {
            const verifyResponse = await axios.post(`${API_URL}/payment/verify-payment`, {
              razorpay_order_id: response.razorpay_order_id,
              razorpay_payment_id: response.razorpay_payment_id,
              razorpay_signature: response.razorpay_signature
            });

            if (verifyResponse.data.success) {
              alert('Payment successful! Your session is booked.');
              if (onSuccess) onSuccess(verifyResponse.data);
            }
          } catch (error) {
            console.error('Verification error:', error);
            alert('Payment verification failed. Please contact support.');
          }
        },
        prefill: {
          name: 'Student Name',
          email: 'student@example.com',
          contact: '9999999999'
        },
        theme: {
          color: '#6366f1'
        },
        modal: {
          ondismiss: function() {
            setLoading(false);
          }
        }
      };

      const razorpay = new window.Razorpay(options);
      razorpay.open();
      setLoading(false);

    } catch (error) {
      console.error('Payment error:', error);
      alert('Failed to initiate payment. Please try again.');
      setLoading(false);
    }
  };

  return (
    <button 
      className="btn btn-primary"
      onClick={handlePayment}
      disabled={loading}
    >
      {loading ? (
        <>
          <span className="spinner-border spinner-border-sm me-2"></span>
          Processing...
        </>
      ) : (
        <>
          💳 Pay ₹{counsellor.profile?.hourly_rate || 500}/hour
        </>
      )}
    </button>
  );
};

export default PaymentButton;