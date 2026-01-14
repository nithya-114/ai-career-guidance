import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';

function CounsellorDashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [greeting, setGreeting] = useState('');
  const [profileData, setProfileData] = useState(null);
  const [appointments, setAppointments] = useState([]);
  const [stats, setStats] = useState({
    totalSessions: 0,
    averageRating: 4.5,
    studentsHelped: 0,
    earnings: 0,
    todayAppointments: 0,
    pendingPayments: 0
  });
  const [loading, setLoading] = useState(true);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

  useEffect(() => {
    const hour = new Date().getHours();
    if (hour < 12) setGreeting('Good Morning');
    else if (hour < 18) setGreeting('Good Afternoon');
    else setGreeting('Good Evening');

    fetchCounsellorData();
  }, []);

  const fetchCounsellorData = async () => {
    try {
      const token = localStorage.getItem('token');
      
      // Fetch profile
      const profileResponse = await axios.get(`${API_URL}/user/profile`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setProfileData(profileResponse.data);
      
      // Calculate stats from profile
      const profile = profileResponse.data.profile || {};
      setStats({
        totalSessions: profile.sessions_conducted || 0,
        averageRating: profile.rating || 4.5,
        studentsHelped: profile.sessions_conducted || 0,
        earnings: (profile.sessions_conducted || 0) * (profile.hourly_rate || 500),
        todayAppointments: 0,
        pendingPayments: 0
      });

      // TODO: Fetch appointments from backend
      // const appointmentsResponse = await axios.get(`${API_URL}/counsellor/appointments`, {
      //   headers: { Authorization: `Bearer ${token}` }
      // });
      // setAppointments(appointmentsResponse.data.appointments);

      setLoading(false);
    } catch (error) {
      console.error('Error fetching counsellor data:', error);
      setLoading(false);
    }
  };

  const quickActions = [
    {
      icon: '📅',
      title: 'View Schedule',
      description: 'See your upcoming appointments',
      action: () => alert('Schedule feature coming soon!'),
      color: 'primary',
      bgColor: '#e8eaf6'
    },
    {
      icon: '👥',
      title: 'My Students',
      description: 'View your student list',
      action: () => alert('Students list coming soon!'),
      color: 'success',
      bgColor: '#e8f5e9'
    },
    {
      icon: '💰',
      title: 'Earnings',
      description: 'View payment history',
      action: () => alert('Earnings page coming soon!'),
      color: 'warning',
      bgColor: '#fff8e1'
    },
    {
      icon: '📊',
      title: 'Reports',
      description: 'View session reports',
      action: () => alert('Reports coming soon!'),
      color: 'info',
      bgColor: '#e1f5fe'
    },
    {
      icon: '⚙️',
      title: 'Settings',
      description: 'Update your profile',
      action: () => navigate('/profile'),
      color: 'secondary',
      bgColor: '#f3e5f5'
    },
    {
      icon: '💬',
      title: 'Messages',
      description: 'Chat with students',
      action: () => alert('Messaging coming soon!'),
      color: 'danger',
      bgColor: '#fce4ec'
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
      {/* Welcome Section */}
      <div className="row mb-4">
        <div className="col-12">
          <div className="p-4 rounded-3 shadow-sm" style={{
            background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', color: 'white'
          }}>
            <h2 className="mb-2">{greeting}, <span className="fw-bold">{profileData?.name}!</span></h2>
            <p className="mb-0">
              Specialization: {profileData?.profile?.specialization || 'Not specified'} | 
              Experience: {profileData?.profile?.experience || 0} years | 
              Rate: ₹{profileData?.profile?.hourly_rate || 500}/hour
            </p>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="row mb-4">
        <div className="col-md-3 mb-3">
          <div className="card border-0 shadow-sm">
            <div className="card-body text-center">
              <h3 className="text-primary mb-2">{stats.totalSessions}</h3>
              <p className="text-muted small mb-0">Total Sessions</p>
            </div>
          </div>
        </div>
        <div className="col-md-3 mb-3">
          <div className="card border-0 shadow-sm">
            <div className="card-body text-center">
              <h3 className="text-success mb-2">⭐ {stats.averageRating.toFixed(1)}</h3>
              <p className="text-muted small mb-0">Average Rating</p>
            </div>
          </div>
        </div>
        <div className="col-md-3 mb-3">
          <div className="card border-0 shadow-sm">
            <div className="card-body text-center">
              <h3 className="text-warning mb-2">{stats.studentsHelped}</h3>
              <p className="text-muted small mb-0">Students Helped</p>
            </div>
          </div>
        </div>
        <div className="col-md-3 mb-3">
          <div className="card border-0 shadow-sm">
            <div className="card-body text-center">
              <h3 className="text-info mb-2">₹{stats.earnings}</h3>
              <p className="text-muted small mb-0">Total Earnings</p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
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
                <button className={`btn btn-${action.color} btn-sm mt-2`}>Open</button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Today's Schedule */}
      <div className="row">
        <div className="col-lg-8 mb-4">
          <div className="card border-0 shadow-sm">
            <div className="card-body">
              <h5 className="card-title mb-4">Today's Appointments</h5>
              {appointments.length === 0 ? (
                <div className="text-center py-5 text-muted">
                  <p className="mb-0">No appointments scheduled for today</p>
                  <small>Students will appear here after booking sessions</small>
                </div>
              ) : (
                <div className="table-responsive">
                  <table className="table">
                    <thead>
                      <tr>
                        <th>Time</th>
                        <th>Student</th>
                        <th>Status</th>
                        <th>Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      {appointments.map((apt, index) => (
                        <tr key={index}>
                          <td>{apt.time}</td>
                          <td>{apt.student_name}</td>
                          <td><span className="badge bg-success">Confirmed</span></td>
                          <td><button className="btn btn-sm btn-primary">View</button></td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Profile Summary */}
        <div className="col-lg-4 mb-4">
          <div className="card border-0 shadow-sm">
            <div className="card-body">
              <h5 className="card-title mb-4">Your Profile</h5>
              <p><strong>Specialization:</strong><br/>{profileData?.profile?.specialization}</p>
              <p><strong>Experience:</strong><br/>{profileData?.profile?.experience} years</p>
              <p><strong>Education:</strong><br/>{profileData?.profile?.education}</p>
              <p><strong>Hourly Rate:</strong><br/>₹{profileData?.profile?.hourly_rate}</p>
              <button className="btn btn-primary w-100 mt-2" onClick={() => navigate('/profile')}>
                Edit Profile
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CounsellorDashboard;