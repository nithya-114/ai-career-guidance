import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Form, Button, Badge, InputGroup, Spinner, Alert } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { FaSearch, FaBriefcase, FaMoneyBillWave, FaGraduationCap, FaArrowRight } from 'react-icons/fa';
import axios from 'axios';
import '../assets/css/Career.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function CareerListing() {
  const [careers, setCareers] = useState([]);
  const [filteredCareers, setFilteredCareers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');

  const categories = [
    'All',
    'Technology',
    'Healthcare',
    'Business',
    'Engineering',
    'Education',
    'Creative Arts',
    'Science',
    'Finance'
  ];

  useEffect(() => {
    fetchCareers();
  }, []);

  useEffect(() => {
    filterCareers();
  }, [searchTerm, selectedCategory, careers]);

  const fetchCareers = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/careers`);
      setCareers(response.data.careers || []);
      setError('');
    } catch (err) {
      console.error('Error fetching careers:', err);
      setError('Failed to load careers. Please try again.');
      // Set mock data for demo
      setMockCareers();
    } finally {
      setLoading(false);
    }
  };

  const setMockCareers = () => {
    const mockData = [
      {
        _id: '1',
        name: 'Software Engineer',
        category: 'Technology',
        description: 'Design, develop, and maintain software applications using programming languages and frameworks.',
        salary_range: '₹4-25 LPA',
        required_education: ['B.Tech Computer Science', 'BCA', 'MCA'],
        growth_prospects: 'Excellent'
      },
      {
        _id: '2',
        name: 'Data Scientist',
        category: 'Technology',
        description: 'Analyze complex data to help organizations make better decisions using statistical and machine learning techniques.',
        salary_range: '₹6-30 LPA',
        required_education: ['B.Tech', 'M.Sc Statistics', 'MBA Analytics'],
        growth_prospects: 'Excellent'
      },
      {
        _id: '3',
        name: 'Doctor',
        category: 'Healthcare',
        description: 'Diagnose and treat illnesses, provide medical care, and work to improve patient health outcomes.',
        salary_range: '₹6-50 LPA',
        required_education: ['MBBS', 'MD', 'MS'],
        growth_prospects: 'Very Good'
      },
      {
        _id: '4',
        name: 'Business Analyst',
        category: 'Business',
        description: 'Analyze business processes and requirements to improve organizational efficiency and profitability.',
        salary_range: '₹5-20 LPA',
        required_education: ['BBA', 'MBA', 'B.Tech'],
        growth_prospects: 'Excellent'
      },
      {
        _id: '5',
        name: 'Graphic Designer',
        category: 'Creative Arts',
        description: 'Create visual content for brands, products, and communications using design software and creativity.',
        salary_range: '₹3-15 LPA',
        required_education: ['B.Des', 'BFA', 'Diploma in Design'],
        growth_prospects: 'Good'
      },
      {
        _id: '6',
        name: 'Civil Engineer',
        category: 'Engineering',
        description: 'Design, construct, and maintain infrastructure projects like buildings, roads, and bridges.',
        salary_range: '₹3-15 LPA',
        required_education: ['B.Tech Civil', 'Diploma Civil'],
        growth_prospects: 'Good'
      },
      {
        _id: '7',
        name: 'Teacher',
        category: 'Education',
        description: 'Educate and inspire students, create lesson plans, and assess student progress.',
        salary_range: '₹3-8 LPA',
        required_education: ['B.Ed', 'M.Ed', 'B.A/B.Sc + B.Ed'],
        growth_prospects: 'Good'
      },
      {
        _id: '8',
        name: 'Chartered Accountant',
        category: 'Finance',
        description: 'Manage financial records, audits, taxation, and provide financial advisory services.',
        salary_range: '₹6-30 LPA',
        required_education: ['CA', 'B.Com + CA'],
        growth_prospects: 'Excellent'
      }
    ];
    setCareers(mockData);
  };

  const filterCareers = () => {
    let filtered = careers;

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(career =>
        career.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        career.description.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Filter by category
    if (selectedCategory !== 'all') {
      filtered = filtered.filter(career =>
        career.category.toLowerCase() === selectedCategory.toLowerCase()
      );
    }

    setFilteredCareers(filtered);
  };

  const getGrowthBadgeColor = (growth) => {
    if (growth === 'Excellent') return 'success';
    if (growth === 'Very Good') return 'info';
    if (growth === 'Good') return 'primary';
    return 'secondary';
  };

  if (loading) {
    return (
      <Container className="py-5 text-center">
        <Spinner animation="border" variant="primary" />
        <p className="mt-3">Loading careers...</p>
      </Container>
    );
  }

  return (
    <div className="career-listing-page">
      <div className="career-header bg-primary text-white py-5">
        <Container>
          <h1 className="display-4 mb-3">Explore Career Paths</h1>
          <p className="lead">
            Discover your perfect career from our comprehensive database of opportunities
          </p>
        </Container>
      </div>

      <Container className="py-4">
        {error && (
          <Alert variant="warning" dismissible onClose={() => setError('')}>
            {error}
          </Alert>
        )}

        {/* Search and Filter Section */}
        <Card className="mb-4 shadow-sm">
          <Card.Body>
            <Row className="g-3">
              <Col md={6}>
                <InputGroup>
                  <InputGroup.Text>
                    <FaSearch />
                  </InputGroup.Text>
                  <Form.Control
                    type="text"
                    placeholder="Search careers..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                </InputGroup>
              </Col>
              <Col md={6}>
                <Form.Select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                >
                  <option value="all">All Categories</option>
                  {categories.map((category, index) => (
                    <option key={index} value={category.toLowerCase()}>
                      {category}
                    </option>
                  ))}
                </Form.Select>
              </Col>
            </Row>
          </Card.Body>
        </Card>

        {/* Results Count */}
        <div className="mb-3">
          <p className="text-muted">
            Showing {filteredCareers.length} {filteredCareers.length === 1 ? 'career' : 'careers'}
          </p>
        </div>

        {/* Career Cards Grid */}
        {filteredCareers.length === 0 ? (
          <Alert variant="info">
            <FaBriefcase className="me-2" />
            No careers found matching your criteria. Try different search terms or categories.
          </Alert>
        ) : (
          <Row className="g-4">
            {filteredCareers.map((career) => (
              <Col key={career._id} md={6} lg={4}>
                <Card className="career-card h-100 shadow-sm hover-shadow">
                  <Card.Body className="d-flex flex-column">
                    <div className="d-flex justify-content-between align-items-start mb-3">
                      <div>
                        <Badge bg="light" text="dark" className="mb-2">
                          {career.category}
                        </Badge>
                        <h5 className="mb-0">{career.name}</h5>
                      </div>
                      <FaBriefcase size={24} className="text-primary" />
                    </div>

                    <p className="text-muted flex-grow-1">
                      {career.description}
                    </p>

                    <div className="career-info mt-3">
                      <div className="d-flex align-items-center mb-2">
                        <FaMoneyBillWave className="text-success me-2" />
                        <small className="text-muted">Salary Range:</small>
                        <strong className="ms-auto">{career.salary_range}</strong>
                      </div>

                      <div className="d-flex align-items-center mb-2">
                        <FaGraduationCap className="text-info me-2" />
                        <small className="text-muted">Education:</small>
                        <Badge bg="light" text="dark" className="ms-auto">
                          {career.required_education?.[0] || 'Various'}
                        </Badge>
                      </div>

                      <div className="d-flex align-items-center mb-3">
                        <small className="text-muted">Growth:</small>
                        <Badge 
                          bg={getGrowthBadgeColor(career.growth_prospects)} 
                          className="ms-auto"
                        >
                          {career.growth_prospects}
                        </Badge>
                      </div>

                      <Button
                        as={Link}
                        to={`/careers/${career._id}`}
                        variant="outline-primary"
                        className="w-100"
                      >
                        View Details <FaArrowRight className="ms-2" />
                      </Button>
                    </div>
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>
        )}

        {/* Call to Action */}
        <Card className="mt-5 bg-light border-0">
          <Card.Body className="text-center py-5">
            <h3 className="mb-3">Not Sure Which Career Is Right for You?</h3>
            <p className="text-muted mb-4">
              Take our comprehensive career assessment to get personalized recommendations
            </p>
            <div className="d-flex gap-3 justify-content-center flex-wrap">
              <Button as={Link} to="/quiz" variant="primary" size="lg">
                Take Career Quiz
              </Button>
              <Button as={Link} to="/recommendations" variant="outline-primary" size="lg">
                Get AI Recommendations
              </Button>
            </div>
          </Card.Body>
        </Card>
      </Container>
    </div>
  );
}

export default CareerListing;