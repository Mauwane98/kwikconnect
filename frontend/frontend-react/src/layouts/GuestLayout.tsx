
import React from 'react';
import { Outlet } from 'react-router-dom';
import Footer from '../components/Footer';

const GuestLayout: React.FC = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <div className="flex-1 flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="kc-container max-w-md w-full space-y-8">
          <Outlet /> {/* This is where child routes will be rendered */}
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default GuestLayout;
