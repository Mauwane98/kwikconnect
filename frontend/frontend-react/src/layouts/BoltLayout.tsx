import React from 'react';
import { Outlet } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';

const BoltLayout: React.FC = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <Header isMain />
      <main className="flex-1">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
};

export default BoltLayout;