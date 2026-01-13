import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth APIs - FIXED ENDPOINTS
export const authAPI = {
  register: (data) => api.post('/auth/register', data),  // ← Added /auth/
  login: (data) => api.post('/auth/login', data),        // ← Added /auth/
  getProfile: () => api.get('/user/profile'),            // ← Fixed
  updateProfile: (data) => api.put('/user/profile', data),
};

// Chatbot APIs
export const chatAPI = {
  sendMessage: (data) => api.post('/chat', data),
  getRecommendations: (userId) => api.post('/chat/recommend', { user_id: userId }),
  getChatHistory: (userId) => api.get(`/chat/history/${userId}`),
};

// Career APIs
export const careerAPI = {
  getAllCareers: () => api.get('/careers'),
  getCareerById: (id) => api.get(`/careers/${id}`),
  getCourses: (career) => api.get(`/courses?career=${career}`),
  getColleges: (params) => api.get('/colleges', { params }),
};

// Quiz APIs
export const quizAPI = {
  getQuestions: (type) => api.get(`/quiz/${type}`),
  submitQuiz: (data) => api.post('/quiz/submit', data),
  getResults: (userId) => api.get(`/quiz/results/${userId}`),
};

export default api;