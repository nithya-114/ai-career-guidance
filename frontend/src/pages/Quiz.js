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
    } catch (error) {
      console.error('Error loading quiz:', error);
      // Use mock data
      setMockQuestions(type);
    } finally {
      setLoading(false);
      setQuizStarted(true);
      if (type === 'aptitude') {
        setTimeRemaining(20 * 60); // 20 minutes for aptitude
      }
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
      
      // Navigate to results
      navigate('/quiz/results', { state: { results: response.data } });
    } catch (error) {
      console.error('Error submitting quiz:', error);
      // For demo, show completion
      setQuizCompleted(true);
      setTimeout(() => {
        navigate('/recommendations');
      }, 2000);
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
                  <li className="mb-2">✓ 20 Questions</li>
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
                  <li className="mb-2">✓ 15 Questions</li>
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

  // Quiz Completed Screen
  if (quizCompleted) {
    return (
      <Container className="quiz-page py-5 text-center">
        <div className="completion-animation mb-4">
          <FaCheckCircle size={80} className="text-success" />
        </div>
        <h2 className="mb-3">Quiz Completed!</h2>
        <p className="lead text-muted mb-4">
          Analyzing your responses and generating recommendations...
        </p>
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </Container>
    );
  }

  // Quiz In Progress
  if (quizStarted && questions.length > 0) {
    const question = questions[currentQuestion];
    const progress = calculateProgress();

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
                  <span className={timeRemaining < 60 ? 'text-warning' : ''}>
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
                {currentQuestion < questions.length - 1 ? (
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
                    disabled={Object.keys(answers).length !== questions.length || loading}
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
              <li>You can go back and change answers</li>
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