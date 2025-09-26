import React from 'react';
import Header from './Header';

interface LayoutProps {
  children: React.ReactNode;
  sidebar?: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children, sidebar }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header isMain />
      <div className="container mx-auto px-4">
        {sidebar ? (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 py-6">
            {/** Sidebar on lg, stacked above on small screens */}
            <aside className="lg:col-span-3 order-2 lg:order-1">
              <div className="sticky top-20">
                {sidebar}
              </div>
            </aside>

            <main className="lg:col-span-9 order-1 lg:order-2">
              {children}
            </main>
          </div>
        ) : (
          <div className="py-6">
            <main>{children}</main>
          </div>
        )}
      </div>
    </div>
  );
};

export default Layout;