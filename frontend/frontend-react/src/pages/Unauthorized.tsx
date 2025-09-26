import React from 'react';
import { Link } from 'react-router-dom';

const Unauthorized: React.FC = () => (
  <div className="bg-neutral-100 min-h-screen flex items-center justify-center">
    <div className="kc-container max-w-md text-center p-8">
      <h1 className="text-3xl font-bold mb-4">Unauthorized</h1>
      <p className="text-neutral-600 mb-6">You don't have permission to view this page.</p>
      <Link to="/" className="text-primary hover:underline">Go to Home</Link>
    </div>
  </div>
);

export default Unauthorized;