import React from 'react';
import { User, BarChart2, Settings, HelpCircle } from 'lucide-react';

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

const AdminDashboard: React.FC = () => {
  return (
    <div className="min-h-screen bg-neutral-100">
      <div className="kc-container py-12">
        <header className="mb-8">
            <h1 className="text-3xl font-bold text-neutral-900">Admin Dashboard</h1>
            <p className="text-neutral-600">Welcome back, Admin!</p>
        </header>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <DashboardCard 
                title="Manage Users"
                description="View, edit, and remove users from the platform."
                icon={User}
                color="primary"
            />
            <DashboardCard 
                title="View Reports"
                description="Access platform analytics and activity reports."
                icon={BarChart2}
                color="secondary"
            />
            <DashboardCard 
                title="Settings"
                description="Configure platform preferences and security."
                icon={Settings}
                color="neutral"
            />
            <DashboardCard 
                title="Support"
                description="Contact support or review help resources."
                icon={HelpCircle}
                color="blue"
            />
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;