import React, { useContext, useEffect, useState } from 'react';
import { AuthContext } from '../context/AuthContext';
import { User, Clock, PlusCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

// Mock data for recent orders
const mockOrders: Order[] = [
    { id: 'ZA-12345', date: '2025-09-23', status: 'Delivered', total: 250.75, vendor: 'Dikebu Spar' },
    { id: 'ZA-12342', date: '2025-09-21', status: 'Delivered', total: 95.50, vendor: 'The Butcher Block' },
    { id: 'ZA-12339', date: '2025-09-19', status: 'Delivered', total: 150.00, vendor: 'Dikebu Pharmacy' },
];

// Define the Order type
interface Order {
    id: string;
    date: string;
    status: 'Delivered' | 'Pending' | 'Cancelled';
    total: number;
    vendor: string;
}

// A sub-component for displaying a single order card
const OrderHistoryCard: React.FC<{ order: Order }> = ({ order }) => (
    <div className="bg-white p-4 rounded-lg shadow-sm border border-neutral-200 flex justify-between items-center">
        <div>
            <p className="font-bold text-neutral-800">Order #{order.id}</p>
            <p className="text-sm text-neutral-500">{order.vendor}</p>
            <p className="text-sm text-neutral-500">{order.date}</p>
        </div>
        <div className="text-right">
            <p className="font-semibold text-neutral-800">R {order.total.toFixed(2)}</p>
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                order.status === 'Delivered' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
            }`}>
                {order.status}
            </span>
        </div>
    </div>
);

const CustomerDashboard: React.FC = () => {
    const auth = useContext(AuthContext);
    const [orders, setOrders] = useState<Order[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // In a real app, you would fetch this data from an API.
        // For demonstration, we'll simulate a network request.
        const fetchOrders = async () => {
            setIsLoading(true);
            // const response = await api.get('/orders');
            // setOrders(response.data);
            setOrders(mockOrders); // Using mock data for now
            setIsLoading(false);
        };

        fetchOrders();
    }, []);

    if (!auth || !auth.user) {
        // This should ideally be handled by the ProtectedRoute, but as a fallback:
        return <div>Loading user data...</div>;
    }

    const { user } = auth;

        return (
            <div className="bg-neutral-100 min-h-full">
                <div className="kc-container py-6 md:py-8">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-neutral-900">Welcome, {user.first_name} {user.last_name}!</h1>
                <p className="text-neutral-600">Here's a quick look at your recent activity.</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

                {/* Main Content: Recent Orders */}
                <main className="lg:col-span-2">
                    <div className="bg-white p-6 rounded-lg shadow">
                        <div className="flex items-center mb-4">
                            <Clock className="w-6 h-6 text-neutral-500 mr-3"/>
                            <h2 className="text-xl font-semibold text-neutral-800">Recent Orders</h2>
                        </div>
                        <div className="space-y-4">
                            {isLoading ? (
                                <p>Loading orders...</p>
                            ) : orders.length > 0 ? (
                                orders.map(order => (
                                    <OrderHistoryCard key={order.id} order={order} />
                                ))
                            ) : (
                                <p>You have no recent orders.</p>
                            )}
                        </div>
                        <Link to="/order-history" className="mt-6 inline-block text-primary font-semibold hover:underline">
                            View all orders
                        </Link>
                    </div>
                </main>

                {/* Sidebar: Account Info & Actions */}
                <aside>
                    <div className="bg-white p-6 rounded-lg shadow mb-8">
                        <div className="flex items-center mb-4">
                           <User className="w-6 h-6 text-neutral-500 mr-3"/>
                           <h2 className="text-xl font-semibold text-neutral-800">Your Info</h2>
                        </div>
                        <div className="space-y-2 text-neutral-700">
                           <p><span className="font-semibold">Name:</span> {user.first_name} {user.last_name}</p>
                           <p><span className="font-semibold">Email:</span> {user.email}</p>
                           <p><span className="font-semibold">Role:</span> <span className="capitalize">{user.role}</span></p>
                        </div>
                         <Link to="/profile" className="mt-6 w-full inline-block text-sm text-center text-primary font-semibold hover:underline">
                            Edit Profile
                        </Link>
                    </div>
                     <div className="bg-primary-light text-white p-6 rounded-lg shadow-lg text-center">
                        <h3 className="text-lg font-bold mb-2">Ready for your next order?</h3>
                        <p className="mb-4">Get groceries, essentials, and more delivered to your door.</p>
                        <Link to="/new-order" className="w-full bg-white text-primary font-bold py-2 px-4 rounded-lg hover:bg-neutral-100 transition duration-300 flex items-center justify-center">
                           <PlusCircle className="w-5 h-5 mr-2"/> Start New Order
                        </Link>
                    </div>
                </aside>

                        </div>
                </div>
            </div>
        );
};

export default CustomerDashboard;