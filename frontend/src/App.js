import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

// Components - All using default imports
import NavigationBar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';
import Chatbot from './components/Chatbot/Chatbot';
import RegisterCounsellor from './pages/RegisterCounsellor';
import CareerListing from './pages/CareerListing';
import CareerDetails from './pages/CareerDetails';
import Quiz from './pages/Quiz';
import Recommendations from './pages/Recommendations';
import CollegeFinder from './pages/CollegeFinder';
import CounsellorDirectory from './pages/CounsellorDirectory';

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ minHeight: '100vh' }}>
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

// Public Route Component (redirect if already logged in)
const PublicRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ minHeight: '100vh' }}>
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  if (user) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

// 404 Not Found Component
const NotFound = () => (
  <div className="d-flex flex-column justify-content-center align-items-center" style={{ minHeight: '80vh' }}>
    <h1 className="display-1 fw-bold text-primary">404</h1>
    <h2 className="mb-3">Page Not Found</h2>
    <p className="lead">The page you're looking for doesn't exist.</p>
    <a href="/" className="btn btn-primary mt-3">Go Home</a>
  </div>
);

function AppContent() {
  return (
    <Router>
      <div className="App">
        <NavigationBar />
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<Home />} />
          
          <Route 
            path="/login" 
            element={
              <PublicRoute>
                <Login />
              </PublicRoute>
            } 
          />
          
          <Route 
            path="/register" 
            element={
              <PublicRoute>
                <Register />
              </PublicRoute>
            } 
          />
          
          <Route 
            path="/register-counsellor"
            element={
              <PublicRoute>
                <RegisterCounsellor />
              </PublicRoute>
            } 
          />

          {/* Protected Routes */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />

          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            }
          />

          <Route
            path="/chat"
            element={
              <ProtectedRoute>
                <Chatbot />
              </ProtectedRoute>
            }
          />

          {/* Career Routes */}
          <Route path="/careers" element={<CareerListing />} />
          <Route path="/careers/:id" element={<CareerDetails />} />
          
          {/* Quiz & Recommendations */}
          <Route 
            path="/quiz" 
            element={
              <ProtectedRoute>
                <Quiz />
              </ProtectedRoute>
            } 
          />
          
          <Route 
            path="/recommendations" 
            element={
              <ProtectedRoute>
                <Recommendations />
              </ProtectedRoute>
            } 
          />
          
          {/* College Finder */}
          <Route path="/colleges" element={<CollegeFinder />} />
          
          {/* Counsellors */}
          <Route path="/counsellors" element={<CounsellorDirectory />} />
          
          {/* 404 Route */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </Router>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;