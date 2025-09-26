
import React from 'react';
import { Link } from 'react-router-dom';

const BoltHeader: React.FC = () => {
  return (
    <header className="bg-white shadow-md">
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <div className="flex items-center">
          <Link to="/" className="text-2xl font-bold text-green-600">Kwik Connect</Link>
        </div>
        <nav className="hidden md:flex items-center space-x-8">
          <Link to="/support" className="text-gray-600 hover:text-green-600">Support</Link>
          <Link to="/register" className="text-gray-600 hover:text-green-600">Register</Link>
          <Link to="/products" className="text-gray-600 hover:text-green-600">Products</Link>
        </nav>
        <div className="flex items-center">
          <Link to="/login" className="text-gray-600 hover:text-green-600 mr-4">Log in</Link>
          <Link to="/signup" className="bg-green-600 text-white px-4 py-2 rounded-full hover:bg-green-700">Sign up</Link>
        </div>
      </div>
    </header>
  );
};

export default BoltHeader;
