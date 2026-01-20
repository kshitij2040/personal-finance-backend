/**
 * API client for making requests to the Django backend
 */
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Expense API calls
export const expenseAPI = {
    getAll: () => api.get('/api/expenses/'),
    create: (data) => api.post('/api/expenses/', data),
    update: (id, data) => api.put(`/api/expenses/${id}/`, data),
    delete: (id) => api.delete(`/api/expenses/${id}/`),
    getSummary: () => api.get('/api/expenses/summary/'),
    getMonthly: () => api.get('/api/expenses/monthly/'),
};

// Income API calls
export const incomeAPI = {
    getAll: () => api.get('/api/income/'),
    create: (data) => api.post('/api/income/', data),
    update: (id, data) => api.put(`/api/income/${id}/`, data),
    delete: (id) => api.delete(`/api/income/${id}/`),
    getSummary: () => api.get('/api/income/summary/'),
    getMonthly: () => api.get('/api/income/monthly/'),
};

// User/Budget API calls
export const budgetAPI = {
    getOverview: () => api.get('/api/users/overview/'),
    getAIInsights: () => api.post('/api/users/ai-insights/'),
};

export default api;
