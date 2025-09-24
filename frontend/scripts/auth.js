// frontend/scripts/auth.js

import { apiRequest } from './utils.js';

export const isAuthenticated = () => {
    const token = localStorage.getItem('jwt_token');
    const userRole = localStorage.getItem('user_role');
    return token && userRole;
};

export const getUserRole = () => {
    return localStorage.getItem('user_role');
};

export const setAuthData = (token, role) => {
    localStorage.setItem('jwt_token', token);
    localStorage.setItem('user_role', role);
};

export const clearAuthData = () => {
    localStorage.removeItem('jwt_token');
    localStorage.removeItem('user_role');
};

export const loginUser = async (email, password) => {
    const response = await apiRequest('/auth/login', 'POST', { email, password }, false);
    if (response && !response.error) {
        setAuthData(response.access_token, response.role);
    }
    return response;
};

export const registerUser = async (username, email, password, role) => {
    const response = await apiRequest('/auth/register', 'POST', { username, email, password, role }, false);
    return response;
};

export const logoutUser = async () => {
    // Optionally call backend logout endpoint if needed
    // await apiRequest('/auth/logout', 'POST'); 
    clearAuthData();
    console.log('User logged out');
    window.location.href = '/landing.html'; // Redirect to landing page after logout
};
