import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext'; // Updated import
import { LogIn } from 'lucide-react';
import { useGoogleLogin } from '@react-oauth/google';

const LoginPage: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState<string | null>(null);
    const auth = useAuth(); // Updated to use useAuth hook
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);

        if (!auth) return;

        try {
            console.log('Submitting login for', email);
            const user = await auth.login(email, password);
            console.log('Login response user:', user);
            if (user && user.role) {
                if (user.role === 'vendor') navigate('/vendor-dashboard');
                else if (user.role === 'courier') navigate('/courier-dashboard');
                else navigate('/customer-dashboard');
            } else {
                navigate('/');
            }
        } catch (err: any) {
            // Try to show backend error message when available
            const msg = err?.message || 'Failed to log in. Please check your credentials and try again.';
            setError(msg);
        }
    };

    const handleGoogleLogin = useGoogleLogin({
        onSuccess: async (tokenResponse) => {
            if (!auth) return;
            try {
                const user = await auth.loginWithGoogle(tokenResponse.access_token);
                if (user && user.role) {
                    if (user.role === 'vendor') navigate('/vendor-dashboard');
                    else if (user.role === 'courier') navigate('/courier-dashboard');
                    else navigate('/customer-dashboard');
                } else {
                    navigate('/');
                }
            } catch (err: any) {
                setError(err?.message || 'Google login failed. Please try again.');
            }
        },
        onError: () => {
            setError('Google login failed. Please try again.');
        },
    });

    return (
            <div className="min-h-screen bg-neutral-100 flex flex-col">
                <div className="kc-container py-12">
                    <div className="sm:mx-auto sm:w-full sm:max-w-md">
                <div className="flex justify-center">
                    <LogIn className="w-12 h-12 text-primary" />
                </div>
                <h2 className="mt-6 text-center text-3xl font-extrabold text-neutral-900">
                    Sign in to your account
                </h2>
                <p className="mt-2 text-center text-sm text-neutral-600">
                    Or{' '}
                    <Link to="/signup" className="font-medium text-primary hover:text-primary-dark">
                        start your journey with us
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
                                    autoComplete="current-password"
                                    required
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="appearance-none block w-full px-3 py-2 border border-neutral-300 rounded-md shadow-sm placeholder-neutral-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                                />
                            </div>
                        </div>

                        <div className="flex items-center justify-between">
                            <div className="flex items-center">
                                <input
                                    id="remember-me"
                                    name="remember-me"
                                    type="checkbox"
                                    className="h-4 w-4 text-primary focus:ring-primary border-neutral-300 rounded"
                                />
                                <label htmlFor="remember-me" className="ml-2 block text-sm text-neutral-900">
                                    Remember me
                                </label>
                            </div>

                            <div className="text-sm">
                                <a href="/forgot-password" className="font-medium text-primary hover:text-primary-dark">
                                    Forgot your password?
                                </a>
                            </div>
                        </div>

                        <div>
                            <button
                                type="submit"
                                disabled={auth?.isLoading}
                                className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary ${auth?.isLoading ? 'bg-primary/60 cursor-not-allowed' : 'bg-primary hover:bg-primary-dark'}`}
                            >
                                {auth?.isLoading ? (
                                    <span className="flex items-center space-x-2">
                                        <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
                                        </svg>
                                        <span>Signing in...</span>
                                    </span>
                                ) : (
                                    'Sign in'
                                )}
                            </button>
                        </div>
                    </form>

                    <div className="mt-6">
                        <div className="relative">
                            <div className="absolute inset-0 flex items-center">
                                <div className="w-full border-t border-neutral-300" />
                            </div>
                            <div className="relative flex justify-center text-sm">
                                <span className="px-2 bg-white text-neutral-500">Or continue with</span>
                            </div>
                        </div>

                        <div className="mt-6">
                            <button
                                onClick={() => handleGoogleLogin()}
                                className="w-full flex justify-center py-2 px-4 border border-neutral-300 rounded-md shadow-sm bg-white text-sm font-medium text-neutral-700 hover:bg-neutral-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
                            >
                                Sign in with Google
                            </button>
                        </div>
                    </div>

                    <div className="mt-4 text-sm text-neutral-700">
                        <strong>Debug:</strong>
                        <div>isLoading: {String(auth?.isLoading)}</div>
                        <div>isAuthenticated: {String(auth?.isAuthenticated)}</div>
                        <div>Last user: {auth?.user ? JSON.stringify(auth.user) : 'null'}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    );
};

export default LoginPage;
