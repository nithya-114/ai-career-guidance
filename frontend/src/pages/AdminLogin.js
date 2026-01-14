import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

function AdminLogin() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post(`${API_URL}/auth/login`, {
        login: formData.username,
        password: formData.password
      });

      // Check if user is actually an admin
      if (response.data.user.role !== 'admin') {
        setError('Access denied. Admin credentials required.');
        setLoading(false);
        return;
      }

      // Store admin data
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      
      // Update auth context
      login(response.data.user, response.data.token);

      // Redirect to admin dashboard
      navigate('/dashboard');

    } catch (err) {
      console.error('Admin login error:', err);
      setError(err.response?.data?.error || 'Invalid admin credentials');
      setLoading(false);
    }
  };

  return (
    <div className="min-vh-100 d-flex align-items-center" style={{
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    }}>
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-md-5">
            <div className="card shadow-lg border-0">
              <div className="card-body p-5">
                {/* Header */}
                <div className="text-center mb-4">
                  <div className="mb-3">
                    <i className="bi bi-shield-lock-fill text-danger" style={{ fontSize: '3rem' }}></i>
                  </div>
                  <h3 className="fw-bold">Admin Login</h3>
                  <p className="text-muted">Access Control Panel</p>
                </div>

                {/* Error Alert */}
                {error && (
                  <div className="alert alert-danger alert-dismissible fade show" role="alert">
                    <i className="bi bi-exclamation-triangle-fill me-2"></i>
                    {error}
                    <button 
                      type="button" 
                      className="btn-close" 
                      onClick={() => setError('')}
                    ></button>
                  </div>
                )}

                {/* Login Form */}
                <form onSubmit={handleSubmit}>
                  {/* Username */}
                  <div className="mb-3">
                    <label className="form-label fw-bold">
                      <i className="bi bi-person-badge me-2"></i>
                      Admin Username
                    </label>
                    <input
                      type="text"
                      className="form-control form-control-lg"
                      name="username"
                      value={formData.username}
                      onChange={handleChange}
                      placeholder="Enter admin username"
                      required
                      autoFocus
                    />
                  </div>

                  {/* Password */}
                  <div className="mb-4">
                    <label className="form-label fw-bold">
                      <i className="bi bi-key-fill me-2"></i>
                      Password
                    </label>
                    <input
                      type="password"
                      className="form-control form-control-lg"
                      name="password"
                      value={formData.password}
                      onChange={handleChange}
                      placeholder="Enter password"
                      required
                    />
                  </div>

                  {/* Submit Button */}
                  <button
                    type="submit"
                    className="btn btn-danger btn-lg w-100 mb-3"
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2"></span>
                        Verifying...
                      </>
                    ) : (
                      <>
                        <i className="bi bi-shield-lock-fill me-2"></i>
                        Login to Admin Panel
                      </>
                    )}
                  </button>
                </form>

                {/* Security Notice */}
                <div className="alert alert-warning mt-4 mb-0" role="alert">
                  <small>
                    <i className="bi bi-info-circle-fill me-2"></i>
                    <strong>Security Notice:</strong> This area is restricted to authorized administrators only. 
                    All login attempts are logged.
                  </small>
                </div>

                {/* Back to Home */}
                <div className="text-center mt-3">
                  <a href="/" className="text-muted small">
                    <i className="bi bi-arrow-left me-1"></i>
                    Back to Home
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AdminLogin;