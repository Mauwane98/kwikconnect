import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Sidebar: React.FC = () => {
  const { user } = useAuth();

  const getDashboardLink = () => {
    if (!user) return '/';
    switch (user.role) {
      case 'customer':
        return '/customer/dashboard';
      case 'vendor':
        return '/vendor/dashboard';
      case 'courier':
        return '/courier/dashboard';
      case 'admin':
        return '/admin/dashboard';
      default:
        return '/';
    }
  };

  return (
    <div className="flex flex-col w-64 bg-gray-800">
      <div className="flex items-center justify-center h-16 bg-gray-900">
        <span className="text-white font-bold uppercase">Kwik Connect</span>
      </div>
      <nav className="flex-1 flex flex-col p-4">
        <Link
          to={getDashboardLink()}
          className="flex items-center text-gray-400 hover:text-white py-2 px-4 rounded transition duration-200"
        >
          <svg
            className="h-5 w-5 mr-3"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M3 12L12 3L21 12H17V20H7V12H3Z"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          Dashboard
        </Link>

        {user && user.role === 'customer' && (
          <Link
            to="/customer/orders"
            className="flex items-center text-gray-400 hover:text-white py-2 px-4 rounded transition duration-200"
          >
            <svg
              className="h-5 w-5 mr-3"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M9 19H15M12 12V19M12 12C12 9.87827 12.8428 7.84344 14.3431 6.34315C15.8434 4.84285 17.8783 4 20 4C20.7956 4 21.5587 4.15612 22.2549 4.45879C22.9511 4.76146 23.5696 5.19977 24 5.75M12 12C12 9.87827 11.1572 7.84344 9.65685 6.34315C8.15656 4.84285 6.12173 4 4 4C3.20443 4 2.44129 4.15612 1.74512 4.45879C1.04896 4.76146 0.430391 5.19977 0 5.75"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            My Orders
          </Link>
        )}

        {user && user.role === 'vendor' && (
          <Link
            to="/vendor/products"
            className="flex items-center text-gray-400 hover:text-white py-2 px-4 rounded transition duration-200"
          >
            <svg
              className="h-5 w-5 mr-3"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M16 11V7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7V11M5 11H19M5 11C4.44772 11 4 11.4477 4 12V20C4 20.5523 4.44772 21 5 21H19C19.5523 21 20 20.5523 20 20V12C20 11.4477 19.5523 11 19 11M5 11L8 7M19 11L16 7"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            My Products
          </Link>
        )}

        {user && user.role === 'courier' && (
          <Link
            to="/courier/jobs"
            className="flex items-center text-gray-400 hover:text-white py-2 px-4 rounded transition duration-200"
          >
            <svg
              className="h-5 w-5 mr-3"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M12 18V12L16 10"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            Available Jobs
          </Link>
        )}

        {user && user.role === 'admin' && (
          <Link
            to="/admin/users"
            className="flex items-center text-gray-400 hover:text-white py-2 px-4 rounded transition duration-200"
          >
            <svg
              className="h-5 w-5 mr-3"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M17 21V19C17 17.9391 16.5786 16.9217 15.8284 16.1716C15.0783 15.4214 14.0609 15 13 15H11C9.93913 15 8.92172 15.4214 8.17157 16.1716C7.42143 16.9217 7 17.9391 7 19V21M12 11C14.2091 11 16 9.20914 16 7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7C8 9.20914 9.79086 11 12 11Z"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            Manage Users
          </Link>
        )}

        {/* Common links for all authenticated users */}
        <Link
          to="/profile"
          className="flex items-center text-gray-400 hover:text-white py-2 px-4 rounded transition duration-200"
        >
          <svg
            className="h-5 w-5 mr-3"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21M12 11C14.2091 11 16 9.20914 16 7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7C8 9.20914 9.79086 11 12 11Z"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            Profile
          </Link>

        <button
          onClick={logout}
          className="flex items-center text-gray-400 hover:text-white py-2 px-4 rounded transition duration-200 w-full text-left"
        >
          <svg
            className="h-5 w-5 mr-3"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M17 16L21 12L17 8M21 12H9M11 21H4C3.46957 21 2.96086 20.7893 2.58579 20.4142C2.21071 20.0391 2 19.5304 2 19V5C2 4.46957 2.21071 3.96086 2.58579 3.58579C2.96086 3.21071 3.46957 3 4 3H11"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          Logout
        </button>
      </nav>
    </div>
  );
};

export default Sidebar;