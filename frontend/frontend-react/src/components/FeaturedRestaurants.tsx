import React, { useEffect, useState } from 'react';

const FeaturedRestaurants: React.FC = () => {
  const [vendors, setVendors] = useState<Array<any>>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const API_BASE = process.env.REACT_APP_API_BASE || 'http://127.0.0.1:5000';
    fetch(`${API_BASE}/api/v1/vendors`) // get all approved/open vendors
      .then((r) => r.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setVendors(data.slice(0, 8).map((v: any) => ({
            id: v.id || v._id || v._id?.$oid || String(v._id || ''),
            name: v.name || v.business_name || v.display_name || '',
            cuisine: v.category || v.vendor_type || 'Local',
            rating: v.rating || 4.3,
            image: v.profile_image_url || v.image || 'https://via.placeholder.com/300'
          })));
        }
      })
      .catch((err) => setError(String(err)));
  }, []);

  return (
    <section className="py-16 bg-white">
      <div className="container mx-auto px-4">
        <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-6">Local vendors we recommend</h2>
        <p className="text-gray-600 mb-6">Spazas, kota stands, butcheries, taverns and small shops from your area — supporting local businesses.</p>
        {error && <div className="text-red-600 mb-4">Could not load vendors: {error}</div>}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {vendors.map((restaurant, index) => (
            <div key={restaurant.id || index} className="bg-white rounded-lg shadow-md overflow-hidden">
              <img src={restaurant.image} alt={restaurant.name} className="w-full h-40 object-cover" />
              <div className="p-4">
                <h3 className="text-lg font-bold text-gray-900 mb-1">{restaurant.name}</h3>
                <p className="text-sm text-gray-600 mb-2">{restaurant.cuisine}</p>
                <div className="flex items-center">
                  <span className="text-yellow-500">★</span>
                  <span className="ml-2 text-gray-600">{restaurant.rating}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturedRestaurants;
