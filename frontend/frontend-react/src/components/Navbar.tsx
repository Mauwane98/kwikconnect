import React from 'react';
import { useAuth } from '../context/AuthContext';

const Navbar: React.FC = () => {
  const { logout } = useAuth();

  return (
    <header className="flex justify-between items-center py-4 px-6 bg-white border-b-4 border-indigo-600">
      <div className="flex items-center">
        <button
          aria-label="Toggle sidebar"
          className="text-gray-500 focus:outline-none focus:text-gray-700"
        >
          <svg
            className="h-6 w-6"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M4 6H20M4 12H20M4 18H11"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </button>

        <div className="relative mx-4 lg:mx-0">
          <span className="absolute inset-y-0 left-0 pl-3 flex items-center">
            <svg
              className="h-5 w-5 text-gray-500"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M15.7955 15.8111L21 21M18 10.5C18 14.6421 14.6421 18 10.5 18C6.35786 18 3 14.6421 3 10.5C3 6.35786 6.35786 3 10.5 3C14.6421 3 18 6.35786 18 10.5Z"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </span>

          <input
            className="form-input w-32 sm:w-64 rounded-md pl-10 pr-4 focus:border-indigo-600"
            type="text"
            placeholder="Search"
          />
        </div>
      </div>

      <div className="flex items-center">
        <div className="relative">
          <button
            className="flex items-center mx-4 text-gray-700 focus:outline-none"
          >
            <svg
              className="h-6 w-6"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M15 17H20L18.5951 15.3631C18.3671 15.1108 18.2751 14.7796 18.3002 14.4435V12C18.3002 11.0433 17.9729 10.1261 17.3715 9.42465C16.7701 8.7232 15.9071 8.28671 15.0002 8.17847V7C15.0002 6.44772 14.5525 6 14.0002 6C13.4479 6 13.0002 6.44772 13.0002 7V8.17847C12.0933 8.28671 11.2303 8.7232 10.6289 9.42465C10.0274 10.1261 9.70012 11.0433 9.70012 12V14.4435C9.72521 14.7796 9.63318 15.1108 9.40518 15.3631L8 17H13M15 17V18C15 18.5523 14.5523 19 14 19H10C9.44772 19 9 18.5523 9 18V17M15 17H9"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </button>

          <div
            className="absolute right-0 mt-2 w-48 bg-white rounded-md overflow-hidden shadow-xl z-10"
            style={{ display: 'none' }}
          >
            <a
              href="#"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-indigo-600 hover:text-white"
            >
              Messages
            </a>
            <a
              href="#"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-indigo-600 hover:text-white"
            >
              Settings
            </a>
          </div>
        </div>

        <div className="relative">
          <button
            className="relative block h-8 w-8 rounded-full overflow-hidden shadow focus:outline-none"
          >
            <img
              className="h-full w-full object-cover"
              src="https://images.unsplash.com/photo-1528892952291-009c6695fd88?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=320&h=320&q=80"
              alt="Your avatar"
            />
          </button>

          <div
            className="absolute right-0 mt-2 w-48 bg-white rounded-md overflow-hidden shadow-xl z-10"
            style={{ display: 'none' }}
          >
            <a
              href="#"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-indigo-600 hover:text-white"
            >
              Profile
            </a>
            <a
              href="#"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-indigo-600 hover:text-white"
            >
              Settings
            </a>
            <button
              onClick={logout}
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-indigo-600 hover:text-white"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Navbar;