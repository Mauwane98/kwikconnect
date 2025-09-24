
import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from '../components/Navbar'; // Assuming you'll create a Navbar component
import Sidebar from '../components/Sidebar'; // Assuming you'll create a Sidebar component

const AuthLayout: React.FC = () => {
  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar />
      <div className="flex flex-col flex-1 overflow-hidden">
        <Navbar />
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-200">
          <div className="container mx-auto px-6 py-8">
            <Outlet /> {/* This is where child routes will be rendered */}
          </div>
        </main>
      </div>
    </div>
  );
};

export default AuthLayout;
