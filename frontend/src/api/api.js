import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if it exists
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle response errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear token on unauthorized
      localStorage.removeItem('authToken');
      localStorage.removeItem('currentUser');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Authentication APIs
export const authAPI = {
  register: (username, email, password) =>
    apiClient.post('/auth/register', { username, email, password }),
  
  login: (username, password) =>
    apiClient.post('/auth/login', { username, password }),
  
  logout: () =>
    apiClient.post('/auth/logout'),
  
  verifyToken: () =>
    apiClient.get('/auth/verify-token'),
  
  getProfile: () =>
    apiClient.get('/auth/profile'),
  
  updateProfile: (data) =>
    apiClient.put('/auth/profile', data),
};

// Recommendation APIs
export const recommendationAPI = {
  getRecommendations: (city, maxBudget, tenantType, bhk, topN = 5) => {
    const params = {
      city,
      ...(maxBudget !== undefined && { max_budget: maxBudget }),
      ...(tenantType !== undefined && tenantType !== null && { tenant_type: tenantType }),
      ...(bhk !== undefined && bhk !== null && { bhk }),
      ...(topN && { top_n: topN }),
    };
    return apiClient.get('/recommend', { params });
  },
  
  getPGDetails: (pgId) =>
    apiClient.get(`/pg/${pgId}`),
  
  filterPGs: (filters) =>
    apiClient.get('/filter', { params: filters }),
  
  getCities: () =>
    apiClient.get('/cities'),
  
  getLocalities: (city) =>
    apiClient.get(`/localities/${city}`),
  
  getStats: () =>
    apiClient.get('/stats'),
};

export default apiClient;
