import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import '../assets/css/Dashboard.css';

function Dashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [greeting, setGreeting] = useState('');
  const [profileData, setProfileData] = useState(null);
  const [appointments, setAppointments] = useState([]);
  const [stats, setStats] = useState({
    totalSessions: 0,
    averageRating: 0,
    studentsHelped: 0,
    earnings: 0,
    pendingAppointments: 0,
    completedAppointments: 0
  });
  const [loading, setLoading] = useState(true);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

  useEffect(() => {
    const hour = new Date().getHours();
    if (hour < 12) setGreeting('Good Morning');
    else if (hour < 18) setGreeting('Good Afternoon');
    else setGreeting('Good Evening');

    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      const token = localStorage.getItem('token');
      
      if (!token) {
        setLoading(false);
        return;
      }

      // Fetch user profile
      const profileResponse = await axios.get(`${API_URL}/user/profile`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      console.log('Profile data:', profileResponse.data);
      setProfileData(profileResponse.data);

      // If counsellor, fetch appointments
      if (profileResponse.data.role === 'counsellor') {
        // TODO: Fetch appointments from backend
        // For now using mock data
        const profile = profileResponse.data.profile || {};
        setStats({
          totalSessions: profile.sessions_conducted || 0,
          averageRating: profile.rating || 4.5,
          studentsHelped: profile.sessions_conducted || 0,
          earnings: (profile.sessions_conducted || 0) * (profile.hourly_rate || 500),
          pendingAppointments: 0,
          completedAppointments: 0
        });
      }

      setLoading(false);
    } catch (error) {
      console.error('Error fetching user data:', error);
      setLoading(false);
    }
  };

  // STUDENT DASHBOARD
  const StudentDashboard = () => {
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
        description: 'Discover best colleges for you',
        action: () => navigate('/colleges'),
        color: 'info',
        bgColor: '#e1f5fe'
      },
      {
        icon: '👨‍🏫',
        title: 'Book Counsellor Session',
        description: 'Connect with expert counsellors',
        action: () => navigate('/counsellors'),
        color: 'danger',
        bgColor: '#fce4ec'
      },
      {
        icon: '🎯',
        title: 'Get Recommendations',
        description: 'AI-powered career suggestions',
        action: () => navigate('/recommendations'),
        color: 'secondary',
        bgColor: '#f3e5f5'
      }
    ];

    return (
      <>
        {/* Quick Actions */}
        <div className="row mb-4">
          <div className="col-12">
            <h4 className="mb-3">Quick Actions</h4>
          </div>
          {quickActions.map((action, index) => (
            <div key={index} className="col-lg-4 col-md-6 mb-4">
              <div 
                className="action-card card h-100 border-0 shadow-sm"
                onClick={action.action}
                style={{ cursor: 'pointer', transition: 'transform 0.2s' }}
                onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-5px)'}
                onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0)'}
              >
                <div className="card-body text-center p-4">
                  <div 
                    className="icon-wrapper mb-3 mx-auto d-flex align-items-center justify-content-center rounded-circle"
                    style={{
                      width: '80px',
                      height: '80px',
                      backgroundColor: action.bgColor,
                      fontSize: '2.5rem'
                    }}
                  >
                    {action.icon}
                  </div>
                  <h5 className="card-title mb-2">{action.title}</h5>
                  <p className="card-text text-muted small">{action.description}</p>
                  <button className={`btn btn-${action.color} btn-sm mt-2`}>
                    {action.title.includes('Book') ? 'View Counsellors' :
                     action.title.includes('Chat') ? 'Start Chat' :
                     action.title.includes('Quiz') ? 'Take Quiz' :
                     'Get Started'}
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </>
    );
  };

  // COUNSELLOR DASHBOARD
  const CounsellorDashboard = () => {
    const counsellorActions = [
      {
        icon: '📅',
        title: 'My Appointments',
        description: 'View and manage scheduled sessions',
        action: () => navigate('/appointments'),
        color: 'primary',
        bgColor: '#e8eaf6'
      },
      {
        icon: '👥',
        title: 'Student Profiles',
        description: 'View assigned student profiles',
        action: () => navigate('/students'),
        color: 'success',
        bgColor: '#e8f5e9'
      },
      {
        icon: '📊',
        title: 'Reports & Analytics',
        description: 'View session reports and analytics',
        action: () => navigate('/reports'),
        color: 'info',
        bgColor: '#e1f5fe'
      },
      {
        icon: '⚙️',
        title: 'Profile Settings',
        description: 'Update your professional profile',
        action: () => navigate('/profile'),
        color: 'warning',
        bgColor: '#fff8e1'
      }
    ];

    return (
      <>
        {/* Counsellor Quick Actions */}
        <div className="row mb-4">
          <div className="col-12">
            <h4 className="mb-3">Quick Actions</h4>
          </div>
          {counsellorActions.map((action, index) => (
            <div key={index} className="col-lg-3 col-md-6 mb-4">
              <div 
                className="action-card card h-100 border-0 shadow-sm"
                onClick={action.action}
                style={{ cursor: 'pointer', transition: 'transform 0.2s' }}
                onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-5px)'}
                onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0)'}
              >
                <div className="card-body text-center p-4">
                  <div 
                    className="icon-wrapper mb-3 mx-auto d-flex align-items-center justify-content-center rounded-circle"
                    style={{
                      width: '70px',
                      height: '70px',
                      backgroundColor: action.bgColor,
                      fontSize: '2rem'
                    }}
                  >
                    {action.icon}
                  </div>
                  <h6 className="card-title mb-2">{action.title}</h6>
                  <p className="card-text text-muted small">{action.description}</p>
                  <button className={`btn btn-${action.color} btn-sm mt-2`}>
                    View
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Upcoming Appointments */}
        <div className="row mb-4">
          <div className="col-12">
            <div className="card border-0 shadow-sm">
              <div className="card-body">
                <h5 className="card-title mb-4">📅 Upcoming Appointments</h5>
                {appointments.length === 0 ? (
                  <div className="text-center py-5">
                    <p className="text-muted mb-3">No upcoming appointments</p>
                    <small className="text-muted">Students will see your profile in the counsellor directory</small>
                  </div>
                ) : (
                  <div className="table-responsive">
                    <table className="table table-hover">
                      <thead>
                        <tr>
                          <th>Student</th>
                          <th>Date & Time</th>
                          <th>Duration</th>
                          <th>Amount</th>
                          <th>Status</th>
                          <th>Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {appointments.map((apt, index) => (
                          <tr key={index}>
                            <td>{apt.student_name}</td>
                            <td>{apt.date} {apt.time}</td>
                            <td>{apt.duration}h</td>
                            <td>₹{apt.amount}</td>
                            <td><span className={`badge bg-${apt.status === 'scheduled' ? 'success' : 'warning'}`}>{apt.status}</span></td>
                            <td>
                              <button className="btn btn-sm btn-primary">View Profile</button>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Counsellor Profile Summary */}
        {profileData?.profile && (
          <div className="row">
            <div className="col-12">
              <div className="card border-0 shadow-sm">
                <div className="card-body">
                  <h5 className="card-title mb-3">👤 Your Professional Profile</h5>
                  <div className="row">
                    <div className="col-md-6">
                      <p><strong>Specialization:</strong> {profileData.profile.specialization}</p>
                      <p><strong>Experience:</strong> {profileData.profile.experience} years</p>
                      <p><strong>Education:</strong> {profileData.profile.education}</p>
                    </div>
                    <div className="col-md-6">
                      <p><strong>Hourly Rate:</strong> ₹{profileData.profile.hourly_rate}/hour</p>
                      <p><strong>Rating:</strong> ⭐ {profileData.profile.rating}/5</p>
                      <p><strong>Sessions Conducted:</strong> {profileData.profile.sessions_conducted}</p>
                    </div>
                  </div>
                  {profileData.profile.bio && (
                    <div className="mt-3">
                      <p><strong>Bio:</strong></p>
                      <p className="text-muted">{profileData.profile.bio}</p>
                    </div>
                  )}
                  <button 
                    className="btn btn-primary mt-2"
                    onClick={() => navigate('/profile')}
                  >
                    Edit Profile
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </>
    );
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ minHeight: '80vh' }}>
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading dashboard...</span>
        </div>
      </div>
    );
  }

  const isCounsellor = profileData?.role === 'counsellor';

  return (
    <div className="dashboard-container">
      <div className="container-fluid py-4">
        {/* Welcome Section */}
        <div className="row mb-4">
          <div className="col-12">
            <div className="welcome-card p-4 rounded-3 shadow-sm" style={{
              background: isCounsellor 
                ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                : 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
              color: 'white'
            }}>
              <div className="d-flex justify-content-between align-items-start">
                <div>
                  <h2 className="mb-2">
                    {greeting}, <span className="fw-bold">{profileData?.name || user?.name || 'User'}!</span>
                  </h2>
                  <p className="mb-0" style={{ opacity: 0.9 }}>
                    {isCounsellor 
                      ? `👨‍🏫 Counsellor | ${profileData?.profile?.specialization || 'Not specified'} | ${profileData?.profile?.experience || 0} years experience`
                      : '🎓 Student | Ready to explore your career options?'}
                  </p>
                  {isCounsellor && (
                    <div className="mt-2">
                      <small style={{ opacity: 0.8 }}>
                        📧 {profileData?.email} | 📱 {profileData?.phone}
                      </small>
                    </div>
                  )}
                </div>
                <div className="text-end">
                  <span className={`badge ${isCounsellor ? 'bg-white text-primary' : 'bg-white text-danger'} fs-6 px-3 py-2`}>
                    {isCounsellor ? '👨‍🏫 Counsellor' : '🎓 Student'}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Stats Cards */}
        {isCounsellor ? (
          <div className="row mb-4">
            <div className="col-md-3 mb-3">
              <div className="card border-0 shadow-sm text-center">
                <div className="card-body">
                  <h3 className="text-primary mb-2">{stats.totalSessions}</h3>
                  <p className="text-muted small mb-0">Total Sessions</p>
                </div>
              </div>
            </div>
            <div className="col-md-3 mb-3">
              <div className="card border-0 shadow-sm text-center">
                <div className="card-body">
                  <h3 className="text-success mb-2">{stats.averageRating.toFixed(1)}</h3>
                  <p className="text-muted small mb-0">Average Rating</p>
                </div>
              </div>
            </div>
            <div className="col-md-3 mb-3">
              <div className="card border-0 shadow-sm text-center">
                <div className="card-body">
                  <h3 className="text-warning mb-2">{stats.studentsHelped}</h3>
                  <p className="text-muted small mb-0">Students Helped</p>
                </div>
              </div>
            </div>
            <div className="col-md-3 mb-3">
              <div className="card border-0 shadow-sm text-center">
                <div className="card-body">
                  <h3 className="text-info mb-2">₹{stats.earnings}</h3>
                  <p className="text-muted small mb-0">Total Earnings</p>
                </div>
              </div>
            </div>
          </div>
        ) : null}

        {/* Render appropriate dashboard based on role */}
        {isCounsellor ? <CounsellorDashboard /> : <StudentDashboard />}
      </div>
    </div>
  );
}

export default Dashboard;