import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';

function StudentDashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [greeting, setGreeting] = useState('');
  const [profileData, setProfileData] = useState(null);
  const [stats, setStats] = useState({
    quizzesCompleted: 0,
    careersExplored: 0,
    collegesViewed: 0,
    sessionsBooked: 0
  });
  const [loading, setLoading] = useState(true);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

  useEffect(() => {
    const hour = new Date().getHours();
    if (hour < 12) setGreeting('Good Morning');
    else if (hour < 18) setGreeting('Good Afternoon');
    else setGreeting('Good Evening');

    fetchStudentData();
  }, []);

  const fetchStudentData = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/user/profile`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      setProfileData(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching student data:', error);
      setLoading(false);
    }
  };

  const quickActions = [
    {
      icon: '💬',
      title: 'Chat with AI',
      description: 'Get personalized career guidance',
      action: () => navigate('/chat'),
      color: 'primary',
      bgColor: '#e8eaf6'
    },
    {
      icon: '✅',
      title: 'Take Quiz',
      description: 'Assess your aptitude & personality',
      action: () => navigate('/quiz'),
      color: 'success',
      bgColor: '#e8f5e9'
    },
    {
      icon: '💼',
      title: 'Explore Careers',
      description: 'Browse career options',
      action: () => navigate('/careers'),
      color: 'warning',
      bgColor: '#fff8e1'
    },
    {
      icon: '🏛️',
      title: 'Find Colleges',
      description: 'Discover best colleges',
      action: () => navigate('/colleges'),
      color: 'info',
      bgColor: '#e1f5fe'
    },
    {
      icon: '👨‍🏫',
      title: 'Book Counsellor',
      description: 'Connect with experts',
      action: () => navigate('/counsellors'),
      color: 'danger',
      bgColor: '#fce4ec'
    },
    {
      icon: '🎯',
      title: 'Recommendations',
      description: 'AI career suggestions',
      action: () => navigate('/recommendations'),
      color: 'secondary',
      bgColor: '#f3e5f5'
    }
  ];

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ minHeight: '80vh' }}>
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="container-fluid py-4">
      <div className="row mb-4">
        <div className="col-12">
          <div className="p-4 rounded-3 shadow-sm" style={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white'
          }}>
            <h2 className="mb-2">{greeting}, <span className="fw-bold">{profileData?.name}!</span></h2>
            <p className="mb-0">Ready to explore your career options? Let's get started!</p>
          </div>
        </div>
      </div>

      <div className="row mb-4">
        <div className="col-12"><h4 className="mb-3">Quick Actions</h4></div>
        {quickActions.map((action, index) => (
          <div key={index} className="col-lg-4 col-md-6 mb-4">
            <div className="card h-100 border-0 shadow-sm" onClick={action.action} style={{ cursor: 'pointer' }}>
              <div className="card-body text-center p-4">
                <div className="mb-3 mx-auto d-flex align-items-center justify-content-center rounded-circle"
                  style={{ width: '80px', height: '80px', backgroundColor: action.bgColor, fontSize: '2.5rem' }}>
                  {action.icon}
                </div>
                <h5 className="card-title mb-2">{action.title}</h5>
                <p className="card-text text-muted small">{action.description}</p>
                <button className={`btn btn-${action.color} btn-sm mt-2`}>Get Started</button>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="row mt-4">
        <div className="col-md-3 mb-3">
          <div className="card border-0 shadow-sm text-center">
            <div className="card-body"><h3 className="text-primary mb-2">{stats.quizzesCompleted}</h3>
              <p className="text-muted small mb-0">Quizzes Completed</p></div>
          </div>
        </div>
        <div className="col-md-3 mb-3">
          <div className="card border-0 shadow-sm text-center">
            <div className="card-body"><h3 className="text-success mb-2">{stats.careersExplored}</h3>
              <p className="text-muted small mb-0">Careers Explored</p></div>
          </div>
        </div>
        <div className="col-md-3 mb-3">
          <div className="card border-0 shadow-sm text-center">
            <div className="card-body"><h3 className="text-warning mb-2">{stats.collegesViewed}</h3>
              <p className="text-muted small mb-0">Colleges Viewed</p></div>
          </div>
        </div>
        <div className="col-md-3 mb-3">
          <div className="card border-0 shadow-sm text-center">
            <div className="card-body"><h3 className="text-info mb-2">{stats.sessionsBooked}</h3>
              <p className="text-muted small mb-0">Sessions Booked</p></div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default StudentDashboard;