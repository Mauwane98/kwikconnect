import React from 'react';
import { Outlet } from 'react-router-dom';
import Footer from '../components/Footer';

const MainLayout: React.FC = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <main className="flex-grow kc-container py-8">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
};

export default MainLayout;
