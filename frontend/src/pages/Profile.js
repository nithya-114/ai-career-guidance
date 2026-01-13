import React, { useState } from 'react';
import { Container, Row, Col, Card, Form, Button, Alert, Badge } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';
import { FaUser, FaEnvelope, FaPhone, FaMapMarkerAlt, FaSave, FaEdit } from 'react-icons/fa';
import '../assets/css/Profile.css';

const Profile = () => {
  const { user, updateUserProfile } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });
  const [formData, setFormData] = useState({
    name: user?.name || '',
    email: user?.email || '',
    phone: user?.profile?.phone || '',
    location: user?.profile?.location || '',
    education: user?.profile?.education || '',
    interests: user?.profile?.interests || '',
    goals: user?.profile?.goals || '',
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage({ type: '', text: '' });

    const result = await updateUserProfile({
      phone: formData.phone,
      location: formData.location,
      education: formData.education,
      interests: formData.interests,
      goals: formData.goals,
    });

    if (result.success) {
      setMessage({ type: 'success', text: 'Profile updated successfully!' });
      setIsEditing(false);
    } else {
      setMessage({ type: 'danger', text: result.error });
    }
  };

  const calculateProfileCompletion = () => {
    const fields = [formData.name, formData.email, formData.phone, formData.location, formData.education, formData.interests, formData.goals];
    const filledFields = fields.filter(field => field && field.trim() !== '').length;
    return Math.round((filledFields / fields.length) * 100);
  };

  const profileCompletion = calculateProfileCompletion();

  return (
    <div className="profile-page">
      <Container className="py-5">
        <Row className="justify-content-center">
          <Col lg={8}>
            {/* Profile Header */}
            <Card className="mb-4 border-0 shadow-sm">
              <Card.Body className="p-4">
                <div className="d-flex align-items-center justify-content-between">
                  <div className="d-flex align-items-center">
                    <div className="profile-avatar me-3">
                      <FaUser size={50} className="text-white" />
                    </div>
                    <div>
                      <h3 className="mb-1">{user?.name}</h3>
                      <p className="text-muted mb-0">{user?.email}</p>
                      <Badge bg="primary" className="mt-2">
                        Student
                      </Badge>
                    </div>
                  </div>
                  <div className="text-end">
                    <div className="profile-completion mb-2">
                      <div className="completion-circle">
                        <svg viewBox="0 0 36 36" className="circular-chart">
                          <path className="circle-bg"
                            d="M18 2.0845
                              a 15.9155 15.9155 0 0 1 0 31.831
                              a 15.9155 15.9155 0 0 1 0 -31.831"
                          />
                          <path className="circle"
                            strokeDasharray={`${profileCompletion}, 100`}
                            d="M18 2.0845
                              a 15.9155 15.9155 0 0 1 0 31.831
                              a 15.9155 15.9155 0 0 1 0 -31.831"
                          />
                          <text x="18" y="20.35" className="percentage">{profileCompletion}%</text>
                        </svg>
                      </div>
                    </div>
                    <small className="text-muted">Profile Complete</small>
                  </div>
                </div>
              </Card.Body>
            </Card>

            {/* Profile Form */}
            <Card className="border-0 shadow-sm">
              <Card.Header className="bg-white border-bottom d-flex justify-content-between align-items-center">
                <h5 className="mb-0">Personal Information</h5>
                {!isEditing && (
                  <Button 
                    variant="outline-primary" 
                    size="sm"
                    onClick={() => setIsEditing(true)}
                  >
                    <FaEdit className="me-2" />
                    Edit Profile
                  </Button>
                )}
              </Card.Header>
              <Card.Body className="p-4">
                {message.text && (
                  <Alert variant={message.type} dismissible onClose={() => setMessage({ type: '', text: '' })}>
                    {message.text}
                  </Alert>
                )}

                <Form onSubmit={handleSubmit}>
                  <Row>
                    <Col md={6}>
                      <Form.Group className="mb-3">
                        <Form.Label>
                          <FaUser className="me-2" />
                          Full Name
                        </Form.Label>
                        <Form.Control
                          type="text"
                          name="name"
                          value={formData.name}
                          disabled
                        />
                      </Form.Group>
                    </Col>
                    <Col md={6}>
                      <Form.Group className="mb-3">
                        <Form.Label>
                          <FaEnvelope className="me-2" />
                          Email Address
                        </Form.Label>
                        <Form.Control
                          type="email"
                          name="email"
                          value={formData.email}
                          disabled
                        />
                      </Form.Group>
                    </Col>
                  </Row>

                  <Row>
                    <Col md={6}>
                      <Form.Group className="mb-3">
                        <Form.Label>
                          <FaPhone className="me-2" />
                          Phone Number
                        </Form.Label>
                        <Form.Control
                          type="tel"
                          name="phone"
                          value={formData.phone}
                          onChange={handleChange}
                          placeholder="Enter your phone number"
                          disabled={!isEditing}
                        />
                      </Form.Group>
                    </Col>
                    <Col md={6}>
                      <Form.Group className="mb-3">
                        <Form.Label>
                          <FaMapMarkerAlt className="me-2" />
                          Location
                        </Form.Label>
                        <Form.Control
                          type="text"
                          name="location"
                          value={formData.location}
                          onChange={handleChange}
                          placeholder="City, State"
                          disabled={!isEditing}
                        />
                      </Form.Group>
                    </Col>
                  </Row>

                  <Form.Group className="mb-3">
                    <Form.Label>Current Education</Form.Label>
                    <Form.Select
                      name="education"
                      value={formData.education}
                      onChange={handleChange}
                      disabled={!isEditing}
                    >
                      <option value="">Select your education level</option>
                      <option value="10th">10th Standard</option>
                      <option value="12th">12th Standard</option>
                      <option value="Undergraduate">Undergraduate</option>
                      <option value="Graduate">Graduate</option>
                      <option value="Postgraduate">Postgraduate</option>
                    </Form.Select>
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label>Interests (comma separated)</Form.Label>
                    <Form.Control
                      type="text"
                      name="interests"
                      value={formData.interests}
                      onChange={handleChange}
                      placeholder="e.g., Technology, Art, Science, Sports"
                      disabled={!isEditing}
                    />
                    <Form.Text className="text-muted">
                      Help us understand what you're passionate about
                    </Form.Text>
                  </Form.Group>

                  <Form.Group className="mb-4">
                    <Form.Label>Career Goals</Form.Label>
                    <Form.Control
                      as="textarea"
                      rows={3}
                      name="goals"
                      value={formData.goals}
                      onChange={handleChange}
                      placeholder="What are your career aspirations?"
                      disabled={!isEditing}
                    />
                  </Form.Group>

                  {isEditing && (
                    <div className="d-flex gap-2">
                      <Button variant="primary" type="submit">
                        <FaSave className="me-2" />
                        Save Changes
                      </Button>
                      <Button 
                        variant="secondary" 
                        onClick={() => setIsEditing(false)}
                      >
                        Cancel
                      </Button>
                    </div>
                  )}
                </Form>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default Profile;