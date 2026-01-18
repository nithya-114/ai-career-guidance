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
  const [formData, setFormData] = useState({});

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

  const getAuthHeaders = () => {
    const token = localStorage.getItem('token');
    return {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    };
  };

  const fetchDashboardData = async () => {
    try {
      const response = await axios.get(`${API_URL}/admin/dashboard`, {
        headers: getAuthHeaders()
      });
      setStats(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching dashboard:', error);
      alert('Failed to load dashboard data: ' + (error.response?.data?.error || error.message));
      setLoading(false);
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await axios.get(`${API_URL}/admin/users`, {
        headers: getAuthHeaders()
      });
      setUsers(response.data.users || []);
    } catch (error) {
      console.error('Error fetching users:', error);
      alert('Failed to load users: ' + (error.response?.data?.error || error.message));
    }
  };

  const fetchCounsellors = async () => {
    try {
      const response = await axios.get(`${API_URL}/admin/counsellors`, {
        headers: getAuthHeaders()
      });
      setCounsellors(response.data.counsellors || []);
    } catch (error) {
      console.error('Error fetching counsellors:', error);
      alert('Failed to load counsellors: ' + (error.response?.data?.error || error.message));
    }
  };

  const fetchCareers = async () => {
    try {
      const response = await axios.get(`${API_URL}/admin/careers`, {
        headers: getAuthHeaders()
      });
      setCareers(response.data.careers || []);
    } catch (error) {
      console.error('Error fetching careers:', error);
      alert('Failed to load careers: ' + (error.response?.data?.error || error.message));
    }
  };

  const fetchColleges = async () => {
    try {
      const response = await axios.get(`${API_URL}/admin/colleges`, {
        headers: getAuthHeaders()
      });
      setColleges(response.data.colleges || []);
    } catch (error) {
      console.error('Error fetching colleges:', error);
      alert('Failed to load colleges: ' + (error.response?.data?.error || error.message));
    }
  };

  const handleDeleteUser = async (userId) => {
    if (!window.confirm('Are you sure you want to delete this user?')) return;
    
    try {
      await axios.delete(`${API_URL}/admin/users/${userId}`, {
        headers: getAuthHeaders()
      });
      alert('User deleted successfully');
      fetchUsers();
      fetchDashboardData();
    } catch (error) {
      alert('Failed to delete user: ' + (error.response?.data?.error || error.message));
    }
  };

  const handleApproveCounsellor = async (counsellorId, approved) => {
    try {
      await axios.put(
        `${API_URL}/admin/counsellors/${counsellorId}/approve`, 
        { approved },
        { headers: getAuthHeaders() }
      );
      alert(`Counsellor ${approved ? 'approved' : 'rejected'} successfully`);
      fetchCounsellors();
      fetchDashboardData();
    } catch (error) {
      alert('Failed to update counsellor: ' + (error.response?.data?.error || error.message));
    }
  };

  const handleDeleteCareer = async (careerId) => {
    if (!window.confirm('Are you sure you want to delete this career?')) return;
    
    try {
      await axios.delete(`${API_URL}/admin/careers/${careerId}`, {
        headers: getAuthHeaders()
      });
      alert('Career deleted successfully');
      fetchCareers();
      fetchDashboardData();
    } catch (error) {
      alert('Failed to delete career: ' + (error.response?.data?.error || error.message));
    }
  };

  const handleDeleteCollege = async (collegeId) => {
    if (!window.confirm('Are you sure you want to delete this college?')) return;
    
    try {
      await axios.delete(`${API_URL}/admin/colleges/${collegeId}`, {
        headers: getAuthHeaders()
      });
      alert('College deleted successfully');
      fetchColleges();
      fetchDashboardData();
    } catch (error) {
      alert('Failed to delete college: ' + (error.response?.data?.error || error.message));
    }
  };

  const openAddModal = (type) => {
    setModalType(type);
    setEditItem(null);
    setFormData({});
    setShowModal(true);
  };

  const handleModalInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleAddCollege = async (e) => {
    e.preventDefault();
    
    try {
      await axios.post(`${API_URL}/admin/colleges`, formData, {
        headers: getAuthHeaders()
      });
      alert('College added successfully');
      setShowModal(false);
      setFormData({});
      fetchColleges();
      fetchDashboardData();
    } catch (error) {
      alert('Failed to add college: ' + (error.response?.data?.error || error.message));
    }
  };

  const handleAddCareer = async (e) => {
    e.preventDefault();
    
    try {
      await axios.post(`${API_URL}/admin/careers`, formData, {
        headers: getAuthHeaders()
      });
      alert('Career added successfully');
      setShowModal(false);
      setFormData({});
      fetchCareers();
      fetchDashboardData();
    } catch (error) {
      alert('Failed to add career: ' + (error.response?.data?.error || error.message));
    }
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
              <h2 className="mb-2">🛡️ Admin Control Panel</h2>
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
                  <h3 className="mb-0">₹{stats.revenue?.toLocaleString() || 0}</h3>
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
                  <h3 className="mb-0">{stats.activeNow || 0}</h3>
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
                { icon: '📊', title: 'View Analytics', tab: 'analytics', color: 'info' }
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
            <button className="btn btn-primary btn-sm" onClick={() => fetchUsers()}>
              🔄 Refresh
            </button>
          </div>
          <div className="card-body">
            {users.length === 0 ? (
              <div className="alert alert-info">No users found</div>
            ) : (
              <div className="table-responsive">
                <table className="table table-hover">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Email</th>
                      <th>Username</th>
                      <th>Role</th>
                      <th>Status</th>
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
                          <span className={`badge bg-${user.role === 'student' ? 'info' : user.role === 'admin' ? 'danger' : 'success'}`}>
                            {user.role}
                          </span>
                        </td>
                        <td>
                          <span className={`badge bg-${user.is_active ? 'success' : 'secondary'}`}>
                            {user.is_active ? 'Active' : 'Inactive'}
                          </span>
                        </td>
                        <td>
                          <button 
                            className="btn btn-sm btn-danger"
                            onClick={() => handleDeleteUser(user._id)}
                            disabled={user.role === 'admin'}
                          >
                            🗑️ Delete
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      )}

      {activeTab === 'counsellors' && (
        <div className="card shadow-sm">
          <div className="card-header bg-white d-flex justify-content-between align-items-center">
            <h5 className="mb-0">👨‍🏫 Counsellor Management</h5>
            <button className="btn btn-primary btn-sm" onClick={() => fetchCounsellors()}>
              🔄 Refresh
            </button>
          </div>
          <div className="card-body">
            {counsellors.length === 0 ? (
              <div className="alert alert-info">No counsellors found</div>
            ) : (
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
                          <span className={`badge bg-${counsellor.is_active ? 'success' : 'warning'}`}>
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
            )}
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
            {careers.length === 0 ? (
              <div className="alert alert-info">No careers found. Click "Add Career" to create one.</div>
            ) : (
              <div className="table-responsive">
                <table className="table table-hover">
                  <thead>
                    <tr>
                      <th>Title</th>
                      <th>Category</th>
                      <th>Description</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {careers.map(career => (
                      <tr key={career._id}>
                        <td>{career.title || career.name}</td>
                        <td>{career.category}</td>
                        <td>{(career.description || '').substring(0, 100)}...</td>
                        <td>
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
            )}
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
            {colleges.length === 0 ? (
              <div className="alert alert-info">No colleges found. Click "Add College" to create one.</div>
            ) : (
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
            )}
          </div>
        </div>
      )}

      {activeTab === 'analytics' && (
        <div className="card shadow-sm">
          <div className="card-header bg-white">
            <h5 className="mb-0">📊 System Analytics</h5>
          </div>
          <div className="card-body">
            <div className="row g-3">
              <div className="col-md-6">
                <div className="card">
                  <div className="card-body">
                    <h6 className="card-title">📈 User Statistics</h6>
                    <ul className="list-group list-group-flush">
                      <li className="list-group-item d-flex justify-content-between">
                        <span>Total Users</span>
                        <strong>{stats.totalUsers}</strong>
                      </li>
                      <li className="list-group-item d-flex justify-content-between">
                        <span>Students</span>
                        <strong>{stats.totalStudents}</strong>
                      </li>
                      <li className="list-group-item d-flex justify-content-between">
                        <span>Counsellors</span>
                        <strong>{stats.totalCounsellors}</strong>
                      </li>
                      <li className="list-group-item d-flex justify-content-between">
                        <span>Active Now</span>
                        <strong>{stats.activeNow || 0}</strong>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
              
              <div className="col-md-6">
                <div className="card">
                  <div className="card-body">
                    <h6 className="card-title">💰 Financial Overview</h6>
                    <ul className="list-group list-group-flush">
                      <li className="list-group-item d-flex justify-content-between">
                        <span>Total Revenue</span>
                        <strong>₹{stats.revenue?.toLocaleString() || 0}</strong>
                      </li>
                      <li className="list-group-item d-flex justify-content-between">
                        <span>Total Sessions</span>
                        <strong>{stats.totalSessions}</strong>
                      </li>
                      <li className="list-group-item d-flex justify-content-between">
                        <span>Avg. per Session</span>
                        <strong>
                          ₹{stats.totalSessions > 0 
                            ? Math.round(stats.revenue / stats.totalSessions).toLocaleString() 
                            : 0}
                        </strong>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>

              <div className="col-md-6">
                <div className="card">
                  <div className="card-body">
                    <h6 className="card-title">📚 Content Statistics</h6>
                    <ul className="list-group list-group-flush">
                      <li className="list-group-item d-flex justify-content-between">
                        <span>Total Careers</span>
                        <strong>{stats.totalCareers}</strong>
                      </li>
                      <li className="list-group-item d-flex justify-content-between">
                        <span>Total Colleges</span>
                        <strong>{stats.totalColleges}</strong>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>

              <div className="col-md-6">
                <div className="card">
                  <div className="card-body">
                    <h6 className="card-title">⚠️ Pending Actions</h6>
                    <ul className="list-group list-group-flush">
                      <li className="list-group-item d-flex justify-content-between">
                        <span>Pending Counsellor Approvals</span>
                        <strong className="text-warning">{stats.pendingApprovals || 0}</strong>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Add Modal */}
      {showModal && (
        <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">
                  {modalType === 'college' ? '🏫 Add New College' : '💼 Add New Career'}
                </h5>
                <button 
                  type="button" 
                  className="btn-close" 
                  onClick={() => setShowModal(false)}
                ></button>
              </div>
              <div className="modal-body">
                {modalType === 'college' ? (
                  <form onSubmit={handleAddCollege}>
                    <div className="mb-3">
                      <label className="form-label">College Name *</label>
                      <input
                        type="text"
                        className="form-control"
                        name="name"
                        value={formData.name || ''}
                        onChange={handleModalInputChange}
                        required
                      />
                    </div>
                    <div className="mb-3">
                      <label className="form-label">Location *</label>
                      <input
                        type="text"
                        className="form-control"
                        name="location"
                        value={formData.location || ''}
                        onChange={handleModalInputChange}
                        required
                      />
                    </div>
                    <div className="mb-3">
                      <label className="form-label">Type *</label>
                      <select
                        className="form-control"
                        name="type"
                        value={formData.type || ''}
                        onChange={handleModalInputChange}
                        required
                      >
                        <option value="">Select Type</option>
                        <option value="Engineering">Engineering</option>
                        <option value="Medical">Medical</option>
                        <option value="Arts & Science">Arts & Science</option>
                        <option value="Management">Management</option>
                        <option value="Law">Law</option>
                        <option value="Other">Other</option>
                      </select>
                    </div>
                    <div className="mb-3">
                      <label className="form-label">Description</label>
                      <textarea
                        className="form-control"
                        name="description"
                        value={formData.description || ''}
                        onChange={handleModalInputChange}
                        rows="3"
                      ></textarea>
                    </div>
                    <button type="submit" className="btn btn-primary">Add College</button>
                  </form>
                ) : (
                  <form onSubmit={handleAddCareer}>
                    <div className="mb-3">
                      <label className="form-label">Career Title *</label>
                      <input
                        type="text"
                        className="form-control"
                        name="title"
                        value={formData.title || ''}
                        onChange={handleModalInputChange}
                        required
                      />
                    </div>
                    <div className="mb-3">
                      <label className="form-label">Category *</label>
                      <select
                        className="form-control"
                        name="category"
                        value={formData.category || ''}
                        onChange={handleModalInputChange}
                        required
                      >
                        <option value="">Select Category</option>
                        <option value="Technology">Technology</option>
                        <option value="Healthcare">Healthcare</option>
                        <option value="Business">Business</option>
                        <option value="Engineering">Engineering</option>
                        <option value="Arts">Arts</option>
                        <option value="Science">Science</option>
                        <option value="Other">Other</option>
                      </select>
                    </div>
                    <div className="mb-3">
                      <label className="form-label">Description *</label>
                      <textarea
                        className="form-control"
                        name="description"
                        value={formData.description || ''}
                        onChange={handleModalInputChange}
                        rows="4"
                        required
                      ></textarea>
                    </div>
                    <button type="submit" className="btn btn-primary">Add Career</button>
                  </form>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default AdminDashboard;