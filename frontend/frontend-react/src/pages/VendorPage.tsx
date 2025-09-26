import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Layout from '../components/Layout';
import ProductCard from '../components/ProductCard'; // Import ProductCard

// Interfaces
interface Vendor {
  id: string;
  name: string;
  category: string;
  // Add other vendor properties as needed
}

interface Product {
  id: string;
  name: string;
  price: number;
  image?: string;
}

const VendorPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [vendor, setVendor] = useState<Vendor | null>(null);
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchVendorAndProducts = async () => {
      const API_BASE = process.env.REACT_APP_API_BASE || (typeof window !== 'undefined' && (['localhost','127.0.0.1'].includes(window.location.hostname) || process.env.NODE_ENV === 'development') ? 'http://127.0.0.1:5000' : '');
      try {
        // Fetch vendor details
        const vendorResponse = await fetch(`${API_BASE}/api/v1/vendors/${id}`);
        if (!vendorResponse.ok) throw new Error('Vendor not found');
        const vendorData = await vendorResponse.json();
        setVendor(vendorData);

        // Fetch vendor products
        const productsResponse = await fetch(`${API_BASE}/api/v1/vendors/${id}/products`);
        if (!productsResponse.ok) throw new Error('Could not load products');
        const productsData = await productsResponse.json();
        setProducts(productsData);

      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchVendorAndProducts();
    }
  }, [id]);

  if (loading) {
    return <Layout><div className="text-center p-8">Loading...</div></Layout>;
  }

  if (error) {
    return <Layout><div className="text-center p-8 text-red-500">Error: {error}</div></Layout>;
  }

  if (!vendor) {
    return <Layout><div className="text-center p-8">Vendor not found.</div></Layout>;
  }

  return (
    <Layout>
      <div className="container mx-auto p-4">
        <header className="bg-white shadow-md rounded-lg p-6 mb-8">
          <h1 className="text-4xl font-bold">{vendor.name}</h1>
          <p className="text-xl text-gray-600">{vendor.category}</p>
        </header>
        
        <main>
          <h2 className="text-2xl font-bold mb-4">Menu / Products</h2>
          {products.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {products.map(product => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          ) : (
            <p>No products found for this vendor.</p>
          )}
        </main>
      </div>
    </Layout>
  );
};

export default VendorPage;
