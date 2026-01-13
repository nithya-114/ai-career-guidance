import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Form, Button, Alert, Container, Row, Col, Card, InputGroup } from 'react-bootstrap';
import { FaUser, FaLock, FaEnvelope } from 'react-icons/fa';
import { useAuth } from '../context/AuthContext';
import '../assets/css/Auth.css';

function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [formData, setFormData] = useState({
    login: '',  // Can be username or email
    password: ''
  });

  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });

    // Clear errors when user types
    if (errors[name]) {
      setErrors({ ...errors, [name]: '' });
    }
    if (apiError) {
      setApiError('');
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.login.trim()) {
      newErrors.login = 'Username or email is required';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
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
      await login({
        login: formData.login,
        password: formData.password
      });

      // Redirect to dashboard
      navigate('/dashboard');
    } catch (error) {
      const errorMsg = error.response?.data?.error || 'Login failed. Please try again.';
      setApiError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <Container>
        <Row className="justify-content-center">
          <Col md={6} lg={5}>
            <Card className="auth-card">
              <Card.Body className="p-5">
                <div className="text-center mb-4">
                  <h2 className="mb-2">Welcome Back</h2>
                  <p className="text-muted">Login to continue your career journey</p>
                </div>

                {apiError && (
                  <Alert variant="danger" dismissible onClose={() => setApiError('')}>
                    {apiError}
                  </Alert>
                )}

                <Form onSubmit={handleSubmit}>
                  <Form.Group className="mb-3">
                    <Form.Label>Username or Email</Form.Label>
                    <InputGroup>
                      <InputGroup.Text>
                        <FaUser />
                      </InputGroup.Text>
                      <Form.Control
                        type="text"
                        name="login"
                        value={formData.login}
                        onChange={handleChange}
                        isInvalid={!!errors.login}
                        placeholder="Enter username or email"
                        autoComplete="username"
                      />
                      <Form.Control.Feedback type="invalid">
                        {errors.login}
                      </Form.Control.Feedback>
                    </InputGroup>
                    <Form.Text className="text-muted">
                      You can login with either your username or email
                    </Form.Text>
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label>Password</Form.Label>
                    <InputGroup>
                      <InputGroup.Text>
                        <FaLock />
                      </InputGroup.Text>
                      <Form.Control
                        type="password"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                        isInvalid={!!errors.password}
                        placeholder="Enter your password"
                        autoComplete="current-password"
                      />
                      <Form.Control.Feedback type="invalid">
                        {errors.password}
                      </Form.Control.Feedback>
                    </InputGroup>
                  </Form.Group>

                  <div className="d-flex justify-content-between align-items-center mb-4">
                    <Form.Check
                      type="checkbox"
                      label="Remember me"
                      id="rememberMe"
                    />
                    <Link to="/forgot-password" className="text-primary">
                      Forgot password?
                    </Link>
                  </div>

                  <Button
                    variant="primary"
                    type="submit"
                    className="w-100 auth-btn mb-3"
                    disabled={loading}
                  >
                    {loading ? 'Logging in...' : 'Login'}
                  </Button>

                  <div className="text-center">
                    <p className="mb-0">
                      Don't have an account?{' '}
                      <Link to="/register">Register as Student</Link>
                      {' or '}
                      <Link to="/register-counsellor">Register as Counsellor</Link>
                    </p>
                  </div>
                </Form>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default Login;