import React from 'react';
import { Link } from 'react-router-dom';
import { useCart } from '../context/CartContext';

const NewOrder: React.FC = () => {
  const cart = useCart();

  const products = [
    { id: 'p1', name: 'Rice 2kg', price: 49.99, vendor: 'Dikebu Supermarket' },
    { id: 'p2', name: 'Milk 2L', price: 24.5, vendor: 'Community Pharmacy' },
    { id: 'p3', name: 'Chicken 1kg', price: 69.0, vendor: 'Local Butchery' },
  ];

  return (
    <div className="bg-neutral-100 min-h-full">
      <div className="kc-container py-8">
        <h1 className="text-2xl font-bold mb-4">Start a New Order</h1>
        <p className="text-neutral-600 mb-6">Search for items, add them to your cart, and create an order.</p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {products.map(p => (
            <div key={p.id} className="bg-white p-4 rounded-lg shadow">
              <div className="font-semibold">{p.name}</div>
              <div className="text-sm text-neutral-500">{p.vendor}</div>
              <div className="mt-4 flex items-center justify-between">
                <div className="font-bold">R {p.price.toFixed(2)}</div>
                <button onClick={() => cart.addToCart({ id: p.id, name: p.name, price: p.price })} className="bg-primary text-white px-3 py-1 rounded">Add</button>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-6">
          <Link to="/cart" className="text-primary font-semibold">View Cart & Checkout</Link>
        </div>
      </div>
    </div>
  );
};

export default NewOrder;