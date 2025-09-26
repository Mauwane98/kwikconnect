import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link } from 'react-router-dom';

interface Product {
  id: string;
  name: string;
  price: number;
  // Add other product properties as needed
}

const ManageProductsPage: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();

  useEffect(() => {
    const fetchProducts = async () => {
      if (!user) {
        setLoading(false);
        setError("You must be logged in to view this page.");
        return;
      }
      
      const API_BASE = process.env.REACT_APP_API_BASE || (typeof window !== 'undefined' && (['localhost','127.0.0.1'].includes(window.location.hostname) || process.env.NODE_ENV === 'development') ? 'http://127.0.0.1:5000' : '');
      
      try {
        // Assuming the vendor's products are fetched based on the logged-in user's ID
        const response = await fetch(`${API_BASE}/api/v1/vendors/${user.id}/products`);
        if (!response.ok) {
          throw new Error('Failed to fetch products.');
        }
        const data = await response.json();
        setProducts(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, [user]);

  if (loading) {
    return <div className="text-center p-8">Loading products...</div>;
  }

  if (error) {
    return <div className="text-center p-8 text-red-500">Error: {error}</div>;
  }

  return (
    <div className="container mx-auto py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Manage Your Products</h1>
        <Link to="/vendor-dashboard/products/new" className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700">
          Add New Product
        </Link>
      </div>
      <div className="bg-white p-6 rounded-lg shadow">
        {products.length === 0 ? (
          <p>You haven't added any products yet.</p>
        ) : (
          <ul className="space-y-4">
            {products.map(product => (
              <li key={product.id} className="flex justify-between items-center p-4 border rounded-lg">
                <div>
                  <p className="font-semibold">{product.name}</p>
                  <p className="text-gray-600">R {product.price.toFixed(2)}</p>
                </div>
                <div>
                  <button className="text-blue-600 hover:underline mr-4">Edit</button>
                  <button className="text-red-600 hover:underline">Delete</button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default ManageProductsPage;
