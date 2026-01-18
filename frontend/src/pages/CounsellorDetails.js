import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import PaymentButton from '../components/PaymentButton';

function CounsellorDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [counsellor, setCounsellor] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

  useEffect(() => {
    fetchCounsellorDetails();
  }, [id]);

  const fetchCounsellorDetails = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/counsellors/${id}`);
      setCounsellor(response.data);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching counsellor:', err);
      setError(err.message);
      setLoading(false);
    }
  };

  const handleBookingSuccess = (data) => {
    alert(`✅ Booking confirmed! Appointment ID: ${data.appointment_id}`);
    navigate('/dashboard');
  };

  if (loading) {
    return (
      <div className="container mt-5 text-center">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  if (error || !counsellor) {
    return (
      <div className="container mt-5">
        <div className="alert alert-danger">
          <h4>Error loading counsellor details</h4>
          <p>{error}</p>
          <button className="btn btn-primary" onClick={() => navigate('/counsellors')}>
            Back to Counsellors
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-5 mb-5">
      {/* Back Button */}
      <button 
        className="btn btn-outline-secondary mb-4"
        onClick={() => navigate('/counsellors')}
      >
        ← Back to Counsellors
      </button>

      <div className="row">
        {/* Left Column - Profile Info */}
        <div className="col-lg-4 mb-4">
          <div className="card shadow-sm" style={{ borderRadius: '12px', border: 'none' }}>
            <div className="card-body text-center p-4">
              {/* Profile Picture */}
              <div className="bg-primary text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3" 
                   style={{
                     width: '120px', 
                     height: '120px', 
                     fontSize: '3rem',
                     fontWeight: 'bold'
                   }}>
                {counsellor.name.charAt(0)}
              </div>

              <h3 className="mb-2">{counsellor.name}</h3>
              <p className="text-muted mb-3">{counsellor.email}</p>

              <div className="badge bg-light text-dark mb-3" style={{ fontSize: '1rem' }}>
                {counsellor.specialization || counsellor.profile?.specialization || 'Career Counsellor'}
              </div>

              {/* Rating */}
              <div className="mb-3">
                <h4 className="text-warning mb-0">
                  ⭐ {counsellor.rating || counsellor.profile?.rating || 4.5}/5
                </h4>
                <small className="text-muted">
                  Based on {counsellor.sessions_conducted || counsellor.profile?.sessions_conducted || 0} sessions
                </small>
              </div>

              {/* Price */}
              <div className="mb-4">
                <h2 className="text-primary mb-0">
                  ₹{counsellor.hourly_rate || counsellor.profile?.hourly_rate || 500}
                  <small className="text-muted" style={{ fontSize: '1rem' }}>/hour</small>
                </h2>
              </div>

              {/* Book Button */}
              <PaymentButton 
                counsellor={counsellor}
                onSuccess={handleBookingSuccess}
              />
            </div>
          </div>
        </div>

        {/* Right Column - Details */}
        <div className="col-lg-8">
          {/* About Section */}
          <div className="card shadow-sm mb-4" style={{ borderRadius: '12px', border: 'none' }}>
            <div className="card-body p-4">
              <h4 className="mb-3">👨‍🏫 About</h4>
              <p className="text-muted">
                {counsellor.bio || counsellor.profile?.bio || 
                 'Experienced career counsellor dedicated to helping students achieve their career goals through personalized guidance and support.'}
              </p>
            </div>
          </div>

          {/* Experience & Education */}
          <div className="row mb-4">
            <div className="col-md-6 mb-3">
              <div className="card shadow-sm h-100" style={{ borderRadius: '12px', border: 'none' }}>
                <div className="card-body p-4">
                  <h5 className="mb-3">💼 Experience</h5>
                  <h3 className="text-primary">
                    {counsellor.experience || counsellor.profile?.experience || 5}+ years
                  </h3>
                  <p className="text-muted mb-0">Professional counselling experience</p>
                </div>
              </div>
            </div>
            <div className="col-md-6 mb-3">
              <div className="card shadow-sm h-100" style={{ borderRadius: '12px', border: 'none' }}>
                <div className="card-body p-4">
                  <h5 className="mb-3">🎓 Education</h5>
                  <p className="mb-0">
                    {counsellor.education || counsellor.profile?.education || 'MA in Psychology'}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Specializations */}
          <div className="card shadow-sm mb-4" style={{ borderRadius: '12px', border: 'none' }}>
            <div className="card-body p-4">
              <h4 className="mb-3">🎯 Specializations</h4>
              <div className="d-flex flex-wrap gap-2">
                <span className="badge bg-primary" style={{ fontSize: '0.9rem', padding: '0.5rem 1rem' }}>
                  {counsellor.specialization || counsellor.profile?.specialization || 'Career Guidance'}
                </span>
                <span className="badge bg-secondary" style={{ fontSize: '0.9rem', padding: '0.5rem 1rem' }}>
                  Student Counselling
                </span>
                <span className="badge bg-success" style={{ fontSize: '0.9rem', padding: '0.5rem 1rem' }}>
                  Academic Planning
                </span>
              </div>
            </div>
          </div>

          {/* Contact Info */}
          {counsellor.phone && (
            <div className="card shadow-sm" style={{ borderRadius: '12px', border: 'none' }}>
              <div className="card-body p-4">
                <h4 className="mb-3">📞 Contact Information</h4>
                <p className="mb-2">
                  <strong>Email:</strong> {counsellor.email}
                </p>
                <p className="mb-0">
                  <strong>Phone:</strong> {counsellor.phone}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default CounsellorDetails;