import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Form, Button, Alert, Container, Row, Col, Card } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';
import '../assets/css/Auth.css';

function RegisterCounsellor() {
  const navigate = useNavigate();
  const { register } = useAuth();

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    phone: '',
    specialization: '',
    experience: '',
    education: '',
    bio: '',
    agreeToTerms: false
  });

  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState('');

  const specializations = [
    'Career Counselling',
    'Engineering Guidance',
    'Medical Career Advice',
    'Business & Management',
    'Arts & Humanities',
    'Science & Research',
    'IT & Technology',
    'General Counselling'
  ];

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors({ ...errors, [name]: '' });
    }
  };

  const validateForm = () => {
    const newErrors = {};

    // Name validation
    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    } else if (formData.name.trim().length < 3) {
      newErrors.name = 'Name must be at least 3 characters';
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!emailRegex.test(formData.email)) {
      newErrors.email = 'Invalid email format';
    }

    // Phone validation
    if (!formData.phone.trim()) {
      newErrors.phone = 'Phone number is required';
    } else if (formData.phone.length < 10) {
      newErrors.phone = 'Phone number must be at least 10 digits';
    }

    // Specialization validation
    if (!formData.specialization) {
      newErrors.specialization = 'Specialization is required';
    }

    // Experience validation
    if (!formData.experience.trim()) {
      newErrors.experience = 'Experience is required';
    }

    // Education validation
    if (!formData.education.trim()) {
      newErrors.education = 'Education qualification is required';
    }

    // Password validation
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    // Confirm password validation
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    // Terms validation
    if (!formData.agreeToTerms) {
      newErrors.agreeToTerms = 'You must agree to the terms and conditions';
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

    setLoading(true);

    try {
      // Register as counsellor with additional profile data
      await register({
        name: formData.name,
        email: formData.email,
        password: formData.password,
        role: 'counsellor',
        phone: formData.phone,
        profile: {
          specialization: formData.specialization,
          experience: formData.experience,
          education: formData.education,
          bio: formData.bio
        }
      });

      // Success - redirect to dashboard
      navigate('/dashboard');
    } catch (error) {
      setApiError(error.response?.data?.error || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
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
                  <h2 className="mb-2">Register as Counsellor</h2>
                  <p className="text-muted">Join us to guide students in their career journey</p>
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
                    <Form.Control
                      type="text"
                      name="name"
                      value={formData.name}
                      onChange={handleChange}
                      isInvalid={!!errors.name}
                      placeholder="Dr. Jane Smith"
                    />
                    <Form.Control.Feedback type="invalid">
                      {errors.name}
                    </Form.Control.Feedback>
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label>Email Address *</Form.Label>
                    <Form.Control
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      isInvalid={!!errors.email}
                      placeholder="jane.smith@example.com"
                    />
                    <Form.Control.Feedback type="invalid">
                      {errors.email}
                    </Form.Control.Feedback>
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label>Phone Number *</Form.Label>
                    <Form.Control
                      type="tel"
                      name="phone"
                      value={formData.phone}
                      onChange={handleChange}
                      isInvalid={!!errors.phone}
                      placeholder="1234567890"
                    />
                    <Form.Control.Feedback type="invalid">
                      {errors.phone}
                    </Form.Control.Feedback>
                  </Form.Group>

                  {/* Professional Information */}
                  <h5 className="mb-3 mt-4 text-primary">Professional Information</h5>

                  <Form.Group className="mb-3">
                    <Form.Label>Specialization *</Form.Label>
                    <Form.Select
                      name="specialization"
                      value={formData.specialization}
                      onChange={handleChange}
                      isInvalid={!!errors.specialization}
                    >
                      <option value="">Select your specialization</option>
                      {specializations.map((spec, index) => (
                        <option key={index} value={spec}>{spec}</option>
                      ))}
                    </Form.Select>
                    <Form.Control.Feedback type="invalid">
                      {errors.specialization}
                    </Form.Control.Feedback>
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label>Years of Experience *</Form.Label>
                    <Form.Control
                      type="text"
                      name="experience"
                      value={formData.experience}
                      onChange={handleChange}
                      isInvalid={!!errors.experience}
                      placeholder="e.g., 5 years"
                    />
                    <Form.Control.Feedback type="invalid">
                      {errors.experience}
                    </Form.Control.Feedback>
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label>Education Qualification *</Form.Label>
                    <Form.Control
                      type="text"
                      name="education"
                      value={formData.education}
                      onChange={handleChange}
                      isInvalid={!!errors.education}
                      placeholder="e.g., M.A. in Psychology"
                    />
                    <Form.Control.Feedback type="invalid">
                      {errors.education}
                    </Form.Control.Feedback>
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label>Bio (Optional)</Form.Label>
                    <Form.Control
                      as="textarea"
                      rows={3}
                      name="bio"
                      value={formData.bio}
                      onChange={handleChange}
                      placeholder="Tell students about yourself and your expertise..."
                    />
                  </Form.Group>

                  {/* Security */}
                  <h5 className="mb-3 mt-4 text-primary">Security</h5>

                  <Form.Group className="mb-3">
                    <Form.Label>Password *</Form.Label>
                    <Form.Control
                      type="password"
                      name="password"
                      value={formData.password}
                      onChange={handleChange}
                      isInvalid={!!errors.password}
                      placeholder="At least 6 characters"
                    />
                    <Form.Control.Feedback type="invalid">
                      {errors.password}
                    </Form.Control.Feedback>
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label>Confirm Password *</Form.Label>
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
                          <Link to="/terms">Terms & Conditions</Link> and{' '}
                          <Link to="/privacy">Privacy Policy</Link>
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
                    disabled={loading}
                  >
                    {loading ? 'Creating Account...' : 'Register as Counsellor'}
                  </Button>
                </Form>

                <div className="text-center mt-4">
                  <p className="mb-2">
                    Already have an account?{' '}
                    <Link to="/login">Login here</Link>
                  </p>
                  <p className="text-muted">
                    Are you a student?{' '}
                    <Link to="/register">Register as Student</Link>
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

export default RegisterCounsellor;