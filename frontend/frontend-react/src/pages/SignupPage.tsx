import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext'; // Updated import
import { UserPlus } from 'lucide-react';

const SignupPage: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [fullName, setFullName] = useState('');
    const [role, setRole] = useState('customer');
    const [error, setError] = useState<string | null>(null);
    const auth = useAuth(); // Updated to use useAuth hook
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        if (!auth) return;

        try {
            // The signup function in AuthContext will handle the API call
            // Split fullName into first and last name (best-effort)
            const parts = fullName.trim().split(/\s+/);
            const firstName = parts.shift() || '';
            const lastName = parts.join(' ') || '';
            const user = await auth.signup(email, password, firstName, lastName, role);
            // Redirect based on role
            if (user && user.role) {
                if (user.role === 'vendor') navigate('/vendor-dashboard');
                else if (user.role === 'courier') navigate('/courier-dashboard');
                else navigate('/customer-dashboard');
            } else {
                navigate('/login');
            }
        } catch (err) {
            setError('Failed to create an account. The email might already be in use.');
        }
    };

    return (
        <div className="min-h-screen bg-neutral-100 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
            <div className="sm:mx-auto sm:w-full sm:max-w-md">
                <div className="flex justify-center">
                    <UserPlus className="w-12 h-12 text-primary" />
                </div>
                <h2 className="mt-6 text-center text-3xl font-extrabold text-neutral-900">
                    Create your account
                </h2>
                <p className="mt-2 text-center text-sm text-neutral-600">
                    Already have an account?{' '}
                    <Link to="/login" className="font-medium text-primary hover:text-primary-dark">
                        Sign in
                    </Link>
                </p>
            </div>

            <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
                <div className="bg-white py-8 px-4 shadow-lg sm:rounded-lg sm:px-10">
                    {error && (
                        <div className="mb-4 bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md" role="alert">
                            <p>{error}</p>
                        </div>
                    )}
                    <form className="space-y-6" onSubmit={handleSubmit}>
                        <div>
                            <label htmlFor="fullName" className="block text-sm font-medium text-neutral-700">
                                Full Name
                            </label>
                            <div className="mt-1">
                                <input
                                    id="fullName"
                                    name="fullName"
                                    type="text"
                                    autoComplete="name"
                                    required
                                    value={fullName}
                                    onChange={(e) => setFullName(e.target.value)}
                                    className="appearance-none block w-full px-3 py-2 border border-neutral-300 rounded-md shadow-sm placeholder-neutral-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                                />
                            </div>
                        </div>

                        <div>
                            <label htmlFor="email" className="block text-sm font-medium text-neutral-700">
                                Email address
                            </label>
                            <div className="mt-1">
                                <input
                                    id="email"
                                    name="email"
                                    type="email"
                                    autoComplete="email"
                                    required
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="appearance-none block w-full px-3 py-2 border border-neutral-300 rounded-md shadow-sm placeholder-neutral-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                                />
                            </div>
                        </div>

                        <div>
                            <label htmlFor="password" className="block text-sm font-medium text-neutral-700">
                                Password
                            </label>
                            <div className="mt-1">
                                <input
                                    id="password"
                                    name="password"
                                    type="password"
                                    autoComplete="new-password"
                                    required
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="appearance-none block w-full px-3 py-2 border border-neutral-300 rounded-md shadow-sm placeholder-neutral-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                                />
                            </div>
                        </div>

                        <div>
                            <label htmlFor="role" className="block text-sm font-medium text-neutral-700">I am a...</label>
                            <select 
                                id="role" 
                                name="role" 
                                value={role} 
                                onChange={e => setRole(e.target.value)}
                                className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-neutral-300 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm rounded-md"
                            >
                                <option value="customer">Customer</option>
                                <option value="vendor">Vendor</option>
                                <option value="courier">Courier</option>
                            </select>
                        </div>

                        <div>
                            <button
                                type="submit"
                                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
                            >
                                Create Account
                            </button>
                        </div>
                         <p className="text-xs text-neutral-500 mt-4 text-center">By creating an account, you agree to our <Link to="/terms-of-service" className="underline hover:text-neutral-700">Terms of Service</Link>.</p>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default SignupPage;
