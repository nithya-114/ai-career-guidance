import React from 'react';
import { Container, Row, Col, Button, Card } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { FaRobot, FaClipboardCheck, FaBriefcase, FaUniversity, FaArrowRight, FaUserGraduate, FaChalkboardTeacher } from 'react-icons/fa';
import '../assets/css/Home.css';

const Home = () => {
  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero-section">
        <Container>
          <Row className="align-items-center min-vh-75">
            <Col lg={6} className="text-center text-lg-start">
              <h1 className="display-3 fw-bold mb-4">
                Discover Your <span className="text-primary">Perfect Career</span>
              </h1>
              <p className="lead mb-4">
                Get personalized career guidance powered by AI. Take aptitude tests, 
                chat with our intelligent Chatbot, Book counsellor, and find the ideal career path 
                tailored just for you.
              </p>
              
              {/* Updated: Separate buttons for Student and Counsellor */}
              <div className="d-flex flex-column flex-sm-row gap-3 justify-content-center justify-content-lg-start mb-3">
                <Button 
                  as={Link} 
                  to="/register" 
                  variant="primary" 
                  size="lg"
                  className="px-4"
                >
                  <FaUserGraduate className="me-2" />
                  Register as Student
                </Button>
                <Button 
                  as={Link} 
                  to="/register-counsellor" 
                  variant="outline-primary" 
                  size="lg"
                  className="px-4"
                >
                  <FaChalkboardTeacher className="me-2" />
                  Register as Counsellor
                </Button>
              </div>
              
              <div className="d-flex gap-3 justify-content-center justify-content-lg-start">
                <Button 
                  as={Link} 
                  to="/careers" 
                  variant="outline-secondary" 
                  size="md"
                  className="px-4"
                >
                  Explore Careers <FaArrowRight className="ms-2" />
                </Button>
              </div>
            </Col>
            <Col lg={6} className="d-none d-lg-block">
              <div className="hero-image-placeholder">
                <img 
                  src="https://img.freepik.com/free-vector/career-development-concept-illustration_114360-8814.jpg" 
                  alt="Career Guidance" 
                  className="img-fluid rounded"
                />
              </div>
            </Col>
          </Row>
        </Container>
      </section>

      {/* Features Section */}
      <section className="features-section py-5 bg-light">
        <Container>
          <h2 className="text-center mb-5">How It Works</h2>
          <Row className="g-4">
            <Col md={6} lg={3}>
              <Card className="h-100 text-center border-0 shadow-sm hover-card">
                <Card.Body className="p-4">
                  <div className="icon-wrapper mb-3">
                    <FaRobot size={50} className="text-primary" />
                  </div>
                  <Card.Title>AI-Powered Chat</Card.Title>
                  <Card.Text>
                    Have natural conversations with our intelligent chatbot 
                    to discover your interests and strengths.
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>

            <Col md={6} lg={3}>
              <Card className="h-100 text-center border-0 shadow-sm hover-card">
                <Card.Body className="p-4">
                  <div className="icon-wrapper mb-3">
                    <FaClipboardCheck size={50} className="text-success" />
                  </div>
                  <Card.Title>Take Assessments</Card.Title>
                  <Card.Text>
                    Complete aptitude and personality tests designed to 
                    understand your unique profile.
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>

            <Col md={6} lg={3}>
              <Card className="h-100 text-center border-0 shadow-sm hover-card">
                <Card.Body className="p-4">
                  <div className="icon-wrapper mb-3">
                    <FaBriefcase size={50} className="text-warning" />
                  </div>
                  <Card.Title>Get Recommendations</Card.Title>
                  <Card.Text>
                    Receive personalized career suggestions matched to 
                    your skills, interests, and personality.
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>

            <Col md={6} lg={3}>
              <Card className="h-100 text-center border-0 shadow-sm hover-card">
                <Card.Body className="p-4">
                  <div className="icon-wrapper mb-3">
                    <FaUniversity size={50} className="text-info" />
                  </div>
                  <Card.Title>Find Colleges</Card.Title>
                  <Card.Text>
                    Discover the best colleges and courses aligned with 
                    your chosen career path.
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Container>
      </section>

      {/* Why Choose Us Section */}
      <section className="why-choose-section py-5">
        <Container>
          <Row className="align-items-center">
            <Col lg={6} className="mb-4 mb-lg-0">
              <h2 className="mb-4">Why Choose CareerGuide AI?</h2>
              <ul className="feature-list">
                <li className="mb-3">
                  <strong>Personalized Guidance:</strong> AI-driven recommendations 
                  based on your unique profile
                </li>
                <li className="mb-3">
                  <strong>Comprehensive Database:</strong> Access to thousands of 
                  careers, courses, and colleges
                </li>
                <li className="mb-3">
                  <strong>Expert Counselors:</strong> Connect with certified career 
                  counselors for deeper guidance
                </li>
                <li className="mb-3">
                  <strong>24/7 Availability:</strong> Get career advice anytime, 
                  anywhere through our chatbot
                </li>
                <li className="mb-3">
                  <strong>Data-Driven Insights:</strong> Make informed decisions 
                  based on aptitude and personality analysis
                </li>
              </ul>
            </Col>
            <Col lg={6}>
              <Card className="border-0 shadow-lg">
                <Card.Body className="p-5 text-center">
                  <h3 className="mb-4">Ready to Start?</h3>
                  <p className="mb-4">
                    Join thousands of students who have found their perfect career path
                  </p>
                  
                  {/* Updated: Two registration buttons */}
                  <div className="d-grid gap-3">
                    <Button 
                      as={Link} 
                      to="/register" 
                      variant="primary" 
                      size="lg"
                    >
                      <FaUserGraduate className="me-2" />
                      I'm a Student
                    </Button>
                    <Button 
                      as={Link} 
                      to="/register-counsellor" 
                      variant="outline-primary" 
                      size="lg"
                    >
                      <FaChalkboardTeacher className="me-2" />
                      I'm a Counsellor
                    </Button>
                  </div>
                  
                  <p className="mt-3 text-muted small">
                    Already have an account? <Link to="/login">Login here</Link>
                  </p>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Container>
      </section>

      {/* For Counsellors Section - NEW */}
      <section className="counsellor-section py-5 bg-light">
        <Container>
          <Row className="align-items-center">
            <Col lg={6} className="mb-4 mb-lg-0">
              <Card className="border-0 shadow-lg h-100">
                <Card.Body className="p-5">
                  <div className="d-flex align-items-center mb-3">
                    <FaChalkboardTeacher size={40} className="text-primary me-3" />
                    <h3 className="mb-0">For Career Counsellors</h3>
                  </div>
                  <p className="lead mb-4">
                    Join our platform as a professional career counsellor and help 
                    students discover their ideal career paths.
                  </p>
                  <ul className="feature-list">
                    <li className="mb-2">✓ Reach thousands of students seeking guidance</li>
                    <li className="mb-2">✓ Flexible scheduling for counselling sessions</li>
                    <li className="mb-2">✓ Earn while helping students succeed</li>
                    <li className="mb-2">✓ Access to AI-powered student insights</li>
                    <li className="mb-2">✓ Build your professional profile</li>
                  </ul>
                  <Button 
                    as={Link} 
                    to="/register-counsellor" 
                    variant="primary" 
                    size="lg"
                    className="mt-3 w-100"
                  >
                    Register as Counsellor
                  </Button>
                </Card.Body>
              </Card>
            </Col>
            <Col lg={6}>
              <Card className="border-0 shadow-lg h-100">
                <Card.Body className="p-5">
                  <div className="d-flex align-items-center mb-3">
                    <FaUserGraduate size={40} className="text-success me-3" />
                    <h3 className="mb-0">For Students</h3>
                  </div>
                  <p className="lead mb-4">
                    Get personalized career guidance and discover your perfect 
                    career path with AI assistance.
                  </p>
                  <ul className="feature-list">
                    <li className="mb-2">✓ Free AI-powered career assessments</li>
                    <li className="mb-2">✓ Personalized career recommendations</li>
                    <li className="mb-2">✓ Book sessions with expert counsellors</li>
                    <li className="mb-2">✓ Explore careers, courses, and colleges</li>
                    <li className="mb-2">✓ 24/7 AI chatbot support</li>
                  </ul>
                  <Button 
                    as={Link} 
                    to="/register" 
                    variant="success" 
                    size="lg"
                    className="mt-3 w-100"
                  >
                    Register as Student
                  </Button>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Container>
      </section>

      {/* Statistics Section */}
      <section className="stats-section py-5 bg-primary text-white">
        <Container>
          <Row className="text-center">
            <Col md={3} className="mb-4 mb-md-0">
              <h2 className="display-4 fw-bold">50+</h2>
              <p className="mb-0">Career Options</p>
            </Col>
            <Col md={3} className="mb-4 mb-md-0">
              <h2 className="display-4 fw-bold">100+</h2>
              <p className="mb-0">Courses</p>
            </Col>
            <Col md={3} className="mb-4 mb-md-0">
              <h2 className="display-4 fw-bold">30+</h2>
              <p className="mb-0">Top Colleges</p>
            </Col>
            <Col md={3}>
              <h2 className="display-4 fw-bold">1000+</h2>
              <p className="mb-0">Happy Students</p>
            </Col>
          </Row>
        </Container>
      </section>

      {/* CTA Section */}
      <section className="cta-section py-5">
        <Container>
          <div className="text-center">
            <h2 className="mb-4">Start Your Career Journey Today</h2>
            <p className="lead mb-4">
              Don't let confusion hold you back. Let AI guide you to your perfect career.
            </p>
            <div className="d-flex gap-3 justify-content-center flex-wrap">
              <Button 
                as={Link} 
                to="/register" 
                variant="primary" 
                size="lg"
                className="px-5"
              >
                <FaUserGraduate className="me-2" />
                Register as Student
              </Button>
              <Button 
                as={Link} 
                to="/register-counsellor" 
                variant="outline-primary" 
                size="lg"
                className="px-5"
              >
                <FaChalkboardTeacher className="me-2" />
                Register as Counsellor
              </Button>
            </div>
          </div>
        </Container>
      </section>
    </div>
  );
};

export default Home;