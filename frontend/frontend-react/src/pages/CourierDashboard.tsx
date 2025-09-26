import React from 'react';
import { Bike, DollarSign, User, HelpCircle } from 'lucide-react';

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

const CourierDashboard: React.FC = () => {
  return (
    <div className="min-h-screen bg-neutral-100">
      <div className="kc-container py-12">
        <header className="mb-8">
            <h1 className="text-3xl font-bold text-neutral-900">Courier Dashboard</h1>
            <p className="text-neutral-600">Welcome back, Courier!</p>
        </header>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <DashboardCard 
                title="Active Deliveries"
                description="View and manage your current delivery jobs."
                icon={Bike}
                color="primary"
            />
            <DashboardCard 
                title="Earnings"
                description="Track your earnings and completed jobs."
                icon={DollarSign}
                color="secondary"
            />
            <DashboardCard 
                title="Profile"
                description="Update your courier profile and vehicle info."
                icon={User}
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

export default CourierDashboard;