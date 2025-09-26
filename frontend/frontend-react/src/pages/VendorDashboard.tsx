import React from 'react';
import { Link } from 'react-router-dom'; // Import Link
import { ShoppingBag, ClipboardList, BarChart2, HelpCircle } from 'lucide-react';

const DashboardCard: React.FC<{ title: string; description: string; icon: React.ElementType; color: string }> = ({ title, description, icon: Icon, color }) => (
    <div className={`bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 border-l-4 border-${color}-500`}>
        <div className="flex items-center mb-4">
            <div className={`flex-shrink-0 h-12 w-12 flex items-center justify-center rounded-full bg-${color}-100 text-${color}-600`}>
                <Icon size={24} />
            </div>
            <div className="ml-4">
                <h3 className="text-lg font-semibold text-neutral-800">{title}</h3>
            </div>
        </div>
        <p className="text-neutral-600">{description}</p>
    </div>
);

const VendorDashboard: React.FC = () => {
  return (
    <div className="min-h-screen bg-neutral-100">
      <div className="kc-container py-12">
        <header className="mb-8">
            <h1 className="text-3xl font-bold text-neutral-900">Vendor Dashboard</h1>
            <p className="text-neutral-600">Welcome back, Vendor!</p>
        </header>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <Link to="/vendor-dashboard/products">
                <DashboardCard 
                    title="Manage Products"
                    description="Add, edit, or remove products from your store."
                    icon={ShoppingBag}
                    color="primary"
                />
            </Link>
            <DashboardCard 
                title="Orders"
                description="View and fulfill incoming orders."
                icon={ClipboardList}
                color="secondary"
            />
            <DashboardCard 
                title="Analytics"
                description="Track your sales and performance."
                icon={BarChart2}
                color="neutral"
            />
            <DashboardCard 
                title="Support"
                description="Get help or contact support."
                icon={HelpCircle}
                color="blue"
            />
        </div>
      </div>
    </div>
  );
};

export default VendorDashboard;