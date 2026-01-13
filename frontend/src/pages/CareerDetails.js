import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { Container, Row, Col, Card, Badge, Button, ListGroup, Spinner, Alert } from 'react-bootstrap';
import { FaArrowLeft, FaBriefcase, FaMoneyBillWave, FaGraduationCap, FaChartLine, FaLightbulb, FaUserTie, FaBook } from 'react-icons/fa';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function CareerDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [career, setCareer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchCareerDetails();
  }, [id]);

  const fetchCareerDetails = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/careers/${id}`);
      setCareer(response.data);
      setError('');
    } catch (err) {
      console.error('Error fetching career details:', err);
      setError('Failed to load career details.');
      // Mock data for demo
      setMockCareer();
    } finally {
      setLoading(false);
    }
  };

  const setMockCareer = () => {
    const mockData = {
      _id: id,
      name: 'Software Engineer',
      category: 'Technology',
      description: 'Software engineers design, develop, test, and maintain software applications and systems. They work with programming languages, frameworks, and tools to create solutions that meet user needs. This role involves problem-solving, collaboration with teams, and continuous learning to stay updated with technology trends.',
      detailed_description: 'Software engineering is one of the most dynamic and rewarding career paths in technology. As a software engineer, you\'ll be at the forefront of innovation, creating applications and systems that power businesses and improve lives. The role requires strong analytical thinking, creativity, and the ability to work both independently and as part of a team.',
      salary_range: '₹4-25 LPA',
      required_education: ['B.Tech Computer Science', 'BCA', 'MCA', 'B.Sc Computer Science'],
      required_skills: ['Programming', 'Problem-solving', 'Analytical thinking', 'Communication', 'Team collaboration'],
      personality_traits: ['Analytical', 'Detail-oriented', 'Creative', 'Patient', 'Curious'],
      interests: ['Technology', 'Problem-solving', 'Innovation', 'Continuous learning'],
      work_environment: 'Office/Remote',
      job_outlook: 'Excellent - High demand with 22% growth expected',
      growth_prospects: 'Excellent',
      typical_day: [
        'Attend daily stand-up meetings',
        'Write and review code',
        'Debug and fix issues',
        'Collaborate with team members',
        'Test new features',
        'Documentation and planning'
      ],
      career_path: [
        'Junior Software Engineer (0-2 years)',
        'Software Engineer (2-5 years)',
        'Senior Software Engineer (5-8 years)',
        'Lead Engineer/Architect (8+ years)',
        'Engineering Manager/CTO'
      ],
      related_careers: ['Data Scientist', 'DevOps Engineer', 'Full Stack Developer', 'Mobile App Developer']
    };
    setCareer(mockData);
  };

  if (loading) {
    return (
      <Container className="py-5 text-center">
        <Spinner animation="border" variant="primary" />
        <p className="mt-3">Loading career details...</p>
      </Container>
    );
  }

  if (error || !career) {
    return (
      <Container className="py-5">
        <Alert variant="danger">
          {error || 'Career not found.'}
          <div className="mt-3">
            <Button variant="primary" onClick={() => navigate('/careers')}>
              Back to Career Listing
            </Button>
          </div>
        </Alert>
      </Container>
    );
  }

  return (
    <div className="career-details-page">
      {/* Header */}
      <div className="career-details-header bg-primary text-white py-4">
        <Container>
          <Button
            variant="light"
            size="sm"
            className="mb-3"
            onClick={() => navigate('/careers')}
          >
            <FaArrowLeft className="me-2" />
            Back to Careers
          </Button>
          <div className="d-flex align-items-start justify-content-between">
            <div>
              <Badge bg="light" text="dark" className="mb-2">
                {career.category}
              </Badge>
              <h1 className="display-5 mb-2">{career.name}</h1>
              <p className="lead mb-0">{career.description}</p>
            </div>
            <FaBriefcase size={50} />
          </div>
        </Container>
      </div>

      <Container className="py-4">
        <Row className="g-4">
          {/* Main Content */}
          <Col lg={8}>
            {/* Overview */}
            <Card className="mb-4 shadow-sm">
              <Card.Body>
                <h4 className="mb-3">
                  <FaBook className="me-2 text-primary" />
                  Overview
                </h4>
                <p>{career.detailed_description || career.description}</p>
              </Card.Body>
            </Card>

            {/* Required Skills */}
            <Card className="mb-4 shadow-sm">
              <Card.Body>
                <h4 className="mb-3">
                  <FaLightbulb className="me-2 text-warning" />
                  Required Skills
                </h4>
                <div className="d-flex flex-wrap gap-2">
                  {career.required_skills?.map((skill, index) => (
                    <Badge key={index} bg="primary" className="px-3 py-2">
                      {skill}
                    </Badge>
                  ))}
                </div>
              </Card.Body>
            </Card>

            {/* Personality Traits */}
            <Card className="mb-4 shadow-sm">
              <Card.Body>
                <h4 className="mb-3">
                  <FaUserTie className="me-2 text-info" />
                  Ideal Personality Traits
                </h4>
                <div className="d-flex flex-wrap gap-2">
                  {career.personality_traits?.map((trait, index) => (
                    <Badge key={index} bg="info" className="px-3 py-2">
                      {trait}
                    </Badge>
                  ))}
                </div>
              </Card.Body>
            </Card>

            {/* Typical Day */}
            {career.typical_day && (
              <Card className="mb-4 shadow-sm">
                <Card.Body>
                  <h4 className="mb-3">A Day in the Life</h4>
                  <ListGroup variant="flush">
                    {career.typical_day.map((activity, index) => (
                      <ListGroup.Item key={index}>
                        <span className="text-primary me-2">✓</span>
                        {activity}
                      </ListGroup.Item>
                    ))}
                  </ListGroup>
                </Card.Body>
              </Card>
            )}

            {/* Career Path */}
            {career.career_path && (
              <Card className="mb-4 shadow-sm">
                <Card.Body>
                  <h4 className="mb-3">
                    <FaChartLine className="me-2 text-success" />
                    Career Progression
                  </h4>
                  <div className="career-path">
                    {career.career_path.map((stage, index) => (
                      <div key={index} className="career-stage mb-3 ps-3">
                        <div className="d-flex align-items-center">
                          <div className="stage-number me-3">
                            <Badge bg="success" className="rounded-circle" style={{ width: '30px', height: '30px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                              {index + 1}
                            </Badge>
                          </div>
                          <div>
                            <strong>{stage}</strong>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </Card.Body>
              </Card>
            )}

            {/* Related Careers */}
            {career.related_careers && career.related_careers.length > 0 && (
              <Card className="shadow-sm">
                <Card.Body>
                  <h4 className="mb-3">Related Careers</h4>
                  <div className="d-flex flex-wrap gap-2">
                    {career.related_careers.map((relatedCareer, index) => (
                      <Badge key={index} bg="light" text="dark" className="px-3 py-2">
                        {relatedCareer}
                      </Badge>
                    ))}
                  </div>
                </Card.Body>
              </Card>
            )}
          </Col>

          {/* Sidebar */}
          <Col lg={4}>
            {/* Key Information */}
            <Card className="mb-4 shadow-sm sticky-top" style={{ top: '20px' }}>
              <Card.Header className="bg-primary text-white">
                <h5 className="mb-0">Key Information</h5>
              </Card.Header>
              <ListGroup variant="flush">
                <ListGroup.Item>
                  <div className="d-flex align-items-center mb-2">
                    <FaMoneyBillWave className="text-success me-2" />
                    <strong>Salary Range</strong>
                  </div>
                  <p className="mb-0 text-muted">{career.salary_range}</p>
                </ListGroup.Item>

                <ListGroup.Item>
                  <div className="d-flex align-items-center mb-2">
                    <FaGraduationCap className="text-info me-2" />
                    <strong>Required Education</strong>
                  </div>
                  <ul className="mb-0">
                    {career.required_education?.map((edu, index) => (
                      <li key={index} className="text-muted">{edu}</li>
                    ))}
                  </ul>
                </ListGroup.Item>

                <ListGroup.Item>
                  <div className="d-flex align-items-center mb-2">
                    <FaBriefcase className="text-primary me-2" />
                    <strong>Work Environment</strong>
                  </div>
                  <p className="mb-0 text-muted">{career.work_environment}</p>
                </ListGroup.Item>

                <ListGroup.Item>
                  <div className="d-flex align-items-center mb-2">
                    <FaChartLine className="text-success me-2" />
                    <strong>Job Outlook</strong>
                  </div>
                  <p className="mb-0 text-muted">{career.job_outlook || 'Positive growth expected'}</p>
                </ListGroup.Item>

                <ListGroup.Item>
                  <div className="d-flex align-items-center mb-2">
                    <strong>Growth Prospects</strong>
                  </div>
                  <Badge bg="success">{career.growth_prospects}</Badge>
                </ListGroup.Item>
              </ListGroup>
            </Card>

            {/* Call to Action */}
            <Card className="shadow-sm bg-light border-0">
              <Card.Body className="text-center">
                <h5 className="mb-3">Interested in this career?</h5>
                <div className="d-grid gap-2">
                  <Button as={Link} to="/recommendations" variant="primary">
                    Get Personalized Match
                  </Button>
                  <Button as={Link} to="/colleges" variant="outline-primary">
                    Find Related Colleges
                  </Button>
                  <Button as={Link} to="/counsellors" variant="outline-primary">
                    Talk to a Counsellor
                  </Button>
                </div>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default CareerDetails;