import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';

function AdminDashboard() {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    totalUsers: 0,
    totalStudents: 0,
    totalCounsellors: 0,
    totalSessions: 0,
    totalCareers: 0,
    totalColleges: 0,
    revenue: 0,
    activeNow: 0,
    pendingApprovals: 0
  });
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [users, setUsers] = useState([]);
  const [counsellors, setCounsellors] = useState([]);
  const [careers, setCareers] = useState([]);
  const [colleges, setColleges] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [modalType, setModalType] = useState('');
  const [editItem, setEditItem] = useState(null);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

  useEffect(() => {
    fetchDashboardData();
  }, []);

  useEffect(() => {
    if (activeTab === 'users') fetchUsers();
    if (activeTab === 'counsellors') fetchCounsellors();
    if (activeTab === 'careers') fetchCareers();
    if (activeTab === 'colleges') fetchColleges();
  }, [activeTab]);

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/admin/dashboard`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setStats(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching dashboard:', error);
      setLoading(false);
    }
  };

  const fetchUsers = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/admin/users`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUsers(response.data.users || []);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const fetchCounsellors = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/admin/counsellors`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setCounsellors(response.data.counsellors || []);
    } catch (error) {
      console.error('Error fetching counsellors:', error);
    }
  };

  const fetchCareers = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/admin/careers`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setCareers(response.data.careers || []);
    } catch (error) {
      console.error('Error fetching careers:', error);
    }
  };

  const fetchColleges = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/admin/colleges`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setColleges(response.data.colleges || []);
    } catch (error) {
      console.error('Error fetching colleges:', error);
    }
  };

  const handleDeleteUser = async (userId) => {
    if (!window.confirm('Are you sure you want to delete this user?')) return;
    
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`${API_URL}/admin/users/${userId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert('User deleted successfully');
      fetchUsers();
      fetchDashboardData();
    } catch (error) {
      alert('Failed to delete user: ' + error.response?.data?.error);
    }
  };

  const handleApproveCounsellor = async (counsellorId, approved) => {
    try {
      const token = localStorage.getItem('token');
      await axios.put(`${API_URL}/admin/counsellors/${counsellorId}/approve`, 
        { approved },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert(`Counsellor ${approved ? 'approved' : 'rejected'} successfully`);
      fetchCounsellors();
      fetchDashboardData();
    } catch (error) {
      alert('Failed to update counsellor: ' + error.response?.data?.error);
    }
  };

  const handleDeleteCareer = async (careerId) => {
    if (!window.confirm('Are you sure you want to delete this career?')) return;
    
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`${API_URL}/admin/careers/${careerId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert('Career deleted successfully');
      fetchCareers();
    } catch (error) {
      alert('Failed to delete career: ' + error.response?.data?.error);
    }
  };

  const handleDeleteCollege = async (collegeId) => {
    if (!window.confirm('Are you sure you want to delete this college?')) return;
    
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`${API_URL}/admin/colleges/${collegeId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert('College deleted successfully');
      fetchColleges();
    } catch (error) {
      alert('Failed to delete college: ' + error.response?.data?.error);
    }
  };

  const openAddModal = (type) => {
    setModalType(type);
    setEditItem(null);
    setShowModal(true);
  };

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
      {/* Welcome Banner */}
      <div className="card shadow-sm mb-4" style={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        border: 'none',
        color: 'white'
      }}>
        <div className="card-body p-4">
          <div className="row align-items-center">
            <div className="col-md-8">
              <h2 className="mb-2">
                🛡️ Admin Control Panel
              </h2>
              <p className="mb-0 opacity-75">
                Welcome back, {user?.name} | System Administrator
              </p>
            </div>
            <div className="col-md-4 text-md-end mt-3 mt-md-0">
              <span className="badge bg-light text-dark px-3 py-2">
                🕒 {new Date().toLocaleDateString('en-US', { 
                  weekday: 'short', 
                  month: 'short', 
                  day: 'numeric' 
                })}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="row g-3 mb-4">
        <div className="col-md-3">
          <div className="card shadow-sm h-100">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <p className="text-muted mb-1">Total Users</p>
                  <h3 className="mb-0">{stats.totalUsers}</h3>
                </div>
                <div className="bg-primary bg-opacity-10 p-3 rounded">
                  <span style={{ fontSize: '2rem' }}>👥</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card shadow-sm h-100">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <p className="text-muted mb-1">Students</p>
                  <h3 className="mb-0">{stats.totalStudents}</h3>
                </div>
                <div className="bg-info bg-opacity-10 p-3 rounded">
                  <span style={{ fontSize: '2rem' }}>🎓</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card shadow-sm h-100">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <p className="text-muted mb-1">Counsellors</p>
                  <h3 className="mb-0">{stats.totalCounsellors}</h3>
                </div>
                <div className="bg-success bg-opacity-10 p-3 rounded">
                  <span style={{ fontSize: '2rem' }}>👨‍🏫</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card shadow-sm h-100">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <p className="text-muted mb-1">Total Sessions</p>
                  <h3 className="mb-0">{stats.totalSessions}</h3>
                </div>
                <div className="bg-warning bg-opacity-10 p-3 rounded">
                  <span style={{ fontSize: '2rem' }}>📅</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card shadow-sm h-100">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <p className="text-muted mb-1">Careers</p>
                  <h3 className="mb-0">{stats.totalCareers}</h3>
                </div>
                <div className="bg-purple bg-opacity-10 p-3 rounded">
                  <span style={{ fontSize: '2rem' }}>💼</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card shadow-sm h-100">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <p className="text-muted mb-1">Colleges</p>
                  <h3 className="mb-0">{stats.totalColleges}</h3>
                </div>
                <div className="bg-danger bg-opacity-10 p-3 rounded">
                  <span style={{ fontSize: '2rem' }}>🏫</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card shadow-sm h-100">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <p className="text-muted mb-1">Revenue</p>
                  <h3 className="mb-0">₹{stats.revenue.toLocaleString()}</h3>
                </div>
                <div className="bg-success bg-opacity-10 p-3 rounded">
                  <span style={{ fontSize: '2rem' }}>💰</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card shadow-sm h-100">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <p className="text-muted mb-1">Active Now</p>
                  <h3 className="mb-0">{stats.activeNow}</h3>
                </div>
                <div className="bg-success bg-opacity-10 p-3 rounded">
                  <span style={{ fontSize: '2rem' }}>🟢</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <ul className="nav nav-tabs mb-4">
        {['overview', 'users', 'counsellors', 'careers', 'colleges', 'analytics'].map(tab => (
          <li key={tab} className="nav-item">
            <button 
              className={`nav-link ${activeTab === tab ? 'active' : ''}`}
              onClick={() => setActiveTab(tab)}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          </li>
        ))}
      </ul>

      {/* Tab Content */}
      {activeTab === 'overview' && (
        <div className="row g-4">
          <div className="col-12">
            <h5 className="mb-3">⚡ Quick Actions</h5>
            <div className="row g-3">
              {[
                { icon: '👥', title: 'Manage Users', tab: 'users', color: 'primary' },
                { icon: '👨‍🏫', title: 'Manage Counsellors', tab: 'counsellors', color: 'success' },
                { icon: '💼', title: 'Manage Careers', tab: 'careers', color: 'warning' },
                { icon: '🏫', title: 'Manage Colleges', tab: 'colleges', color: 'danger' },
                { icon: '📊', title: 'View Analytics', tab: 'analytics', color: 'info' },
                { icon: '⚙️', title: 'System Settings', tab: 'settings', color: 'secondary' }
              ].map(action => (
                <div key={action.tab} className="col-md-4">
                  <div 
                    className="card shadow-sm h-100 hover-card" 
                    style={{ cursor: 'pointer' }}
                    onClick={() => setActiveTab(action.tab)}
                  >
                    <div className="card-body text-center p-4">
                      <span style={{ fontSize: '3rem' }}>{action.icon}</span>
                      <h5 className="mt-3">{action.title}</h5>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {activeTab === 'users' && (
        <div className="card shadow-sm">
          <div className="card-header bg-white d-flex justify-content-between align-items-center">
            <h5 className="mb-0">👥 User Management</h5>
            <button className="btn btn-primary btn-sm">
              📥 Export Users
            </button>
          </div>
          <div className="card-body">
            <div className="table-responsive">
              <table className="table table-hover">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Username</th>
                    <th>Role</th>
                    <th>Status</th>
                    <th>Created</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map(user => (
                    <tr key={user._id}>
                      <td>{user.name}</td>
                      <td>{user.email}</td>
                      <td>{user.username}</td>
                      <td>
                        <span className={`badge bg-${user.role === 'student' ? 'info' : 'success'}`}>
                          {user.role}
                        </span>
                      </td>
                      <td>
                        <span className={`badge bg-${user.is_active ? 'success' : 'danger'}`}>
                          {user.is_active ? 'Active' : 'Inactive'}
                        </span>
                      </td>
                      <td>{new Date(user.created_at).toLocaleDateString()}</td>
                      <td>
                        <button 
                          className="btn btn-sm btn-danger"
                          onClick={() => handleDeleteUser(user._id)}
                        >
                          🗑️ Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'counsellors' && (
        <div className="card shadow-sm">
          <div className="card-header bg-white d-flex justify-content-between align-items-center">
            <h5 className="mb-0">👨‍🏫 Counsellor Management</h5>
          </div>
          <div className="card-body">
            <div className="table-responsive">
              <table className="table table-hover">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Specialization</th>
                    <th>Experience</th>
                    <th>Sessions</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {counsellors.map(counsellor => (
                    <tr key={counsellor._id}>
                      <td>{counsellor.name}</td>
                      <td>{counsellor.email}</td>
                      <td>{counsellor.profile?.specialization || 'N/A'}</td>
                      <td>{counsellor.profile?.experience || 0} years</td>
                      <td>{counsellor.total_sessions || 0}</td>
                      <td>
                        <span className={`badge bg-${counsellor.is_active ? 'success' : 'danger'}`}>
                          {counsellor.is_active ? 'Active' : 'Pending'}
                        </span>
                      </td>
                      <td>
                        {!counsellor.is_active && (
                          <button 
                            className="btn btn-sm btn-success me-2"
                            onClick={() => handleApproveCounsellor(counsellor._id, true)}
                          >
                            ✅ Approve
                          </button>
                        )}
                        <button 
                          className="btn btn-sm btn-danger"
                          onClick={() => handleApproveCounsellor(counsellor._id, false)}
                        >
                          ❌ {counsellor.is_active ? 'Deactivate' : 'Reject'}
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'careers' && (
        <div className="card shadow-sm">
          <div className="card-header bg-white d-flex justify-content-between align-items-center">
            <h5 className="mb-0">💼 Career Management</h5>
            <button 
              className="btn btn-primary btn-sm"
              onClick={() => openAddModal('career')}
            >
              ➕ Add Career
            </button>
          </div>
          <div className="card-body">
            <div className="table-responsive">
              <table className="table table-hover">
                <thead>
                  <tr>
                    <th>Title</th>
                    <th>Category</th>
                    <th>Avg Salary</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {careers.map(career => (
                    <tr key={career._id}>
                      <td>{career.name || career.title}</td>
                      <td>{career.category}</td>
                      <td>{career.average_salary || career.salary_range || 'N/A'}</td>
                      <td>
                        <button className="btn btn-sm btn-warning me-2">✏️ Edit</button>
                        <button 
                          className="btn btn-sm btn-danger"
                          onClick={() => handleDeleteCareer(career._id)}
                        >
                          🗑️ Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'colleges' && (
        <div className="card shadow-sm">
          <div className="card-header bg-white d-flex justify-content-between align-items-center">
            <h5 className="mb-0">🏫 College Management</h5>
            <button 
              className="btn btn-primary btn-sm"
              onClick={() => openAddModal('college')}
            >
              ➕ Add College
            </button>
          </div>
          <div className="card-body">
            <div className="table-responsive">
              <table className="table table-hover">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Location</th>
                    <th>Type</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {colleges.map(college => (
                    <tr key={college._id}>
                      <td>{college.name}</td>
                      <td>{college.location}</td>
                      <td>{college.type}</td>
                      <td>
                        <button className="btn btn-sm btn-warning me-2">✏️ Edit</button>
                        <button 
                          className="btn btn-sm btn-danger"
                          onClick={() => handleDeleteCollege(college._id)}
                        >
                          🗑️ Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'analytics' && (
        <div className="card shadow-sm">
          <div className="card-header bg-white">
            <h5 className="mb-0">📊 System Analytics</h5>
          </div>
          <div className="card-body">
            <div className="alert alert-info">
              📈 Analytics dashboard with charts and graphs will be implemented here showing:
              <ul className="mt-2 mb-0">
                <li>User growth over time</li>
                <li>Session bookings trend</li>
                <li>Revenue analytics</li>
                <li>Popular careers and colleges</li>
                <li>Counsellor performance metrics</li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default AdminDashboard;