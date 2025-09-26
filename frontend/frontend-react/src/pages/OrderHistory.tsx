import React from 'react';
import { Link } from 'react-router-dom';

const OrderHistory: React.FC = () => {
  return (
    <div className="bg-neutral-100 min-h-full">
      <div className="kc-container py-8">
        <h1 className="text-2xl font-bold mb-4">Order History</h1>
        <p className="text-neutral-600 mb-6">View your past orders and their statuses.</p>
        <div className="bg-white p-6 rounded-lg shadow">
          <p>This is a stub page. It will show a list of past orders.</p>
          <Link to="/customer-dashboard" className="mt-4 inline-block text-primary hover:underline">Back to Dashboard</Link>
        </div>
      </div>
    </div>
  );
};

export default OrderHistory;
