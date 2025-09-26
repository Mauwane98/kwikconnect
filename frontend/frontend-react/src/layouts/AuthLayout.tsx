
import React from 'react';
import { Outlet } from 'react-router-dom';
import Footer from '../components/Footer';

const AuthLayout: React.FC = () => {
  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <main className="flex-1 overflow-x-hidden overflow-y-auto">
        <div className="kc-container py-8">
          <Outlet /> {/* This is where child routes will be rendered */}
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default AuthLayout;
