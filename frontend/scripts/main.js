// frontend/scripts/main.js

document.addEventListener('DOMContentLoaded', () => {
    // Register the Service Worker
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/service-worker.js')
            .then(registration => console.log('Service Worker registered successfully:', registration))
            .catch(error => console.log('Service Worker registration failed:', error));
    }
});