import React, { useState, useEffect } from 'react';
import axios from 'axios';
import PaymentButton from '../components/PaymentButton';
import { useNavigate } from 'react-router-dom';

function CounsellorDirectory() {
  const navigate = useNavigate(); // ADD THIS LINE - Initialize navigate
  const [counsellors, setCounsellors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterSpecialization, setFilterSpecialization] = useState('all');

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

  useEffect(() => {
    fetchCounsellors();
  }, []);

  const fetchCounsellors = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/counsellors`);
      
      console.log('Counsellors response:', response.data);
      
      setCounsellors(response.data.counsellors || []);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching counsellors:', err);
      setError(err.message);
      setLoading(false);
    }
  };

  const handleBookingSuccess = (data) => {
    console.log('Booking successful:', data);
    alert(`✅ Booking confirmed! Appointment ID: ${data.appointment_id}`);
    // You can redirect to bookings page or show confirmation modal
  };

  // Filter counsellors
  const filteredCounsellors = counsellors.filter(counsellor => {
    const matchesSearch = counsellor.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesSpecialization = filterSpecialization === 'all' || 
      counsellor.profile?.specialization?.toLowerCase().includes(filterSpecialization.toLowerCase());
    return matchesSearch && matchesSpecialization;
  });

  if (loading) {
    return (
      <div className="container mt-5 text-center">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p className="mt-3">Loading counsellors...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-5">
        <div className="alert alert-danger">
          <h4>Error loading counsellors</h4>
          <p>{error}</p>
          <button className="btn btn-primary" onClick={fetchCounsellors}>
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-5 mb-5">
      {/* Header */}
      <div className="text-center mb-5">
        <h1 className="display-4 fw-bold mb-3" style={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text'
        }}>
          👨‍🏫 Expert Counsellors
        </h1>
        <p className="lead text-muted">
          Book a session with experienced career counsellors
        </p>
      </div>

      {/* Search & Filter */}
      <div className="row mb-4">
        <div className="col-md-6 mb-3">
          <input
            type="text"
            className="form-control form-control-lg"
            placeholder="🔍 Search counsellors..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{
              borderRadius: '10px',
              border: '2px solid #e0e0e0'
            }}
          />
        </div>
        <div className="col-md-6 mb-3">
          <select
            className="form-select form-select-lg"
            value={filterSpecialization}
            onChange={(e) => setFilterSpecialization(e.target.value)}
            style={{
              borderRadius: '10px',
              border: '2px solid #e0e0e0'
            }}
          >
            <option value="all">All Specializations</option>
            <option value="career">Career Guidance</option>
            <option value="technology">Technology</option>
            <option value="medical">Medical</option>
            <option value="business">Business</option>
            <option value="engineering">Engineering</option>
          </select>
        </div>
      </div>

      {/* Counsellors Grid */}
      {filteredCounsellors.length === 0 ? (
        <div className="alert alert-info text-center">
          <h4>😔 No counsellors found</h4>
          <p className="mb-0">
            {counsellors.length === 0 
              ? 'No counsellors available at the moment. Please check back later.'
              : 'Try adjusting your search or filters.'}
          </p>
        </div>
      ) : (
        <div className="row">
          {filteredCounsellors.map((counsellor) => (
            <div key={counsellor._id} className="col-lg-4 col-md-6 mb-4">
              <div className="card h-100 shadow-sm" style={{
                borderRadius: '12px',
                border: 'none',
                transition: 'all 0.3s ease'
              }}>
                <div className="card-body" style={{ padding: '1.5rem' }}>
                  {/* Profile Picture */}
                  <div className="text-center mb-3">
                    <div className="bg-primary text-white rounded-circle d-inline-flex align-items-center justify-content-center" 
                         style={{
                           width: '80px', 
                           height: '80px', 
                           fontSize: '2rem',
                           fontWeight: 'bold'
                         }}>
                      {counsellor.name.charAt(0)}
                    </div>
                  </div>

                  {/* Name */}
                  <h5 className="card-title text-center mb-2">{counsellor.name}</h5>

                  {/* Specialization */}
                  <p className="text-center text-muted mb-3">
                    <span className="badge bg-light text-dark">
                      {counsellor.profile?.specialization || 'Career Counsellor'}
                    </span>
                  </p>

                  {/* Stats */}
                  <div className="row text-center mb-3">
                    <div className="col-6">
                      <div className="border-end">
                        <h6 className="mb-0 text-primary">
                          {counsellor.profile?.experience || 0}+ years
                        </h6>
                        <small className="text-muted">Experience</small>
                      </div>
                    </div>
                    <div className="col-6">
                      <h6 className="mb-0 text-warning">
                        ⭐ {counsellor.profile?.rating || 4.5}/5
                      </h6>
                      <small className="text-muted">Rating</small>
                    </div>
                  </div>

                  {/* Education */}
                  {counsellor.profile?.education && (
                    <p className="small mb-2">
                      <strong>🎓 Education:</strong> {counsellor.profile.education}
                    </p>
                  )}

                  {/* Bio */}
                  <p className="small text-muted mb-3" style={{minHeight: '60px'}}>
                    {counsellor.profile?.bio || 'Experienced career counsellor dedicated to helping students achieve their goals.'}
                  </p>

                  {/* Sessions Conducted */}
                  <p className="small text-center mb-3">
                    <span className="badge bg-success">
                      {counsellor.profile?.sessions_conducted || 0} sessions conducted
                    </span>
                  </p>

                  {/* Price */}
                  <div className="text-center mb-3">
                    <h4 className="text-primary mb-0">
                      ₹{counsellor.profile?.hourly_rate || 500}
                      <small className="text-muted">/hour</small>
                    </h4>
                  </div>

                  {/* Payment Button */}
                  <PaymentButton 
                    counsellor={counsellor}
                    onSuccess={handleBookingSuccess}
                  />

                  {/* View Profile Link */}
                  <div className="text-center mt-2">
                    <button 
                      className="btn btn-link btn-sm text-muted"
                      onClick={() => navigate(`/counsellors/${counsellor._id}`)}
                    >
                      View Full Profile →
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Info Box */}
      <div className="alert alert-info mt-5" style={{
        background: 'linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%)',
        border: 'none',
        borderRadius: '12px'
      }}>
        <h5 className="alert-heading">💡 How it works</h5>
        <ol className="mb-0">
          <li>Choose a counsellor based on their specialization</li>
          <li>Click "Book Session" and complete payment</li>
          <li>You'll receive confirmation via email</li>
          <li>Counsellor will contact you to schedule the session</li>
        </ol>
      </div>

      {/* Stats */}
      <div className="text-center mt-4 text-muted">
        <p className="mb-0">
          Showing {filteredCounsellors.length} of {counsellors.length} counsellors
        </p>
      </div>
    </div>
  );
}

export default CounsellorDirectory;