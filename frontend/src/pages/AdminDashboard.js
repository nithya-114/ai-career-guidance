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
    activeNow: 0
  });
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/admin/dashboard`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      setStats(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching admin dashboard:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ minHeight: '80vh' }}>
        <div className="spinner-border text-danger" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="container-fluid py-4">
      {/* Welcome Banner */}
      <div className="card shadow-sm mb-4" style={{
        background: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
        border: 'none',
        color: 'white'
      }}>
        <div className="card-body p-4">
          <div className="row align-items-center">
            <div className="col-md-8">
              <h2 className="mb-2">
                <i className="bi bi-shield-check me-2"></i>
                Admin Control Panel
              </h2>
              <p className="mb-0 opacity-75">
                Welcome back, {user?.name} | System Administrator
              </p>
            </div>
            <div className="col-md-4 text-md-end mt-3 mt-md-0">
              <span className="badge bg-light text-dark px-3 py-2">
                <i className="bi bi-clock me-2"></i>
                {new Date().toLocaleDateString('en-US', { 
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
                  <i className="bi bi-people-fill text-primary" style={{ fontSize: '2rem' }}></i>
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
                  <i className="bi bi-mortarboard-fill text-info" style={{ fontSize: '2rem' }}></i>
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
                  <i className="bi bi-person-badge-fill text-success" style={{ fontSize: '2rem' }}></i>
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
                  <i className="bi bi-calendar-check-fill text-warning" style={{ fontSize: '2rem' }}></i>
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
                  <i className="bi bi-briefcase-fill text-purple" style={{ fontSize: '2rem' }}></i>
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
                  <i className="bi bi-building text-danger" style={{ fontSize: '2rem' }}></i>
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
                  <p className="text-muted mb-1">Total Revenue</p>
                  <h3 className="mb-0">₹{stats.revenue.toLocaleString()}</h3>
                </div>
                <div className="bg-success bg-opacity-10 p-3 rounded">
                  <i className="bi bi-currency-rupee text-success" style={{ fontSize: '2rem' }}></i>
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
                  <i className="bi bi-circle-fill text-success" style={{ fontSize: '2rem' }}></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <ul className="nav nav-tabs mb-4">
        <li className="nav-item">
          <button 
            className={`nav-link ${activeTab === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            <i className="bi bi-speedometer2 me-2"></i>Overview
          </button>
        </li>
        <li className="nav-item">
          <button 
            className={`nav-link ${activeTab === 'users' ? 'active' : ''}`}
            onClick={() => setActiveTab('users')}
          >
            <i className="bi bi-people me-2"></i>Users
          </button>
        </li>
        <li className="nav-item">
          <button 
            className={`nav-link ${activeTab === 'counsellors' ? 'active' : ''}`}
            onClick={() => setActiveTab('counsellors')}
          >
            <i className="bi bi-person-badge me-2"></i>Counsellors
          </button>
        </li>
        <li className="nav-item">
          <button 
            className={`nav-link ${activeTab === 'careers' ? 'active' : ''}`}
            onClick={() => setActiveTab('careers')}
          >
            <i className="bi bi-briefcase me-2"></i>Careers
          </button>
        </li>
        <li className="nav-item">
          <button 
            className={`nav-link ${activeTab === 'colleges' ? 'active' : ''}`}
            onClick={() => setActiveTab('colleges')}
          >
            <i className="bi bi-building me-2"></i>Colleges
          </button>
        </li>
      </ul>

      {/* Tab Content */}
      {activeTab === 'overview' && (
        <div className="row g-4">
          {/* Quick Actions */}
          <div className="col-12">
            <h5 className="mb-3">Quick Actions</h5>
            <div className="row g-3">
              <div className="col-md-4">
                <div className="card shadow-sm h-100 hover-shadow" style={{ cursor: 'pointer' }}
                  onClick={() => setActiveTab('users')}>
                  <div className="card-body text-center p-4">
                    <i className="bi bi-people-fill text-primary mb-3" style={{ fontSize: '3rem' }}></i>
                    <h5>Manage Users</h5>
                    <p className="text-muted mb-0">View, edit, and manage all users</p>
                  </div>
                </div>
              </div>

              <div className="col-md-4">
                <div className="card shadow-sm h-100 hover-shadow" style={{ cursor: 'pointer' }}
                  onClick={() => setActiveTab('counsellors')}>
                  <div className="card-body text-center p-4">
                    <i className="bi bi-person-badge-fill text-success mb-3" style={{ fontSize: '3rem' }}></i>
                    <h5>Manage Counsellors</h5>
                    <p className="text-muted mb-0">Approve and monitor counsellors</p>
                  </div>
                </div>
              </div>

              <div className="col-md-4">
                <div className="card shadow-sm h-100 hover-shadow" style={{ cursor: 'pointer' }}
                  onClick={() => setActiveTab('careers')}>
                  <div className="card-body text-center p-4">
                    <i className="bi bi-briefcase-fill text-warning mb-3" style={{ fontSize: '3rem' }}></i>
                    <h5>Manage Careers</h5>
                    <p className="text-muted mb-0">Add, edit, delete career options</p>
                  </div>
                </div>
              </div>

              <div className="col-md-4">
                <div className="card shadow-sm h-100 hover-shadow" style={{ cursor: 'pointer' }}
                  onClick={() => setActiveTab('colleges')}>
                  <div className="card-body text-center p-4">
                    <i className="bi bi-building text-danger mb-3" style={{ fontSize: '3rem' }}></i>
                    <h5>Manage Colleges</h5>
                    <p className="text-muted mb-0">Add, edit, delete colleges</p>
                  </div>
                </div>
              </div>

              <div className="col-md-4">
                <div className="card shadow-sm h-100 hover-shadow" style={{ cursor: 'pointer' }}>
                  <div className="card-body text-center p-4">
                    <i className="bi bi-graph-up text-info mb-3" style={{ fontSize: '3rem' }}></i>
                    <h5>Analytics</h5>
                    <p className="text-muted mb-0">View detailed reports</p>
                  </div>
                </div>
              </div>

              <div className="col-md-4">
                <div className="card shadow-sm h-100 hover-shadow" style={{ cursor: 'pointer' }}>
                  <div className="card-body text-center p-4">
                    <i className="bi bi-gear-fill text-secondary mb-3" style={{ fontSize: '3rem' }}></i>
                    <h5>System Settings</h5>
                    <p className="text-muted mb-0">Configure system settings</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Recent Activity */}
          <div className="col-12">
            <div className="card shadow-sm">
              <div className="card-header bg-white">
                <h5 className="mb-0">
                  <i className="bi bi-clock-history me-2"></i>
                  Recent Activity
                </h5>
              </div>
              <div className="card-body">
                <div className="alert alert-info mb-0">
                  <i className="bi bi-info-circle me-2"></i>
                  Activity tracking coming soon. This will show recent user registrations, sessions, and system events.
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'users' && (
        <div className="card shadow-sm">
          <div className="card-header bg-white d-flex justify-content-between align-items-center">
            <h5 className="mb-0">
              <i className="bi bi-people-fill me-2"></i>
              User Management
            </h5>
            <button className="btn btn-primary btn-sm">
              <i className="bi bi-download me-2"></i>
              Export Users
            </button>
          </div>
          <div className="card-body">
            <div className="alert alert-info">
              <i className="bi bi-info-circle me-2"></i>
              User management interface will be implemented here. Features:
              <ul className="mb-0 mt-2">
                <li>View all users with filters (role, status, date)</li>
                <li>Search users by name, email, username</li>
                <li>Edit user details</li>
                <li>Activate/deactivate accounts</li>
                <li>Delete users</li>
                <li>View user activity history</li>
              </ul>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'counsellors' && (
        <div className="card shadow-sm">
          <div className="card-header bg-white d-flex justify-content-between align-items-center">
            <h5 className="mb-0">
              <i className="bi bi-person-badge-fill me-2"></i>
              Counsellor Management
            </h5>
            <button className="btn btn-success btn-sm">
              <i className="bi bi-download me-2"></i>
              Export Counsellors
            </button>
          </div>
          <div className="card-body">
            <div className="alert alert-success">
              <i className="bi bi-info-circle me-2"></i>
              Counsellor management interface will be implemented here. Features:
              <ul className="mb-0 mt-2">
                <li>View all counsellors with their specializations</li>
                <li>Approve/reject new counsellor applications</li>
                <li>Monitor session counts and ratings</li>
                <li>View earnings and payment history</li>
                <li>Edit counsellor profiles</li>
                <li>Suspend/activate counsellor accounts</li>
                <li>View student feedback and reviews</li>
              </ul>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'careers' && (
        <div className="card shadow-sm">
          <div className="card-header bg-white d-flex justify-content-between align-items-center">
            <h5 className="mb-0">
              <i className="bi bi-briefcase-fill me-2"></i>
              Career Management
            </h5>
            <button className="btn btn-warning btn-sm">
              <i className="bi bi-plus-lg me-2"></i>
              Add New Career
            </button>
          </div>
          <div className="card-body">
            <div className="alert alert-warning">
              <i className="bi bi-info-circle me-2"></i>
              Career management interface will be implemented here. Features:
              <ul className="mb-0 mt-2">
                <li>View all careers with details</li>
                <li>Add new career options</li>
                <li>Edit career details (description, requirements, salary)</li>
                <li>Upload/update career images</li>
                <li>Delete career options</li>
                <li>Categorize careers (Technology, Medical, etc.)</li>
                <li>Set featured careers</li>
              </ul>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'colleges' && (
        <div className="card shadow-sm">
          <div className="card-header bg-white d-flex justify-content-between align-items-center">
            <h5 className="mb-0">
              <i className="bi bi-building me-2"></i>
              College Management
            </h5>
            <button className="btn btn-danger btn-sm">
              <i className="bi bi-plus-lg me-2"></i>
              Add New College
            </button>
          </div>
          <div className="card-body">
            <div className="alert alert-danger">
              <i className="bi bi-info-circle me-2"></i>
              College management interface will be implemented here. Features:
              <ul className="mb-0 mt-2">
                <li>View all colleges with filters (state, type, rating)</li>
                <li>Add new colleges</li>
                <li>Edit college details (courses, fees, location)</li>
                <li>Upload college images and logos</li>
                <li>Delete colleges</li>
                <li>Manage college courses and departments</li>
                <li>Set college rankings and ratings</li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default AdminDashboard;