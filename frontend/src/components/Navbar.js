import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function NavigationBar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark" style={{ 
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    }}>
      <div className="container-fluid">
        {/* Logo/Brand */}
        <Link className="navbar-brand fw-bold" to={user ? "/dashboard" : "/"}>
          <i className="bi bi-mortarboard-fill me-2"></i>
          CareerGuide AI
        </Link>

        {/* Mobile Toggle */}
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        {/* Navigation Links */}
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto align-items-center">
            {!user ? (
              // NOT LOGGED IN
              <>
                <li className="nav-item">
                  <Link className="nav-link" to="/">Home</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/careers">Careers</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/colleges">Colleges</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link btn btn-light text-primary px-3 ms-2" to="/login">
                    Login
                  </Link>
                </li>
                <li className="nav-item ms-2">
                  <Link className="nav-link btn btn-outline-light px-3" to="/register">
                    Register
                  </Link>
                </li>
              </>
            ) : user.role === 'counsellor' ? (
              // COUNSELLOR - Dashboard only
              <>
                <li className="nav-item">
                  <Link className="nav-link" to="/dashboard">
                    <i className="bi bi-speedometer2 me-1"></i>
                    Dashboard
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/profile">
                    <i className="bi bi-person-circle me-1"></i>
                    {user.name}
                  </Link>
                </li>
                <li className="nav-item">
                  <button 
                    className="btn btn-outline-light btn-sm ms-2"
                    onClick={handleLogout}
                  >
                    <i className="bi bi-box-arrow-right me-1"></i>
                    Logout
                  </button>
                </li>
              </>
            ) : user.role === 'admin' ? (
              // ADMIN - Dashboard only (no careers/colleges browsing)
              <>
                <li className="nav-item">
                  <Link className="nav-link" to="/dashboard">
                    <i className="bi bi-speedometer2 me-1"></i>
                    Dashboard
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/profile">
                    <i className="bi bi-person-circle me-1"></i>
                    {user.name}
                  </Link>
                </li>
                <li className="nav-item">
                  <button 
                    className="btn btn-outline-light btn-sm ms-2"
                    onClick={handleLogout}
                  >
                    <i className="bi bi-box-arrow-right me-1"></i>
                    Logout
                  </button>
                </li>
              </>
            ) : (
              // STUDENT - Full access
              <>
                <li className="nav-item">
                  <Link className="nav-link" to="/careers">Careers</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/colleges">Colleges</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/dashboard">Dashboard</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/chat">Chat</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/profile">
                    <i className="bi bi-person-circle me-1"></i>
                    {user.name}
                  </Link>
                </li>
                <li className="nav-item">
                  <button 
                    className="btn btn-outline-light btn-sm ms-2"
                    onClick={handleLogout}
                  >
                    <i className="bi bi-box-arrow-right me-1"></i>
                    Logout
                  </button>
                </li>
              </>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default NavigationBar;