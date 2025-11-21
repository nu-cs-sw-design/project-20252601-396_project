/**
 * API Service - Handles all API calls to the backend
 */
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API endpoints
export const api = {
  // Test endpoint
  test: () => apiClient.get('/test'),
  
  // Add more API endpoints here as needed
  // Example:
  // getMenu: () => apiClient.get('/menu'),
  // createOrder: (orderData) => apiClient.post('/orders', orderData),
};

export default apiClient;

