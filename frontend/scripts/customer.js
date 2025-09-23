document.addEventListener('DOMContentLoaded', () => {
    const categoriesContainer = document.getElementById('categories-container');
    const vendorsGrid = document.getElementById('vendors-grid');
    const categoryCardTemplate = document.getElementById('category-card-template');
    const vendorCardTemplate = document.getElementById('vendor-card-template');

    // Mock Data (replace with API calls later)
    const mockCategories = [
        { id: 1, name: 'Groceries', image: 'https://via.placeholder.com/150/FF5733/FFFFFF?text=Groceries' },
        { id: 2, name: 'Restaurants', image: 'https://via.placeholder.com/150/33FF57/FFFFFF?text=Restaurants' },
        { id: 3, name: 'Pharmacy', image: 'https://via.placeholder.com/150/3357FF/FFFFFF?text=Pharmacy' },
        { id: 4, name: 'Retail', image: 'https://via.placeholder.com/150/FFFF33/000000?text=Retail' },
        { id: 5, name: 'Services', image: 'https://via.placeholder.com/150/FF33FF/FFFFFF?text=Services' },
        { id: 6, name: 'Baked Goods', image: 'https://via.placeholder.com/150/33FFFF/000000?text=Baked+Goods' },
        { id: 7, name: 'Hardware', image: 'https://via.placeholder.com/150/FF8C33/FFFFFF?text=Hardware' },
    ];

    const mockVendors = [
        { id: 1, name: 'Local Grocer', description: 'Fresh produce and daily essentials.', image: 'https://via.placeholder.com/400x250/FF5733/FFFFFF?text=Local+Grocer' },
        { id: 2, name: 'Pizza Palace', description: 'Delicious pizzas and Italian dishes.', image: 'https://via.placeholder.com/400x250/33FF57/FFFFFF?text=Pizza+Palace' },
        { id: 3, name: 'Healthy Pharmacy', description: 'Your health and wellness partner.', image: 'https://via.placeholder.com/400x250/3357FF/FFFFFF?text=Healthy+Pharmacy' },
        { id: 4, name: 'Fashion Hub', description: 'Trendy clothes for all ages.', image: 'https://via.placeholder.com/400x250/FFFF33/000000?text=Fashion+Hub' },
        { id: 5, name: 'Tech Repair', description: 'Fast and reliable device repairs.', image: 'https://via.placeholder.com/400x250/FF33FF/FFFFFF?text=Tech+Repair' },
        { id: 6, name: 'Sweet Treats Bakery', description: 'Custom cakes and pastries.', image: 'https://via.placeholder.com/400x250/33FFFF/000000?text=Sweet+Treats' },
    ];

    function renderCategories() {
        categoriesContainer.innerHTML = ''; // Clear placeholders
        mockCategories.forEach(category => {
            const clone = categoryCardTemplate.content.cloneNode(true);
            clone.querySelector('[data-category-image]').src = category.image;
            clone.querySelector('[data-category-image]').alt = category.name;
            clone.querySelector('[data-category-name]').textContent = category.name;
            categoriesContainer.appendChild(clone);
        });
    }

    function renderVendors() {
        vendorsGrid.innerHTML = ''; // Clear placeholders
        mockVendors.forEach(vendor => {
            const clone = vendorCardTemplate.content.cloneNode(true);
            clone.querySelector('[data-vendor-image]').src = vendor.image;
            clone.querySelector('[data-vendor-image]').alt = vendor.name;
            clone.querySelector('[data-vendor-name]').textContent = vendor.name;
            clone.querySelector('[data-vendor-description]').textContent = vendor.description;
            vendorsGrid.appendChild(clone);
        });
    }

    // Initial render
    renderCategories();
    renderVendors();

    // Event listener for the profile/sign-in button (example)
    const profileButton = document.getElementById('profile-button');
    if (profileButton) {
        profileButton.addEventListener('click', () => {
            alert('Sign In / Profile functionality coming soon!');
            // In a real app, this would redirect to a login page or open a modal
        });
    }

    // Event listener for the address input / Find Stores button (example)
    const findStoresButton = document.querySelector('.hero-bg button');
    const addressInput = document.getElementById('address-input');
    if (findStoresButton && addressInput) {
        findStoresButton.addEventListener('click', () => {
            const address = addressInput.value;
            if (address) {
                alert(`Searching for stores near: ${address}`);
                // In a real app, this would trigger a search API call
            } else {
                alert('Please enter a delivery address.');
            }
        });
    }
});
