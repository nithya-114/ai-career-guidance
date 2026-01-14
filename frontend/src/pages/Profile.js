import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';

function Profile() {
  const { user } = useAuth();
  const [profileData, setProfileData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState({});

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/user/profile`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      console.log('Profile data received:', response.data);
      setProfileData(response.data);
      setFormData(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching profile:', error);
      setLoading(false);
    }
  };

  const getRoleBadgeClass = () => {
    const role = profileData?.role || user?.role || 'student';
    switch(role) {
      case 'counsellor': return 'bg-success';
      case 'admin': return 'bg-danger';
      default: return 'bg-primary';
    }
  };

  const getRoleDisplay = () => {
    const role = profileData?.role || user?.role || 'student';
    return role.charAt(0).toUpperCase() + role.slice(1);
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ minHeight: '80vh' }}>
        <div className="spinner-border text-primary"></div>
      </div>
    );
  }

  const role = profileData?.role || user?.role || 'student';

  return (
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-lg-10">
          {/* Header Card */}
          <div className="card shadow-sm mb-4">
            <div className="card-body p-4">
              <div className="row align-items-center">
                <div className="col-md-8">
                  <div className="d-flex align-items-center">
                    <div className="me-4">
                      <div className="rounded-circle d-flex align-items-center justify-content-center"
                        style={{
                          width: '100px', height: '100px',
                          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                          color: 'white', fontSize: '2.5rem', fontWeight: 'bold'
                        }}>
                        {profileData?.name?.charAt(0).toUpperCase()}
                      </div>
                    </div>
                    <div>
                      <h2 className="mb-1">{profileData?.name}</h2>
                      <p className="text-muted mb-2">{profileData?.email}</p>
                      <span className={`badge ${getRoleBadgeClass()}`}>{getRoleDisplay()}</span>
                    </div>
                  </div>
                </div>
                <div className="col-md-4 text-md-end mt-3 mt-md-0">
                  <h3>43%</h3>
                  <p className="text-muted small">Profile Complete</p>
                </div>
              </div>
            </div>
          </div>

          {/* Details Card */}
          <div className="card shadow-sm">
            <div className="card-body p-4">
              <div className="d-flex justify-content-between mb-4">
                <h4>Personal Information</h4>
                <button className="btn btn-primary">
                  <i className="bi bi-pencil me-2"></i>Edit Profile
                </button>
              </div>

              <div className="row">
                <div className="col-md-6 mb-3">
                  <label className="form-label fw-bold">
                    <i className="bi bi-person me-2"></i>Full Name
                  </label>
                  <input type="text" className="form-control" value={profileData?.name || ''} disabled />
                </div>

                <div className="col-md-6 mb-3">
                  <label className="form-label fw-bold">
                    <i className="bi bi-envelope me-2"></i>Email Address
                  </label>
                  <input type="email" className="form-control" value={profileData?.email || ''} disabled />
                </div>

                {role === 'counsellor' && (
                  <>
                    <div className="col-md-6 mb-3">
                      <label className="form-label fw-bold">
                        <i className="bi bi-phone me-2"></i>Phone Number
                      </label>
                      <input type="tel" className="form-control" value={profileData?.phone || ''} disabled />
                    </div>

                    <div className="col-md-6 mb-3">
                      <label className="form-label fw-bold">
                        <i className="bi bi-geo-alt me-2"></i>Location
                      </label>
                      <input type="text" className="form-control" value={profileData?.location || 'City, State'} disabled />
                    </div>

                    <div className="col-12"><hr/><h5 className="mb-3">Professional Details</h5></div>

                    <div className="col-md-6 mb-3">
                      <label className="form-label fw-bold">Specialization</label>
                      <input type="text" className="form-control" value={profileData?.profile?.specialization || ''} disabled />
                    </div>

                    <div className="col-md-6 mb-3">
                      <label className="form-label fw-bold">Experience</label>
                      <input type="text" className="form-control" value={`${profileData?.profile?.experience || 0} years`} disabled />
                    </div>

                    <div className="col-md-6 mb-3">
                      <label className="form-label fw-bold">Education</label>
                      <input type="text" className="form-control" value={profileData?.profile?.education || ''} disabled />
                    </div>

                    <div className="col-md-6 mb-3">
                      <label className="form-label fw-bold">Hourly Rate</label>
                      <input type="text" className="form-control" value={`₹${profileData?.profile?.hourly_rate || 0}/hour`} disabled />
                    </div>

                    <div className="col-12 mb-3">
                      <label className="form-label fw-bold">Bio</label>
                      <textarea className="form-control" rows="3" value={profileData?.profile?.bio || 'No bio added yet'} disabled />
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Profile;