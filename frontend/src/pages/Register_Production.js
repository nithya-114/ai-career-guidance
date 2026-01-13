import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Form, Button, Alert, Container, Row, Col, Card, InputGroup } from 'react-bootstrap';
import { FaUser, FaEnvelope, FaLock, FaCalendar, FaSchool, FaGraduationCap, FaMapMarkerAlt } from 'react-icons/fa';
import { useAuth } from '../context/AuthContext';
import '../assets/css/Auth.css';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function Register() {
  const navigate = useNavigate();
  const { register } = useAuth();

  const [formData, setFormData] = useState({
    name: '',
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    dob: '',
    class_level: '',
    school: '',
    location: '',
    agreeToTerms: false
  });

  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState('');
  const [passwordStrength, setPasswordStrength] = useState('');
  const [usernameAvailable, setUsernameAvailable] = useState(null);
  const [checkingUsername, setCheckingUsername] = useState(false);

  const classLevels = [
    '8th Grade',
    '9th Grade',
    '10th Grade',
    '11th Grade (Science)',
    '11th Grade (Commerce)',
    '11th Grade (Arts)',
    '12th Grade (Science)',
    '12th Grade (Commerce)',
    '12th Grade (Arts)',
    'Undergraduate Year 1',
    'Undergraduate Year 2',
    'Undergraduate Year 3',
    'Undergraduate Year 4',
    'Postgraduate',
    'Other'
  ];

  const checkPasswordStrength = (password) => {
    let strength = 'Weak';
    let checks = 0;

    if (password.length >= 8) checks++;
    if (/[A-Z]/.test(password)) checks++;
    if (/[a-z]/.test(password)) checks++;
    if (/\d/.test(password)) checks++;
    if (/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(password)) checks++;

    if (checks >= 5) strength = 'Strong';
    else if (checks >= 3) strength = 'Medium';

    return strength;
  };

  const checkUsernameAvailability = async (username) => {
    if (username.length < 3) return;

    setCheckingUsername(true);
    try {
      const response = await axios.post(`${API_URL}/auth/check-username`, { username });
      setUsernameAvailable(response.data.available);
      if (!response.data.available) {
        setErrors(prev => ({ ...prev, username: response.data.error }));
      } else {
        setErrors(prev => {
          const newErrors = { ...prev };
          delete newErrors.username;
          return newErrors;
        });
      }
    } catch (error) {
      console.error('Username check error:', error);
    } finally {
      setCheckingUsername(false);
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    const newValue = type === 'checkbox' ? checked : value;

    setFormData({
      ...formData,
      [name]: newValue
    });

    // Clear error when user types
    if (errors[name]) {
      setErrors({ ...errors, [name]: '' });
    }

    // Check password strength
    if (name === 'password') {
      setPasswordStrength(checkPasswordStrength(value));
    }

    // Check username availability with debounce
    if (name === 'username' && value.length >= 3) {
      clearTimeout(window.usernameTimeout);
      window.usernameTimeout = setTimeout(() => {
        checkUsernameAvailability(value);
      }, 500);
    }
  };

  const validateForm = () => {
    const newErrors = {};

    // Name validation
    if (!formData.name.trim()) {
      newErrors.name = 'Full name is required';
    } else if (formData.name.trim().length < 3) {
      newErrors.name = 'Name must be at least 3 characters';
    }

    // Username validation
    if (!formData.username.trim()) {
      newErrors.username = 'Username is required';
    } else if (formData.username.length < 3 || formData.username.length > 20) {
      newErrors.username = 'Username must be 3-20 characters';
    } else if (!/^[a-zA-Z][a-zA-Z0-9_-]*$/.test(formData.username)) {
      newErrors.username = 'Username must start with a letter and contain only letters, numbers, underscore, or hyphen';
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!emailRegex.test(formData.email)) {
      newErrors.email = 'Invalid email format';
    }

    // DOB validation
    if (!formData.dob) {
      newErrors.dob = 'Date of birth is required';
    } else {
      const dob = new Date(formData.dob);
      const age = (new Date() - dob) / (365.25 * 24 * 60 * 60 * 1000);
      if (age < 5) {
        newErrors.dob = 'You must be at least 5 years old';
      } else if (age > 100) {
        newErrors.dob = 'Invalid date of birth';
      }
    }

    // Class validation
    if (!formData.class_level) {
      newErrors.class_level = 'Class/Grade is required';
    }

    // School validation
    if (!formData.school.trim()) {
      newErrors.school = 'School name is required';
    }

    // Password validation
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else {
      const passwordErrors = [];
      if (formData.password.length < 8) {
        passwordErrors.push('at least 8 characters');
      }
      if (!/[A-Z]/.test(formData.password)) {
        passwordErrors.push('one uppercase letter');
      }
      if (!/[a-z]/.test(formData.password)) {
        passwordErrors.push('one lowercase letter');
      }
      if (!/\d/.test(formData.password)) {
        passwordErrors.push('one number');
      }
      if (!/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(formData.password)) {
        passwordErrors.push('one special character');
      }

      if (passwordErrors.length > 0) {
        newErrors.password = 'Password must contain: ' + passwordErrors.join(', ');
      }
    }

    // Confirm password validation
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    // Terms validation
    if (!formData.agreeToTerms) {
      newErrors.agreeToTerms = 'You must agree to the terms';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setApiError('');

    if (!validateForm()) {
      return;
    }

    if (usernameAvailable === false) {
      setApiError('Username is already taken');
      return;
    }

    setLoading(true);

    try {
      await register({
        name: formData.name,
        username: formData.username,
        email: formData.email,
        password: formData.password,
        role: 'student',
        dob: formData.dob,
        class_level: formData.class_level,
        school: formData.school,
        location: formData.location
      });

      navigate('/dashboard');
    } catch (error) {
      const errorMsg = error.response?.data?.error || 'Registration failed';
      const errorDetails = error.response?.data?.details;
      
      if (errorDetails && Array.isArray(errorDetails)) {
        setApiError(errorMsg + ': ' + errorDetails.join(', '));
      } else {
        setApiError(errorMsg);
      }
    } finally {
      setLoading(false);
    }
  };

  const getPasswordStrengthColor = () => {
    switch (passwordStrength) {
      case 'Strong': return 'success';
      case 'Medium': return 'warning';
      case 'Weak': return 'danger';
      default: return 'secondary';
    }
  };

  return (
    <div className="auth-page">
      <Container>
        <Row className="justify-content-center">
          <Col md={8} lg={6}>
            <Card className="auth-card">
              <Card.Body className="p-5">
                <div className="text-center mb-4">
                  <h2 className="mb-2">Create Student Account</h2>
                  <p className="text-muted">Start your career discovery journey</p>
                </div>

                {apiError && (
                  <Alert variant="danger" dismissible onClose={() => setApiError('')}>
                    {apiError}
                  </Alert>
                )}

                <Form onSubmit={handleSubmit}>
                  {/* Personal Information */}
                  <h5 className="mb-3 text-primary">Personal Information</h5>

                  <Form.Group className="mb-3">
                    <Form.Label>Full Name *</Form.Label>
                    <InputGroup>
                      <InputGroup.Text><FaUser /></InputGroup.Text>
                      <Form.Control
                        type="text"
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                        isInvalid={!!errors.name}
                        placeholder="John Doe"
                      />
                      <Form.Control.Feedback type="invalid">
                        {errors.name}
                      </Form.Control.Feedback>
                    </InputGroup>
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label>Username * <small className="text-muted">(you can login with this)</small></Form.Label>
                    <InputGroup>
                      <InputGroup.Text><FaUser /></InputGroup.Text>
                      <Form.Control
                        type="text"
                        name="username"
                        value={formData.username}
                        onChange={handleChange}
                        isInvalid={!!errors.username}
                        isValid={usernameAvailable === true && formData.username.length >= 3}
                        placeholder="johndoe123"
                      />
                      {checkingUsername && <InputGroup.Text>Checking...</InputGroup.Text>}
                      {usernameAvailable === true && !checkingUsername && (
                        <InputGroup.Text className="text-success">✓ Available</InputGroup.Text>
                      )}
                      <Form.Control.Feedback type="invalid">
                        {errors.username}
                      </Form.Control.Feedback>
                    </InputGroup>
                    <Form.Text className="text-muted">
                      3-20 characters, start with letter, use letters/numbers/_/-
                    </Form.Text>
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label>Email Address *</Form.Label>
                    <InputGroup>
                      <InputGroup.Text><FaEnvelope /></InputGroup.Text>
                      <Form.Control
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        isInvalid={!!errors.email}
                        placeholder="john@example.com"
                      />
                      <Form.Control.Feedback type="invalid">
                        {errors.email}
                      </Form.Control.Feedback>
                    </InputGroup>
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label>Date of Birth *</Form.Label>
                    <InputGroup>
                      <InputGroup.Text><FaCalendar /></InputGroup.Text>
                      <Form.Control
                        type="date"
                        name="dob"
                        value={formData.dob}
                        onChange={handleChange}
                        isInvalid={!!errors.dob}
                        max={new Date().toISOString().split('T')[0]}
                      />
                      <Form.Control.Feedback type="invalid">
                        {errors.dob}
                      </Form.Control.Feedback>
                    </InputGroup>
                  </Form.Group>

                  {/* Education Information */}
                  <h5 className="mb-3 mt-4 text-primary">Education Details</h5>

                  <Form.Group className="mb-3">
                    <Form.Label>Current Class/Grade *</Form.Label>
                    <InputGroup>
                      <InputGroup.Text><FaGraduationCap /></InputGroup.Text>
                      <Form.Select
                        name="class_level"
                        value={formData.class_level}
                        onChange={handleChange}
                        isInvalid={!!errors.class_level}
                      >
                        <option value="">Select your class/grade</option>
                        {classLevels.map((level, index) => (
                          <option key={index} value={level}>{level}</option>
                        ))}
                      </Form.Select>
                      <Form.Control.Feedback type="invalid">
                        {errors.class_level}
                      </Form.Control.Feedback>
                    </InputGroup>
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label>School/College Name *</Form.Label>
                    <InputGroup>
                      <InputGroup.Text><FaSchool /></InputGroup.Text>
                      <Form.Control
                        type="text"
                        name="school"
                        value={formData.school}
                        onChange={handleChange}
                        isInvalid={!!errors.school}
                        placeholder="ABC High School"
                      />
                      <Form.Control.Feedback type="invalid">
                        {errors.school}
                      </Form.Control.Feedback>
                    </InputGroup>
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label>Location <small className="text-muted">(optional)</small></Form.Label>
                    <InputGroup>
                      <InputGroup.Text><FaMapMarkerAlt /></InputGroup.Text>
                      <Form.Control
                        type="text"
                        name="location"
                        value={formData.location}
                        onChange={handleChange}
                        placeholder="City, State"
                      />
                    </InputGroup>
                  </Form.Group>

                  {/* Security */}
                  <h5 className="mb-3 mt-4 text-primary">Security</h5>

                  <Form.Group className="mb-3">
                    <Form.Label>Password *</Form.Label>
                    <InputGroup>
                      <InputGroup.Text><FaLock /></InputGroup.Text>
                      <Form.Control
                        type="password"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                        isInvalid={!!errors.password}
                        placeholder="Create a strong password"
                      />
                      <Form.Control.Feedback type="invalid">
                        {errors.password}
                      </Form.Control.Feedback>
                    </InputGroup>
                    {formData.password && (
                      <Form.Text className={`text-${getPasswordStrengthColor()}`}>
                        Password strength: <strong>{passwordStrength}</strong>
                      </Form.Text>
                    )}
                    <Form.Text className="text-muted d-block">
                      Must contain: 8+ characters, uppercase, lowercase, number, special character
                    </Form.Text>
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label>Confirm Password *</Form.Label>
                    <InputGroup>
                      <InputGroup.Text><FaLock /></InputGroup.Text>
                      <Form.Control
                        type="password"
                        name="confirmPassword"
                        value={formData.confirmPassword}
                        onChange={handleChange}
                        isInvalid={!!errors.confirmPassword}
                        placeholder="Re-enter your password"
                      />
                      <Form.Control.Feedback type="invalid">
                        {errors.confirmPassword}
                      </Form.Control.Feedback>
                    </InputGroup>
                  </Form.Group>

                  <Form.Group className="mb-4">
                    <Form.Check
                      type="checkbox"
                      name="agreeToTerms"
                      checked={formData.agreeToTerms}
                      onChange={handleChange}
                      isInvalid={!!errors.agreeToTerms}
                      label={
                        <span>
                          I agree to the{' '}
                          <Link to="/terms">Terms & Conditions</Link>
                        </span>
                      }
                      feedback={errors.agreeToTerms}
                      feedbackType="invalid"
                    />
                  </Form.Group>

                  <Button
                    variant="primary"
                    type="submit"
                    className="w-100 auth-btn"
                    disabled={loading || checkingUsername || usernameAvailable === false}
                  >
                    {loading ? 'Creating Account...' : 'Create Student Account'}
                  </Button>
                </Form>

                <div className="text-center mt-4">
                  <p className="mb-2">
                    Already have an account?{' '}
                    <Link to="/login">Login here</Link>
                  </p>
                  <p className="text-muted">
                    Are you a counsellor?{' '}
                    <Link to="/register-counsellor" className="text-primary fw-bold">
                      Register as Counsellor
                    </Link>
                  </p>
                </div>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default Register;