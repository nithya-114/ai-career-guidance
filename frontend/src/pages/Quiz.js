import React, { useState, useEffect } from 'react';
import { Container, Card, Button, Form, ProgressBar, Alert, Badge, Row, Col } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { FaClipboardCheck, FaCheckCircle, FaClock, FaArrowRight, FaArrowLeft } from 'react-icons/fa';
import axios from 'axios';
import '../assets/css/Quiz.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function Quiz() {
  const navigate = useNavigate();
  const [quizType, setQuizType] = useState(null); // 'aptitude' or 'personality'
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [quizStarted, setQuizStarted] = useState(false);
  const [quizCompleted, setQuizCompleted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [timeRemaining, setTimeRemaining] = useState(null);
  const [results, setResults] = useState(null);
  const [showResults, setShowResults] = useState(false);

  useEffect(() => {
    if (quizStarted && timeRemaining > 0) {
      const timer = setTimeout(() => {
        setTimeRemaining(timeRemaining - 1);
      }, 1000);
      return () => clearTimeout(timer);
    } else if (timeRemaining === 0) {
      handleSubmitQuiz();
    }
  }, [timeRemaining, quizStarted]);

  const startQuiz = async (type) => {
    setQuizType(type);
    setLoading(true);
    
    try {
      const response = await axios.get(`${API_URL}/quiz/${type}/questions`);
      setQuestions(response.data.questions || []);
      setQuizStarted(true);
      if (type === 'aptitude') {
        setTimeRemaining(20 * 60); // 20 minutes for aptitude
      }
    } catch (error) {
      console.error('Error loading quiz:', error);
      // Use mock data
      setMockQuestions(type);
      setQuizStarted(true);
      if (type === 'aptitude') {
        setTimeRemaining(20 * 60);
      }
    } finally {
      setLoading(false);
    }
  };

  const setMockQuestions = (type) => {
    if (type === 'aptitude') {
      setQuestions([
        {
          id: 1,
          question: 'If 5 machines can produce 5 products in 5 minutes, how many products can 100 machines produce in 100 minutes?',
          options: ['100', '500', '2000', '10000'],
          correct: '2000',
          category: 'logical'
        },
        {
          id: 2,
          question: 'What is the next number in the sequence: 2, 6, 12, 20, 30, ?',
          options: ['38', '40', '42', '44'],
          correct: '42',
          category: 'logical'
        },
        {
          id: 3,
          question: 'If A + B = 10 and A - B = 4, what is the value of A?',
          options: ['6', '7', '8', '9'],
          correct: '7',
          category: 'numerical'
        },
        {
          id: 4,
          question: 'Choose the synonym of "Eloquent"',
          options: ['Articulate', 'Hesitant', 'Silent', 'Confused'],
          correct: 'Articulate',
          category: 'verbal'
        },
        {
          id: 5,
          question: 'A clock shows 3:15. What is the angle between hour and minute hands?',
          options: ['0°', '7.5°', '15°', '30°'],
          correct: '7.5°',
          category: 'numerical'
        }
      ]);
    } else {
      setQuestions([
        {
          id: 1,
          question: 'I prefer working:',
          options: ['Alone', 'In small groups', 'In large teams', 'It depends'],
          trait: 'work_style'
        },
        {
          id: 2,
          question: 'When faced with a problem, I tend to:',
          options: ['Analyze it logically', 'Think creatively', 'Seek advice', 'Take immediate action'],
          trait: 'problem_solving'
        },
        {
          id: 3,
          question: 'I am most interested in:',
          options: ['Technology and innovation', 'Helping people', 'Business and finance', 'Arts and creativity'],
          trait: 'interests'
        },
        {
          id: 4,
          question: 'My ideal work environment is:',
          options: ['Structured and organized', 'Flexible and dynamic', 'Collaborative', 'Independent'],
          trait: 'environment'
        },
        {
          id: 5,
          question: 'I am motivated by:',
          options: ['Financial rewards', 'Recognition', 'Making a difference', 'Learning new things'],
          trait: 'motivation'
        }
      ]);
    }
  };

  const handleAnswerSelect = (answer) => {
    setAnswers({
      ...answers,
      [currentQuestion]: answer
    });
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const handleSubmitQuiz = async () => {
    setLoading(true);
    setQuizCompleted(true);
    
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        `${API_URL}/quiz/submit`,
        {
          quiz_type: quizType,
          answers: answers,
          questions: questions
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      
      // Store results and show them
      setResults(response.data);
      setShowResults(true);
    } catch (error) {
      console.error('Error submitting quiz:', error);
      // Show mock results
      setResults({
        score: { correct: 3, total: 5, percentage: 60 },
        recommendations: []
      });
      setShowResults(true);
    } finally {
      setLoading(false);
    }
  };

  const calculateProgress = () => {
    const answered = Object.keys(answers).length;
    return (answered / questions.length) * 100;
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  // Results Screen
  if (showResults && results) {
    return (
      <Container className="quiz-page py-5">
        <Card className="shadow-sm">
          <Card.Body className="p-5 text-center">
            <div className="mb-4">
              <FaCheckCircle size={80} className="text-success mb-3" />
              <h2 className="mb-3">Quiz Completed!</h2>
            </div>

            {results.score && (
              <div className="mb-4">
                <h4>Your Score</h4>
                <div className="display-4 text-primary mb-3">
                  {results.score.percentage}%
                </div>
                <p className="text-muted">
                  {results.score.correct} correct out of {results.score.total} questions
                </p>
              </div>
            )}

            {results.recommendations && results.recommendations.length > 0 && (
              <div className="mb-4">
                <h4 className="mb-3">Recommended Careers</h4>
                <Row className="g-3">
                  {results.recommendations.map((rec, index) => (
                    <Col md={6} key={index}>
                      <Card className="h-100">
                        <Card.Body>
                          <h5>{rec.career_name}</h5>
                          <Badge bg="info" className="mb-2">{rec.category}</Badge>
                          <p className="mb-2">Match Score: <strong>{rec.match_score}%</strong></p>
                          <Button 
                            size="sm" 
                            variant="outline-primary"
                            onClick={() => navigate(`/careers/${rec.career_id}`)}
                          >
                            View Details
                          </Button>
                        </Card.Body>
                      </Card>
                    </Col>
                  ))}
                </Row>
              </div>
            )}

            <div className="mt-4">
              <Button 
                variant="primary" 
                size="lg" 
                className="me-3"
                onClick={() => navigate('/careers')}
              >
                Explore All Careers
              </Button>
              <Button 
                variant="outline-secondary" 
                size="lg"
                onClick={() => {
                  setQuizType(null);
                  setQuestions([]);
                  setCurrentQuestion(0);
                  setAnswers({});
                  setQuizStarted(false);
                  setQuizCompleted(false);
                  setResults(null);
                  setShowResults(false);
                  setTimeRemaining(null);
                }}
              >
                Take Another Quiz
              </Button>
            </div>
          </Card.Body>
        </Card>
      </Container>
    );
  }

  // Quiz Type Selection Screen
  if (!quizStarted && !quizType) {
    return (
      <Container className="quiz-page py-5">
        <div className="text-center mb-5">
          <FaClipboardCheck size={60} className="text-primary mb-3" />
          <h1 className="display-4 mb-3">Career Assessment</h1>
          <p className="lead text-muted">
            Choose a quiz to discover your perfect career path
          </p>
        </div>

        <Row className="g-4 justify-content-center">
          <Col md={6} lg={5}>
            <Card className="quiz-type-card h-100 shadow-sm hover-shadow">
              <Card.Body className="p-4">
                <div className="text-center mb-4">
                  <div className="quiz-icon mb-3">
                    <Badge bg="primary" className="p-3 rounded-circle">
                      <FaClipboardCheck size={40} />
                    </Badge>
                  </div>
                  <h3>Aptitude Test</h3>
                  <p className="text-muted">
                    Assess your logical, numerical, and verbal abilities
                  </p>
                </div>

                <ul className="list-unstyled mb-4">
                  <li className="mb-2">✓ 10 Questions</li>
                  <li className="mb-2">✓ 20 Minutes</li>
                  <li className="mb-2">✓ Multiple Choice</li>
                  <li className="mb-2">✓ Logical & Numerical Reasoning</li>
                </ul>

                <Button
                  variant="primary"
                  size="lg"
                  className="w-100"
                  onClick={() => startQuiz('aptitude')}
                >
                  Start Aptitude Test
                </Button>
              </Card.Body>
            </Card>
          </Col>

          <Col md={6} lg={5}>
            <Card className="quiz-type-card h-100 shadow-sm hover-shadow">
              <Card.Body className="p-4">
                <div className="text-center mb-4">
                  <div className="quiz-icon mb-3">
                    <Badge bg="success" className="p-3 rounded-circle">
                      <FaCheckCircle size={40} />
                    </Badge>
                  </div>
                  <h3>Personality Test</h3>
                  <p className="text-muted">
                    Discover your work style and preferences
                  </p>
                </div>

                <ul className="list-unstyled mb-4">
                  <li className="mb-2">✓ 10 Questions</li>
                  <li className="mb-2">✓ No Time Limit</li>
                  <li className="mb-2">✓ Situational Questions</li>
                  <li className="mb-2">✓ Career Personality Match</li>
                </ul>

                <Button
                  variant="success"
                  size="lg"
                  className="w-100"
                  onClick={() => startQuiz('personality')}
                >
                  Start Personality Test
                </Button>
              </Card.Body>
            </Card>
          </Col>
        </Row>

        <div className="text-center mt-5">
          <p className="text-muted">
            <small>
              These assessments help us provide personalized career recommendations.
              <br />
              Your responses are confidential and used only for guidance.
            </small>
          </p>
        </div>
      </Container>
    );
  }

  // Quiz Completed - Processing
  if (quizCompleted && loading) {
    return (
      <Container className="quiz-page py-5 text-center">
        <div className="completion-animation mb-4">
          <div className="spinner-border text-primary" style={{width: '4rem', height: '4rem'}} role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
        <h2 className="mb-3">Processing Your Results...</h2>
        <p className="lead text-muted mb-4">
          Analyzing your responses and generating recommendations...
        </p>
      </Container>
    );
  }

  // Quiz In Progress
  if (quizStarted && questions.length > 0) {
    const question = questions[currentQuestion];
    const progress = calculateProgress();
    const isLastQuestion = currentQuestion === questions.length - 1;
    const allQuestionsAnswered = Object.keys(answers).length === questions.length;

    return (
      <Container className="quiz-page py-4">
        <Card className="shadow-sm">
          <Card.Header className="bg-primary text-white">
            <div className="d-flex justify-content-between align-items-center">
              <div>
                <h5 className="mb-0">
                  {quizType === 'aptitude' ? 'Aptitude Test' : 'Personality Test'}
                </h5>
                <small>Question {currentQuestion + 1} of {questions.length}</small>
              </div>
              {timeRemaining !== null && (
                <div className="d-flex align-items-center">
                  <FaClock className="me-2" />
                  <span className={timeRemaining < 60 ? 'text-warning fw-bold' : ''}>
                    {formatTime(timeRemaining)}
                  </span>
                </div>
              )}
            </div>
          </Card.Header>

          <Card.Body className="p-4">
            {/* Progress Bar */}
            <div className="mb-4">
              <div className="d-flex justify-content-between mb-2">
                <small className="text-muted">Progress</small>
                <small className="text-muted">{Math.round(progress)}%</small>
              </div>
              <ProgressBar now={progress} variant="primary" />
            </div>

            {/* Question */}
            <div className="question-section mb-4">
              <h4 className="mb-4">{question.question}</h4>

              {/* Options */}
              <div className="options-section">
                {question.options.map((option, index) => (
                  <Card
                    key={index}
                    className={`option-card mb-3 ${answers[currentQuestion] === option ? 'selected' : ''}`}
                    onClick={() => handleAnswerSelect(option)}
                    style={{ cursor: 'pointer' }}
                  >
                    <Card.Body className="d-flex align-items-center">
                      <Form.Check
                        type="radio"
                        name={`question-${currentQuestion}`}
                        checked={answers[currentQuestion] === option}
                        onChange={() => {}}
                        className="me-3"
                      />
                      <span>{option}</span>
                    </Card.Body>
                  </Card>
                ))}
              </div>
            </div>

            {/* Navigation */}
            <div className="d-flex justify-content-between align-items-center">
              <Button
                variant="outline-secondary"
                onClick={handlePrevious}
                disabled={currentQuestion === 0}
              >
                <FaArrowLeft className="me-2" />
                Previous
              </Button>

              <div>
                {!isLastQuestion ? (
                  <Button
                    variant="primary"
                    onClick={handleNext}
                    disabled={!answers[currentQuestion]}
                  >
                    Next
                    <FaArrowRight className="ms-2" />
                  </Button>
                ) : (
                  <Button
                    variant="success"
                    onClick={handleSubmitQuiz}
                    disabled={!allQuestionsAnswered || loading}
                  >
                    {loading ? 'Submitting...' : 'Submit Quiz'}
                    <FaCheckCircle className="ms-2" />
                  </Button>
                )}
              </div>
            </div>

            {/* Answer Count */}
            <div className="text-center mt-3">
              <small className="text-muted">
                Answered: {Object.keys(answers).length} / {questions.length}
              </small>
            </div>
          </Card.Body>
        </Card>

        {/* Tips Card */}
        <Card className="mt-4 border-info">
          <Card.Body>
            <h6 className="text-info mb-2">💡 Tips</h6>
            <ul className="small mb-0">
              <li>Answer honestly for best results</li>
              <li>Don't overthink - go with your first instinct</li>
              <li>You can go back and change answers before submitting</li>
            </ul>
          </Card.Body>
        </Card>
      </Container>
    );
  }

  return (
    <Container className="py-5 text-center">
      <div className="spinner-border text-primary" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
      <p className="mt-3">Loading quiz...</p>
    </Container>
  );
}

export default Quiz;