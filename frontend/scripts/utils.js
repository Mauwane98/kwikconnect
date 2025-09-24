// frontend/scripts/utils.js

export const API_BASE_URL = 'http://localhost:5000/api/v1'; // Adjust if your backend runs on a different port or domain

export const apiRequest = async (endpoint, method = 'GET', data = null, authRequired = true) => {
    const headers = {
        'Content-Type': 'application/json',
    };

    if (authRequired) {
        const token = localStorage.getItem('jwt_token');
        if (!token) {
            // Redirect to login or handle unauthorized access
            console.error('Authentication token not found.');
            window.location.href = '/landing.html'; // Redirect to landing page
            return null; 
        }
        headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
        method: method,
        headers: headers,
    };

    if (data) {
        config.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        const responseData = await response.json();

        if (!response.ok) {
            // Handle API errors
            console.error(`API Error: ${response.status} - ${responseData.message || response.statusText}`);
            return { error: responseData.message || 'An error occurred', status: response.status };
        }

        return responseData;
    } catch (error) {
        console.error('Network or unexpected error:', error);
        return { error: 'Network error or unexpected issue', status: 500 };
    }
};
