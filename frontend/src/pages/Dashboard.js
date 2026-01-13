import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Card, Button, ProgressBar, Badge, ListGroup } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  FaComments, 
  FaClipboardCheck, 
  FaBriefcase, 
  FaUniversity,
  FaChartLine,
  FaTrophy,
  FaClock
} from 'react-icons/fa';
import '../assets/css/Dashboard.css';

const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    profileComplete: 65,
    quizCompleted: false,
    chatSessions: 3,
    recommendationsReceived: false,
  });

  const recentActivities = [
    { id: 1, text: 'Completed personality quiz', time: '2 days ago', icon: FaClipboardCheck, color: 'success' },
    { id: 2, text: 'Chat session with AI counselor', time: '5 days ago', icon: FaComments, color: 'primary' },
    { id: 3, text: 'Viewed Software Engineer career', time: '1 week ago', icon: FaBriefcase, color: 'warning' },
  ];

  const quickActions = [
    {
      title: 'Chat with AI',
      description: 'Get personalized career guidance',
      icon: FaComments,
      color: 'primary',
      link: '/chat',
      buttonText: 'Start Chat'
    },
    {
      title: 'Take Quiz',
      description: 'Assess your aptitude & personality',
      icon: FaClipboardCheck,
      color: 'success',
      link: '/quiz/aptitude',
      buttonText: 'Take Quiz'
    },
    {
      title: 'Explore Careers',
      description: 'Browse career options',
      icon: FaBriefcase,
      color: 'warning',
      link: '/careers',
      buttonText: 'View Careers'
    },
    {
      title: 'Find Colleges',
      description: 'Discover best colleges for you',
      icon: FaUniversity,
      color: 'info',
      link: '/colleges',
      buttonText: 'Find Colleges'
    },
  ];

  return (
    <div className="dashboard-page">
      <Container className="py-5">
        {/* Welcome Section */}
        <Row className="mb-4">
          <Col>
            <h2 className="display-6 fw-bold">
              Welcome back, {user?.name}! 👋
            </h2>
            <p className="text-muted">Here's your career journey progress</p>
          </Col>
        </Row>

        {/* Stats Cards */}
        <Row className="mb-4 g-4">
          <Col md={3}>
            <Card className="stats-card border-0 shadow-sm h-100">
              <Card.Body>
                <div className="d-flex align-items-center">
                  <div className="stats-icon bg-primary-light">
                    <FaChartLine className="text-primary" size={24} />
                  </div>
                  <div className="ms-3">
                    <h3 className="mb-0">{stats.profileComplete}%</h3>
                    <small className="text-muted">Profile Complete</small>
                  </div>
                </div>
              </Card.Body>
            </Card>
          </Col>

          <Col md={3}>
            <Card className="stats-card border-0 shadow-sm h-100">
              <Card.Body>
                <div className="d-flex align-items-center">
                  <div className="stats-icon bg-success-light">
                    <FaComments className="text-success" size={24} />
                  </div>
                  <div className="ms-3">
                    <h3 className="mb-0">{stats.chatSessions}</h3>
                    <small className="text-muted">Chat Sessions</small>
                  </div>
                </div>
              </Card.Body>
            </Card>
          </Col>

          <Col md={3}>
            <Card className="stats-card border-0 shadow-sm h-100">
              <Card.Body>
                <div className="d-flex align-items-center">
                  <div className="stats-icon bg-warning-light">
                    <FaClipboardCheck className="text-warning" size={24} />
                  </div>
                  <div className="ms-3">
                    <h3 className="mb-0">{stats.quizCompleted ? '2' : '0'}</h3>
                    <small className="text-muted">Quizzes Taken</small>
                  </div>
                </div>
              </Card.Body>
            </Card>
          </Col>

          <Col md={3}>
            <Card className="stats-card border-0 shadow-sm h-100">
              <Card.Body>
                <div className="d-flex align-items-center">
                  <div className="stats-icon bg-info-light">
                    <FaTrophy className="text-info" size={24} />
                  </div>
                  <div className="ms-3">
                    <h3 className="mb-0">{stats.recommendationsReceived ? '5' : '0'}</h3>
                    <small className="text-muted">Recommendations</small>
                  </div>
                </div>
              </Card.Body>
            </Card>
          </Col>
        </Row>

        {/* Profile Completion */}
        <Row className="mb-4">
          <Col>
            <Card className="border-0 shadow-sm">
              <Card.Body>
                <div className="d-flex justify-content-between align-items-center mb-3">
                  <div>
                    <h5 className="mb-1">Complete Your Profile</h5>
                    <small className="text-muted">
                      Complete your profile to get better recommendations
                    </small>
                  </div>
                  <Badge bg="primary" className="fs-6">
                    {stats.profileComplete}%
                  </Badge>
                </div>
                <ProgressBar 
                  now={stats.profileComplete} 
                  variant="primary"
                  className="mb-3"
                  style={{ height: '10px' }}
                />
                <Button as={Link} to="/profile" variant="outline-primary" size="sm">
                  Complete Profile
                </Button>
              </Card.Body>
            </Card>
          </Col>
        </Row>

        {/* Quick Actions */}
        <Row className="mb-4">
          <Col>
            <h4 className="mb-3">Quick Actions</h4>
          </Col>
        </Row>

        <Row className="g-4 mb-4">
          {quickActions.map((action, index) => (
            <Col md={6} lg={3} key={index}>
              <Card className="quick-action-card h-100 text-center border-0 shadow-sm">
                <Card.Body className="p-4">
                  <div className={`action-icon bg-${action.color}-light mb-3`}>
                    <action.icon size={40} className={`text-${action.color}`} />
                  </div>
                  <h5>{action.title}</h5>
                  <p className="text-muted small mb-3">{action.description}</p>
                  <Button 
                    as={Link} 
                    to={action.link} 
                    variant={action.color}
                    size="sm"
                    className="w-100"
                  >
                    {action.buttonText}
                  </Button>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>

        {/* Recent Activity */}
        <Row>
          <Col lg={8}>
            <Card className="border-0 shadow-sm">
              <Card.Header className="bg-white border-bottom">
                <h5 className="mb-0">Recent Activity</h5>
              </Card.Header>
              <Card.Body className="p-0">
                <ListGroup variant="flush">
                  {recentActivities.map((activity) => (
                    <ListGroup.Item key={activity.id} className="py-3">
                      <div className="d-flex align-items-center">
                        <div className={`activity-icon bg-${activity.color}-light me-3`}>
                          <activity.icon className={`text-${activity.color}`} />
                        </div>
                        <div className="flex-grow-1">
                          <p className="mb-0">{activity.text}</p>
                          <small className="text-muted">
                            <FaClock className="me-1" />
                            {activity.time}
                          </small>
                        </div>
                      </div>
                    </ListGroup.Item>
                  ))}
                </ListGroup>
              </Card.Body>
            </Card>
          </Col>

          {/* Next Steps */}
          <Col lg={4}>
            <Card className="border-0 shadow-sm">
              <Card.Header className="bg-white border-bottom">
                <h5 className="mb-0">Next Steps</h5>
              </Card.Header>
              <Card.Body>
                <ListGroup variant="flush" className="border-0">
                  <ListGroup.Item className="px-0 border-0">
                    <div className="form-check">
                      <input 
                        className="form-check-input" 
                        type="checkbox" 
                        checked={stats.profileComplete === 100}
                        readOnly
                      />
                      <label className="form-check-label">
                        Complete your profile
                      </label>
                    </div>
                  </ListGroup.Item>
                  <ListGroup.Item className="px-0 border-0">
                    <div className="form-check">
                      <input 
                        className="form-check-input" 
                        type="checkbox"
                        checked={stats.quizCompleted}
                        readOnly
                      />
                      <label className="form-check-label">
                        Take aptitude quiz
                      </label>
                    </div>
                  </ListGroup.Item>
                  <ListGroup.Item className="px-0 border-0">
                    <div className="form-check">
                      <input 
                        className="form-check-input" 
                        type="checkbox"
                        checked={stats.chatSessions > 0}
                        readOnly
                      />
                      <label className="form-check-label">
                        Chat with AI counselor
                      </label>
                    </div>
                  </ListGroup.Item>
                  <ListGroup.Item className="px-0 border-0">
                    <div className="form-check">
                      <input 
                        className="form-check-input" 
                        type="checkbox"
                        checked={stats.recommendationsReceived}
                        readOnly
                      />
                      <label className="form-check-label">
                        Get career recommendations
                      </label>
                    </div>
                  </ListGroup.Item>
                </ListGroup>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default Dashboard;