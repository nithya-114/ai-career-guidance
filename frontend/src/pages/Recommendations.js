import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, ProgressBar, Badge, Alert, Spinner } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { FaStar, FaBriefcase, FaGraduationCap, FaMoneyBillWave, FaChartLine, FaRobot } from 'react-icons/fa';
import axios from 'axios';
import '../assets/css/Recommendations.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function Recommendations() {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [userProfile, setUserProfile] = useState(null);

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const fetchRecommendations = async () => {
    setLoading(true);
    setError('');

    try {
      const token = localStorage.getItem('token');
      
      if (!token) {
        setError('Please login to get recommendations');
        return;
      }

      const response = await axios.get(`${API_URL}/recommendations`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      setRecommendations(response.data.recommendations || []);
      setUserProfile(response.data.based_on || {});
    } catch (err) {
      console.error('Error fetching recommendations:', err);
      
      // For demo, use mock data
      setMockRecommendations();
    } finally {
      setLoading(false);
    }
  };

  const setMockRecommendations = () => {
    const mockData = [
      {
        career_name: 'Software Engineer',
        match_score: 92.5,
        interest_score: 95,
        skill_score: 90,
        personality_score: 92,
        reasons: [
          'Matches your interest in technology',
          'Aligns with your problem-solving and analytical skills',
          'Good personality fit for this role'
        ],
        education: ['B.Tech Computer Science', 'BCA', 'MCA'],
        salary_range: '₹4-25 LPA',
        growth_prospects: 'Excellent',
        work_environment: 'Office/Remote',
        description: 'Design, develop, and maintain software applications'
      },
      {
        career_name: 'Data Scientist',
        match_score: 88.3,
        interest_score: 90,
        skill_score: 88,
        personality_score: 86,
        reasons: [
          'Matches your interests in technology, analysis',
          'Aligns with your analytical, technical skills',
          'Based on your overall profile'
        ],
        education: ['B.Tech', 'M.Sc Statistics', 'MBA Analytics'],
        salary_range: '₹6-30 LPA',
        growth_prospects: 'Excellent',
        work_environment: 'Office/Remote'
      },
      {
        career_name: 'Business Analyst',
        match_score: 82.7,
        interest_score: 80,
        skill_score: 85,
        personality_score: 83,
        reasons: [
          'Matches your interest in problem-solving',
          'Aligns with your analytical, communication skills'
        ],
        education: ['MBA', 'BBA', 'B.Tech'],
        salary_range: '₹5-20 LPA',
        growth_prospects: 'Excellent',
        work_environment: 'Office'
      },
      {
        career_name: 'UI/UX Designer',
        match_score: 76.5,
        interest_score: 75,
        skill_score: 78,
        personality_score: 77,
        reasons: [
          'Matches your creative interests',
          'Aligns with your problem-solving skills'
        ],
        education: ['B.Des', 'BFA', 'Diploma in Design'],
        salary_range: '₹4-18 LPA',
        growth_prospects: 'Good',
        work_environment: 'Office/Remote'
      },
      {
        career_name: 'Product Manager',
        match_score: 74.2,
        interest_score: 70,
        skill_score: 75,
        personality_score: 78,
        reasons: [
          'Matches your interest in technology and business',
          'Aligns with your leadership skills'
        ],
        education: ['MBA', 'B.Tech + MBA'],
        salary_range: '₹8-35 LPA',
        growth_prospects: 'Excellent',
        work_environment: 'Office'
      }
    ];

    setRecommendations(mockData);
    setUserProfile({
      interests: ['technology', 'problem-solving', 'innovation'],
      skills: ['analytical', 'technical', 'communication'],
      personality: ['analytical', 'detail-oriented', 'creative']
    });
  };

  const getMatchColor = (score) => {
    if (score >= 85) return 'success';
    if (score >= 70) return 'info';
    if (score >= 60) return 'warning';
    return 'secondary';
  };

  const getMatchLabel = (score) => {
    if (score >= 85) return 'Excellent Match';
    if (score >= 70) return 'Great Match';
    if (score >= 60) return 'Good Match';
    return 'Potential Match';
  };

  if (loading) {
    return (
      <Container className="recommendations-page py-5">
        <div className="text-center">
          <Spinner animation="border" variant="primary" size="lg" />
          <h4 className="mt-3">Analyzing your profile...</h4>
          <p className="text-muted">
            We're matching you with the perfect careers based on your interests, skills, and personality
          </p>
        </div>
      </Container>
    );
  }

  return (
    <div className="recommendations-page">
      {/* Header */}
      <div className="recommendations-header bg-gradient text-white py-5">
        <Container>
          <div className="text-center">
            <FaRobot size={60} className="mb-3" />
            <h1 className="display-4 mb-3">Your Career Recommendations</h1>
            <p className="lead">
              AI-powered career matches based on your unique profile
            </p>
          </div>
        </Container>
      </div>

      <Container className="py-4">
        {error && (
          <Alert variant="warning" className="mb-4">
            {error}
            <div className="mt-2">
              <Button as={Link} to="/login" variant="primary" size="sm">
                Login
              </Button>
            </div>
          </Alert>
        )}

        {/* Profile Summary */}
        {userProfile && (
          <Card className="mb-4 shadow-sm">
            <Card.Body>
              <h5 className="mb-3">
                <FaChartLine className="me-2 text-primary" />
                Based on Your Profile
              </h5>
              <Row>
                {userProfile.interests && userProfile.interests.length > 0 && (
                  <Col md={4} className="mb-3 mb-md-0">
                    <h6 className="text-muted mb-2">Interests</h6>
                    <div className="d-flex flex-wrap gap-2">
                      {userProfile.interests.map((interest, index) => (
                        <Badge key={index} bg="primary" className="px-2 py-1">
                          {interest}
                        </Badge>
                      ))}
                    </div>
                  </Col>
                )}
                {userProfile.skills && userProfile.skills.length > 0 && (
                  <Col md={4} className="mb-3 mb-md-0">
                    <h6 className="text-muted mb-2">Skills</h6>
                    <div className="d-flex flex-wrap gap-2">
                      {userProfile.skills.map((skill, index) => (
                        <Badge key={index} bg="success" className="px-2 py-1">
                          {skill}
                        </Badge>
                      ))}
                    </div>
                  </Col>
                )}
                {userProfile.personality && userProfile.personality.length > 0 && (
                  <Col md={4}>
                    <h6 className="text-muted mb-2">Personality</h6>
                    <div className="d-flex flex-wrap gap-2">
                      {userProfile.personality.map((trait, index) => (
                        <Badge key={index} bg="info" className="px-2 py-1">
                          {trait}
                        </Badge>
                      ))}
                    </div>
                  </Col>
                )}
              </Row>
            </Card.Body>
          </Card>
        )}

        {/* Recommendations */}
        {recommendations.length === 0 ? (
          <Card className="text-center py-5">
            <Card.Body>
              <FaBriefcase size={60} className="text-muted mb-3" />
              <h4>No recommendations yet</h4>
              <p className="text-muted mb-4">
                Complete your profile and take our quizzes to get personalized career recommendations
              </p>
              <div className="d-flex gap-3 justify-content-center flex-wrap">
                <Button as={Link} to="/profile" variant="primary">
                  Complete Profile
                </Button>
                <Button as={Link} to="/quiz" variant="outline-primary">
                  Take Quiz
                </Button>
              </div>
            </Card.Body>
          </Card>
        ) : (
          <div>
            <div className="mb-4">
              <h4>Top {recommendations.length} Career Matches for You</h4>
              <p className="text-muted">
                Sorted by match score - higher percentages indicate better alignment with your profile
              </p>
            </div>

            {recommendations.map((rec, index) => (
              <Card key={index} className="recommendation-card mb-4 shadow-sm">
                <Card.Body className="p-4">
                  <Row>
                    <Col md={8}>
                      {/* Career Info */}
                      <div className="d-flex align-items-start mb-3">
                        <div className="match-rank me-3">
                          <Badge bg={getMatchColor(rec.match_score)} className="rounded-circle" style={{ width: '50px', height: '50px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.2rem' }}>
                            #{index + 1}
                          </Badge>
                        </div>
                        <div className="flex-grow-1">
                          <h3 className="mb-2">{rec.career_name}</h3>
                          <div className="d-flex align-items-center gap-3 mb-2">
                            <Badge bg={getMatchColor(rec.match_score)}>
                              {rec.match_score}% Match
                            </Badge>
                            <Badge bg="light" text="dark">
                              {getMatchLabel(rec.match_score)}
                            </Badge>
                          </div>
                          {rec.description && (
                            <p className="text-muted mb-3">{rec.description}</p>
                          )}
                        </div>
                      </div>

                      {/* Match Breakdown */}
                      <div className="match-breakdown mb-3">
                        <h6 className="mb-3">Match Breakdown</h6>
                        <Row className="g-3">
                          <Col sm={4}>
                            <div className="mb-1 small text-muted">Interests</div>
                            <ProgressBar 
                              now={rec.interest_score} 
                              variant="primary" 
                              label={`${rec.interest_score}%`}
                              style={{ height: '25px' }}
                            />
                          </Col>
                          <Col sm={4}>
                            <div className="mb-1 small text-muted">Skills</div>
                            <ProgressBar 
                              now={rec.skill_score} 
                              variant="success" 
                              label={`${rec.skill_score}%`}
                              style={{ height: '25px' }}
                            />
                          </Col>
                          <Col sm={4}>
                            <div className="mb-1 small text-muted">Personality</div>
                            <ProgressBar 
                              now={rec.personality_score} 
                              variant="info" 
                              label={`${rec.personality_score}%`}
                              style={{ height: '25px' }}
                            />
                          </Col>
                        </Row>
                      </div>

                      {/* Why This Career */}
                      {rec.reasons && rec.reasons.length > 0 && (
                        <div className="mb-3">
                          <h6 className="mb-2">
                            <FaStar className="text-warning me-2" />
                            Why This Career?
                          </h6>
                          <ul className="reasons-list mb-0">
                            {rec.reasons.map((reason, idx) => (
                              <li key={idx}>{reason}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </Col>

                    <Col md={4}>
                      {/* Career Details */}
                      <Card className="bg-light border-0 h-100">
                        <Card.Body>
                          <h6 className="mb-3">Career Details</h6>
                          
                          <div className="mb-3">
                            <div className="d-flex align-items-center mb-1">
                              <FaMoneyBillWave className="text-success me-2" />
                              <small className="text-muted">Salary Range</small>
                            </div>
                            <strong>{rec.salary_range}</strong>
                          </div>

                          <div className="mb-3">
                            <div className="d-flex align-items-center mb-1">
                              <FaGraduationCap className="text-info me-2" />
                              <small className="text-muted">Education</small>
                            </div>
                            {rec.education && rec.education.slice(0, 2).map((edu, idx) => (
                              <div key={idx} className="small">{edu}</div>
                            ))}
                            {rec.education && rec.education.length > 2 && (
                              <small className="text-muted">+{rec.education.length - 2} more</small>
                            )}
                          </div>

                          <div className="mb-3">
                            <div className="d-flex align-items-center mb-1">
                              <FaChartLine className="text-success me-2" />
                              <small className="text-muted">Growth</small>
                            </div>
                            <Badge bg="success">{rec.growth_prospects}</Badge>
                          </div>

                          <div className="mb-4">
                            <div className="d-flex align-items-center mb-1">
                              <FaBriefcase className="text-primary me-2" />
                              <small className="text-muted">Environment</small>
                            </div>
                            <small>{rec.work_environment}</small>
                          </div>

                          <div className="d-grid gap-2">
                            <Button variant="primary" size="sm">
                              View Details
                            </Button>
                            <Button variant="outline-primary" size="sm">
                              Find Colleges
                            </Button>
                          </div>
                        </Card.Body>
                      </Card>
                    </Col>
                  </Row>
                </Card.Body>
              </Card>
            ))}
          </div>
        )}

        {/* Call to Action */}
        {recommendations.length > 0 && (
          <Card className="mt-4 bg-light border-0">
            <Card.Body className="text-center py-5">
              <h4 className="mb-3">Ready to Take the Next Step?</h4>
              <p className="text-muted mb-4">
                Explore colleges, talk to expert counsellors, or learn more about these careers
              </p>
              <div className="d-flex gap-3 justify-content-center flex-wrap">
                <Button as={Link} to="/colleges" variant="primary" size="lg">
                  Find Colleges
                </Button>
                <Button as={Link} to="/counsellors" variant="outline-primary" size="lg">
                  Book Counsellor
                </Button>
                <Button as={Link} to="/careers" variant="outline-primary" size="lg">
                  Explore All Careers
                </Button>
              </div>
            </Card.Body>
          </Card>
        )}
      </Container>
    </div>
  );
}

export default Recommendations;