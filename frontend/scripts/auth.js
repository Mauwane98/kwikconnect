// frontend/scripts/auth.js

export const isAuthenticated = () => {
    const token = localStorage.getItem('jwt_token');
    const userRole = localStorage.getItem('user_role');
    return token && userRole;
};

export const getUserRole = () => {
    return localStorage.getItem('user_role');
};

export const login = (token, role) => {
    localStorage.setItem('jwt_token', token);
    localStorage.setItem('user_role', role);
    // In a real app, you would redirect to the appropriate dashboard
    console.log('User logged in:', role);
};

export const logout = () => {
    localStorage.removeItem('jwt_token');
    localStorage.removeItem('user_role');
    // In a real app, you would redirect to the landing page
    console.log('User logged out');
};
