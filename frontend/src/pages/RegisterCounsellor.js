import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

function RegisterCounsellor() {
  const navigate = useNavigate();
  const { login } = useAuth(); // This updates auth context

  const [formData, setFormData] = useState({
    name: '',
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    phone: '',
    specialization: '',
    experience: '',
    education: '',
    bio: '',
    hourly_rate: '500'
  });

  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [usernameAvailable, setUsernameAvailable] = useState(null);
  const [emailAvailable, setEmailAvailable] = useState(null);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

  // Validate password strength
  const validatePassword = (password) => {
    const minLength = 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

    if (password.length < minLength) {
      return 'Password must be at least 8 characters long';
    }
    if (!hasUpperCase) {
      return 'Password must contain at least one uppercase letter';
    }
    if (!hasLowerCase) {
      return 'Password must contain at least one lowercase letter';
    }
    if (!hasNumber) {
      return 'Password must contain at least one number';
    }
    if (!hasSpecialChar) {
      return 'Password must contain at least one special character (!@#$%^&*(),.?":{}|<>)';
    }
    return null;
  };

  // Check username availability
  const checkUsername = async (username) => {
    if (username.length < 3) {
      setUsernameAvailable(null);
      return;
    }

    try {
      const response = await axios.post(`${API_URL}/auth/check-username`, { username });
      setUsernameAvailable(response.data.available);
    } catch (error) {
      console.error('Error checking username:', error);
    }
  };

  // Check email availability
  const checkEmail = async (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setEmailAvailable(null);
      return;
    }

    try {
      const response = await axios.post(`${API_URL}/auth/check-email`, { email });
      setEmailAvailable(response.data.available);
    } catch (error) {
      console.error('Error checking email:', error);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    
    // Update form data
    setFormData(prevData => ({
      ...prevData,
      [name]: value
    }));
    
    // Clear error for this field
    setErrors(prevErrors => ({
      ...prevErrors,
      [name]: ''
    }));

    // Real-time validation
    if (name === 'username') {
      checkUsername(value);
    }
    if (name === 'email') {
      checkEmail(value);
    }
    if (name === 'password') {
      const passwordError = validatePassword(value);
      if (passwordError) {
        setErrors(prevErrors => ({ ...prevErrors, password: passwordError }));
      }
    }
    if (name === 'confirmPassword') {
      if (value !== formData.password) {
        setErrors(prevErrors => ({ ...prevErrors, confirmPassword: 'Passwords do not match' }));
      }
    }
  };

  const validateForm = () => {
    const newErrors = {};

    // Required fields
    if (!formData.name.trim()) newErrors.name = 'Name is required';
    if (!formData.username.trim()) newErrors.username = 'Username is required';
    if (!formData.email.trim()) newErrors.email = 'Email is required';
    if (!formData.password) newErrors.password = 'Password is required';
    if (!formData.confirmPassword) newErrors.confirmPassword = 'Please confirm password';
    if (!formData.phone.trim()) newErrors.phone = 'Phone number is required';
    if (!formData.specialization || formData.specialization === '') {
      newErrors.specialization = 'Specialization is required';
    }
    if (!formData.experience) newErrors.experience = 'Experience is required';
    if (!formData.education.trim()) newErrors.education = 'Education is required';

    // Validation rules
    if (formData.username.length < 3) {
      newErrors.username = 'Username must be at least 3 characters';
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      newErrors.email = 'Invalid email format';
    }

    // Password validation
    const passwordError = validatePassword(formData.password);
    if (passwordError) {
      newErrors.password = passwordError;
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    // Phone validation
    const phoneRegex = /^[0-9]{10}$/;
    if (!phoneRegex.test(formData.phone.replace(/\s/g, ''))) {
      newErrors.phone = 'Phone number must be 10 digits';
    }

    // Experience validation
    if (formData.experience < 0 || formData.experience > 50) {
      newErrors.experience = 'Experience must be between 0 and 50 years';
    }

    // Check availability
    if (usernameAvailable === false) {
      newErrors.username = 'Username is already taken';
    }
    if (emailAvailable === false) {
      newErrors.email = 'Email is already registered';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    console.log('Form submitted with data:', formData);

    if (!validateForm()) {
      console.log('Validation failed:', errors);
      return;
    }

    setLoading(true);

    try {
      const payload = {
        name: formData.name,
        username: formData.username,
        email: formData.email,
        password: formData.password,
        role: 'counsellor',
        phone: formData.phone,
        profile: {
          specialization: formData.specialization,
          experience: parseInt(formData.experience),
          education: formData.education,
          bio: formData.bio,
          hourly_rate: parseInt(formData.hourly_rate),
          rating: 4.5,
          sessions_conducted: 0
        }
      };

      console.log('Sending to backend:', payload);

      const response = await axios.post(`${API_URL}/auth/register`, payload);

      console.log('Registration response:', response.data);

      // Store token and user data
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      localStorage.setItem('user_id', response.data.user.id);
      localStorage.setItem('user_name', response.data.user.name);
      localStorage.setItem('user_email', response.data.user.email);
      localStorage.setItem('user_role', response.data.user.role);
      
      // Update auth context - THIS IS CRITICAL!
      login(response.data.user, response.data.token);

      console.log('✅ Auth context updated, navigating to dashboard...');

      alert('✅ Registration successful! Welcome to AI Career Counselling.');
      
      // Navigate to dashboard
      navigate('/dashboard');

    } catch (error) {
      console.error('Registration error:', error);
      
      if (error.response?.data?.error) {
        alert('❌ ' + error.response.data.error);
      } else {
        alert('❌ Registration failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5 mb-5">
      <div className="row justify-content-center">
        <div className="col-lg-8">
          <div className="card shadow-sm">
            <div className="card-body p-5">
              {/* Header */}
              <div className="text-center mb-4">
                <h2 className="fw-bold">👨‍🏫 Counsellor Registration</h2>
                <p className="text-muted">Join our platform to help students achieve their career goals</p>
              </div>

              <form onSubmit={handleSubmit}>
                {/* Personal Information */}
                <h5 className="mb-3 text-primary">Personal Information</h5>

                {/* Name */}
                <div className="mb-3">
                  <label className="form-label">Full Name *</label>
                  <input
                    type="text"
                    className={`form-control ${errors.name ? 'is-invalid' : ''}`}
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="Dr. John Smith"
                  />
                  {errors.name && <div className="invalid-feedback">{errors.name}</div>}
                </div>

                {/* Username */}
                <div className="mb-3">
                  <label className="form-label">Username *</label>
                  <input
                    type="text"
                    className={`form-control ${errors.username ? 'is-invalid' : usernameAvailable === true ? 'is-valid' : ''}`}
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    placeholder="johnsmith"
                  />
                  {errors.username && <div className="invalid-feedback">{errors.username}</div>}
                  {usernameAvailable === true && (
                    <div className="valid-feedback">Username is available!</div>
                  )}
                  {usernameAvailable === false && (
                    <div className="invalid-feedback d-block">Username is already taken</div>
                  )}
                </div>

                {/* Email & Phone */}
                <div className="row">
                  <div className="col-md-6 mb-3">
                    <label className="form-label">Email *</label>
                    <input
                      type="email"
                      className={`form-control ${errors.email ? 'is-invalid' : emailAvailable === true ? 'is-valid' : ''}`}
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      placeholder="john@example.com"
                    />
                    {errors.email && <div className="invalid-feedback">{errors.email}</div>}
                    {emailAvailable === true && (
                      <div className="valid-feedback">Email is available!</div>
                    )}
                    {emailAvailable === false && (
                      <div className="invalid-feedback d-block">Email is already registered</div>
                    )}
                  </div>
                  <div className="col-md-6 mb-3">
                    <label className="form-label">Phone Number *</label>
                    <input
                      type="tel"
                      className={`form-control ${errors.phone ? 'is-invalid' : ''}`}
                      name="phone"
                      value={formData.phone}
                      onChange={handleChange}
                      placeholder="9876543210"
                    />
                    {errors.phone && <div className="invalid-feedback">{errors.phone}</div>}
                  </div>
                </div>

                {/* Password */}
                <div className="row">
                  <div className="col-md-6 mb-3">
                    <label className="form-label">Password *</label>
                    <input
                      type="password"
                      className={`form-control ${errors.password ? 'is-invalid' : ''}`}
                      name="password"
                      value={formData.password}
                      onChange={handleChange}
                      placeholder="••••••••"
                    />
                    {errors.password && <div className="invalid-feedback">{errors.password}</div>}
                    <small className="text-muted">
                      Must be 8+ characters with uppercase, lowercase, number, and special character
                    </small>
                  </div>
                  <div className="col-md-6 mb-3">
                    <label className="form-label">Confirm Password *</label>
                    <input
                      type="password"
                      className={`form-control ${errors.confirmPassword ? 'is-invalid' : ''}`}
                      name="confirmPassword"
                      value={formData.confirmPassword}
                      onChange={handleChange}
                      placeholder="••••••••"
                    />
                    {errors.confirmPassword && (
                      <div className="invalid-feedback">{errors.confirmPassword}</div>
                    )}
                  </div>
                </div>

                <hr className="my-4" />

                {/* Professional Information */}
                <h5 className="mb-3 text-primary">Professional Information</h5>

                {/* Specialization & Experience */}
                <div className="row">
                  <div className="col-md-6 mb-3">
                    <label className="form-label">Specialization *</label>
                    <select
                      className={`form-select ${errors.specialization ? 'is-invalid' : formData.specialization ? 'is-valid' : ''}`}
                      name="specialization"
                      value={formData.specialization}
                      onChange={handleChange}
                    >
                      <option value="">Select specialization</option>
                      <option value="Career Guidance">Career Guidance</option>
                      <option value="Technology">Technology Careers</option>
                      <option value="Medical">Medical Careers</option>
                      <option value="Business">Business & Management</option>
                      <option value="Engineering">Engineering</option>
                      <option value="Arts & Design">Arts & Design</option>
                      <option value="Science">Science & Research</option>
                    </select>
                    {errors.specialization && (
                      <div className="invalid-feedback">{errors.specialization}</div>
                    )}
                    {formData.specialization && !errors.specialization && (
                      <div className="valid-feedback">Selected: {formData.specialization}</div>
                    )}
                  </div>
                  <div className="col-md-6 mb-3">
                    <label className="form-label">Years of Experience *</label>
                    <input
                      type="number"
                      className={`form-control ${errors.experience ? 'is-invalid' : ''}`}
                      name="experience"
                      value={formData.experience}
                      onChange={handleChange}
                      min="0"
                      max="50"
                      placeholder="5"
                    />
                    {errors.experience && (
                      <div className="invalid-feedback">{errors.experience}</div>
                    )}
                  </div>
                </div>

                {/* Education */}
                <div className="mb-3">
                  <label className="form-label">Education *</label>
                  <input
                    type="text"
                    className={`form-control ${errors.education ? 'is-invalid' : ''}`}
                    name="education"
                    value={formData.education}
                    onChange={handleChange}
                    placeholder="Ph.D. in Psychology, M.Ed. in Career Counseling"
                  />
                  {errors.education && <div className="invalid-feedback">{errors.education}</div>}
                </div>

                {/* Hourly Rate */}
                <div className="mb-3">
                  <label className="form-label">Hourly Rate (₹) *</label>
                  <input
                    type="number"
                    className="form-control"
                    name="hourly_rate"
                    value={formData.hourly_rate}
                    onChange={handleChange}
                    min="100"
                    max="10000"
                    step="50"
                  />
                  <small className="text-muted">Your consultation fee per hour</small>
                </div>

                {/* Bio */}
                <div className="mb-3">
                  <label className="form-label">Professional Bio</label>
                  <textarea
                    className="form-control"
                    name="bio"
                    value={formData.bio}
                    onChange={handleChange}
                    rows="4"
                    placeholder="Tell students about your experience, approach, and how you can help them..."
                  />
                  <small className="text-muted">Optional - Appears on your profile</small>
                </div>

                {/* Submit Button */}
                <div className="d-grid gap-2 mt-4">
                  <button
                    type="submit"
                    className="btn btn-primary btn-lg"
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2"></span>
                        Registering...
                      </>
                    ) : (
                      'Register as Counsellor'
                    )}
                  </button>
                </div>

                {/* Login Link */}
                <div className="text-center mt-3">
                  <p className="text-muted mb-0">
                    Already have an account?{' '}
                    <a href="/login" className="text-primary fw-bold">
                      Login here
                    </a>
                  </p>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default RegisterCounsellor;