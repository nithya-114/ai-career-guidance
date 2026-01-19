// src/services/api.js - FIXED VERSION

import axios from 'axios';

// Base API URL
const API_URL = 'http://localhost:5000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for better error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// ==================== AUTHENTICATION ====================

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  checkUsername: (username) => api.post('/auth/check-username', { username }),
  checkEmail: (email) => api.post('/auth/check-email', { email }),
  forgotPassword: (email) => api.post('/auth/forgot-password', { email }),
  verifyResetCode: (email, code) => api.post('/auth/verify-reset-code', { email, code }),
  resetPassword: (data) => api.post('/auth/reset-password', data),
  verifyToken: () => api.get('/auth/verify-token'),
};

// ==================== USER PROFILE ====================

export const userAPI = {
  getProfile: () => api.get('/user/profile'),
  updateProfile: (data) => api.put('/user/profile', data),
};

// ==================== CAREERS ====================

export const careerAPI = {
  getAll: (params) => api.get('/careers', { params }),
  getById: (id) => api.get(`/careers/${id}`),
};

// ==================== COLLEGES ====================

export const collegeAPI = {
  getAll: (params) => api.get('/colleges', { params }),
  getById: (id) => api.get(`/colleges/${id}`),
  getStats: () => api.get('/colleges/stats'),
};

// ==================== COURSES ====================

export const courseAPI = {
  getAll: () => api.get('/courses'),
};

// ==================== COUNSELLORS ====================

export const counsellorAPI = {
  getAll: () => api.get('/counsellors'),
  getById: (id) => api.get(`/counsellors/${id}`),
  getAvailability: (id, date) => api.get(`/counsellors/${id}/availability`, { 
    params: { date } 
  }),
};

// ==================== CHAT ====================

export const chatAPI = {
  sendMessage: (data) => {
    console.log('Calling chat endpoint:', `${API_URL}/chat/send`);
    return api.post('/chat/send', data);
  },
  
  getHistory: (sessionId) => api.get(`/chat/history/${sessionId}`),
  
  clearSession: (sessionId) => api.delete(`/chat/session/${sessionId}`),
};

// ==================== RECOMMENDATIONS ====================

export const recommendationAPI = {
  get: () => api.get('/recommendations'),
};

// ==================== QUIZ ====================

export const quizAPI = {
  getQuiz: () => api.get('/quiz'),
  submitQuiz: (data) => api.post('/quiz/submit', data),
  getResults: (id) => api.get(`/quiz/results/${id}`),
};

// ==================== APPOINTMENTS ====================

export const appointmentAPI = {
  create: (data) => api.post('/appointments', data),
  getAll: (params) => api.get('/appointments', { params }),
  getById: (id) => api.get(`/appointments/${id}`),
  cancel: (id) => api.put(`/appointments/${id}/cancel`),
  complete: (id, data) => api.put(`/appointments/${id}/complete`, data),
  rate: (id, data) => api.post(`/appointments/${id}/rate`, data),
};

// ==================== PAYMENT - FIXED ====================

export const paymentAPI = {
  createOrder: (data) => {
    console.log('Creating payment order:', data);
    return api.post('/payment/create-order', data);
  },
  
  // FIXED: Changed from /payment/verify to /payment/verify-payment
  verifyPayment: (data) => {
    console.log('Verifying payment:', data);
    return api.post('/payment/verify-payment', data);
  },
  
  getPaymentStatus: (orderId) => api.get(`/payment/payment-status/${orderId}`),
  
  getMyBookings: () => api.get('/payment/my-bookings'),
};

// ==================== HEALTH CHECK ====================

export const healthAPI = {
  check: () => api.get('/health'),
};

// Export default api instance
export default api;