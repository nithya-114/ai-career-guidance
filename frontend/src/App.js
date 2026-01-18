import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

// Components
import NavigationBar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';
import Chatbot from './components/Chatbot/Chatbot';
import RegisterCounsellor from './pages/RegisterCounsellor';
import AdminLogin from './pages/AdminLogin';
import CareerListing from './pages/CareerListing';
import CareerDetails from './pages/CareerDetails';
import Quiz from './pages/Quiz';
import Recommendations from './pages/Recommendations';
import CollegeFinder from './pages/CollegeFinder';
import CounsellorDirectory from './pages/CounsellorDirectory';
import ForgotPassword from './components/ForgotPassword';
import AdminDashboard from './pages/AdminDashboard';
import CounsellorDetails from './pages/CounsellorDetails';

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

// Home Route Component
const HomeRoute = () => {
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

  return <Home />;
};

// Admin Route Component (only for admins)
const AdminRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ minHeight: '100vh' }}>
        <div className="spinner-border text-primary"></div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/admin-login" replace />;
  }

  if (user.role !== 'admin') {
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
          {/* Home Route */}
          <Route path="/" element={<HomeRoute />} />
          
          {/* Public Routes */}
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

          {/* Forgot Password Route */}
          <Route 
            path="/forgot-password"
            element={<ForgotPassword />}
          />

          {/* Admin Login Route */}
          <Route 
            path="/admin-login"
            element={
              <PublicRoute>
                <AdminLogin />
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

          {/* Admin Routes */}
          <Route
            path="/admin-dashboard"
            element={
              <AdminRoute>
                <AdminDashboard />
              </AdminRoute>
            }
          />

          {/* Public Career & College Routes */}
          <Route path="/careers" element={<CareerListing />} />
          <Route path="/careers/:id" element={<CareerDetails />} />
          <Route path="/colleges" element={<CollegeFinder />} />
          <Route path="/counsellors" element={<CounsellorDirectory />} />
          <Route path="/counsellors/:id" element={<CounsellorDetails />} />
          {/* 404 Route - Must be last */}
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