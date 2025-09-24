import React from 'react';
import { Link } from 'react-router-dom';

const HomePage: React.FC = () => {
  return (
    <div className="text-center p-8 bg-white shadow-lg rounded-lg">
      <h1 className="text-4xl font-bold text-gray-800 mb-4">Welcome to Kwik Connect!</h1>
      <p className="text-lg text-gray-600 mb-6">Your marketplace for school uniforms and supplies.</p>
      <div className="space-x-4">
        <Link to="/login" className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md transition duration-300">
          Login
        </Link>
        <Link to="/signup" className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-md transition duration-300">
          Sign Up
        </Link>
      </div>
    </div>
  );
};

export default HomePage;