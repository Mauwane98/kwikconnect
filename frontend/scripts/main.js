// frontend/scripts/main.js

document.addEventListener('DOMContentLoaded', () => {
    // Register the Service Worker
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/service-worker.js')
            .then(registration => console.log('Service Worker registered successfully:', registration))
            .catch(error => console.log('Service Worker registration failed:', error));
    }

    // Simple client-side router
    const appRoot = document.getElementById('app-root');

    const loadDashboard = async (dashboardPath) => {
        try {
            const response = await fetch(dashboardPath);
            if (!response.ok) throw new Error('Dashboard not found');
            const content = await response.text();
            appRoot.innerHTML = content;
        } catch (error) {
            console.error('Failed to load dashboard:', error);
            appRoot.innerHTML = `<p class="text-center text-red-500">Error loading page.</p>`;
        }
    };

    import { isAuthenticated, getUserRole } from './auth.js';

    // Routing logic
    if (isAuthenticated()) {
        const userRole = getUserRole();
        switch (userRole) {
            case 'vendor':
                loadDashboard('/dashboards/vendor_dashboard.html');
                break;
            case 'courier':
                loadDashboard('/dashboards/courier_dashboard.html');
                break;
            case 'admin':
                loadDashboard('/dashboards/admin_dashboard.html');
                break;
            case 'customer':
            default:
                loadDashboard('/dashboards/customer_dashboard.html');
                break;
        }
    } else {
        loadDashboard('/landing.html');
    }

    // Event listeners for landing page buttons (if landing.html is loaded)
    document.addEventListener('click', (event) => {
        if (event.target.id === 'login-button') {
            console.log('Login button clicked');
            // In a real app, this would redirect to a login page or show a login modal
            alert('Login functionality not yet implemented.');
        } else if (event.target.id === 'signup-button') {
            console.log('Sign Up button clicked');
            // In a real app, this would redirect to a signup page or show a signup modal
            alert('Sign Up functionality not yet implemented.');
        }
    });
});