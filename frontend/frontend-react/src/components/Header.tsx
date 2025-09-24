import React from 'react';
import { Link } from 'react-router-dom';

const Header: React.FC = () => {
  return (
    <header className="bg-white shadow-md">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <div className="text-2xl font-bold text-gray-800">
          <Link to="/">Kwik Connect</Link>
        </div>
        <nav>
          <ul className="flex space-x-4">
            <li>
              <Link to="/login" className="text-gray-600 hover:text-gray-800">Login</Link>
            </li>
            <li>
              <Link to="/signup" className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
                Sign Up
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;
