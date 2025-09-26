import React, { createContext, useState, useEffect, ReactNode, useContext } from 'react';

// Define the shape of the user object
interface User {
    id: string;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    phone_number?: string;
    role: 'customer' | 'vendor' | 'courier' | 'admin';
    profile_picture_url?: string;
    email_verified?: boolean;
}

// Define the shape of the context value
interface AuthContextType {
    user: User | null;
    token: string | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    login: (email: string, password: string) => Promise<User | null>;
    loginWithGoogle: (accessToken: string) => Promise<User | null>;
    signup: (
        email: string,
        password: string,
        firstName: string,
        lastName: string,
        role: string
    ) => Promise<User | null>;
    logout: () => void;
    updateProfile: (data: Partial<User>) => Promise<User | null>;
}

// Create the context with a default undefined value
export const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Custom hook to use the AuthContext
export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

// Define the props for the AuthProvider component
interface AuthProviderProps {
    children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const [token, setToken] = useState<string | null>(() => localStorage.getItem('token'));
    const [isLoading, setIsLoading] = useState(true);
    // Compute API base: use environment variable when provided, otherwise if we're
    // running in the browser on localhost point to the backend dev server.
    let API_BASE = '';
    if (process.env.REACT_APP_API_BASE) {
        API_BASE = process.env.REACT_APP_API_BASE;
    } else if (typeof window !== 'undefined') {
        const host = window.location.hostname;
        const isLocal = host === 'localhost' || host === '127.0.0.1' || process.env.NODE_ENV === 'development';
        if (isLocal) API_BASE = 'http://127.0.0.1:5000';
    }

    useEffect(() => {
        const fetchUser = async () => {
            // Only fetch profile when we have a token and user isn't already set.
            if (!token) {
                setIsLoading(false);
                return;
            }

            // Capture the token value for this fetch so we can compare later and avoid
            // clearing a token that was set after this fetch started.
            const tokenAtStart = token;

            if (user) {
                // User is already set (e.g. after login), no need to re-fetch immediately.
                setIsLoading(false);
                return;
            }

            try {
                let response;
                try {
                    response = await fetch(`${API_BASE}/api/v1/auth/profile`, {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });
                } catch (fetchErr) {
                    console.error('Network error fetching profile:', fetchErr);
                    // don't clear token here; allow the app to stay logged in until user action
                    setIsLoading(false);
                    return;
                }

                if (!response.ok) {
                    const errText = await response.text().catch(() => '');
                    console.error('Profile fetch failed:', errText || response.statusText);
                    // If unauthorized, clear token **only if** the token hasn't changed since
                    // this fetch started (prevents clearing a token set by a concurrent login).
                    if (response.status === 401 || response.status === 422) {
                        const stored = localStorage.getItem('token');
                        if (stored === tokenAtStart) {
                            localStorage.removeItem('token');
                            setToken(null);
                            setUser(null);
                        } else {
                            console.warn('Token changed since profile fetch started; not clearing.');
                        }
                    }
                    setIsLoading(false);
                    return;
                }

                const userData = await response.json();
                setUser(userData);
            } catch (error) {
                console.error("Authentication Error:", error);
            } finally {
                setIsLoading(false);
            }
        };
        fetchUser();
    }, [token, user]);

    // Debug: log token changes to help trace unexpected clears
    useEffect(() => {
        try {
            console.debug('[AuthContext] token changed ->', token);
        } catch (e) {
            // ignore
        }
    }, [token]);

    const login = async (email: string, password: string) => {
        setIsLoading(true);
        try {
            let response;
            try {
                response = await fetch(`${API_BASE}/api/v1/auth/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password }),
                });
            } catch (fetchErr) {
                console.error('Network error on login:', fetchErr);
                throw new Error('Network error connecting to backend. Is the backend running?');
            }

            if (!response.ok) {
                // try to extract JSON error, otherwise text
                let errorMsg = 'Login failed';
                try {
                    const errorData = await response.json();
                    errorMsg = errorData.message || JSON.stringify(errorData);
                } catch (e) {
                    const txt = await response.text().catch(() => '');
                    errorMsg = txt || errorMsg;
                }
                throw new Error(errorMsg || 'Login failed');
            }

            const { access_token, user } = await response.json();
            // persist token and set user in context
            if (access_token) {
                localStorage.setItem('token', access_token);
                setToken(access_token);
                console.debug('[AuthContext] login stored token');
            }
            setUser(user);
            return user;
        } finally {
            setIsLoading(false);
        }
    };

    const signup = async (
        email: string,
        password: string,
        firstName: string,
        lastName: string,
        role: string
    ) => {
        setIsLoading(true);
        try {
            let response;
            try {
                // Generate a username from the email
                const username = email.split('@')[0] + new Date().getTime(); // Add timestamp for uniqueness
                response = await fetch(`${API_BASE}/api/v1/auth/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        email,
                        password,
                        first_name: firstName,
                        last_name: lastName,
                        username,
                        role,
                    }),
                });
            } catch (fetchErr) {
                console.error('Network error on signup:', fetchErr);
                throw new Error('Network error connecting to backend. Is the backend running?');
            }

            if (!response.ok) {
                let errorMsg = 'Signup failed';
                try {
                    const errorData = await response.json();
                    errorMsg = errorData.message || JSON.stringify(errorData);
                } catch (e) {
                    const txt = await response.text().catch(() => '');
                    errorMsg = txt || errorMsg;
                }
                throw new Error(errorMsg || 'Signup failed');
            }

            const { access_token, user } = await response.json();
            if (access_token) {
                localStorage.setItem('token', access_token);
                setToken(access_token);
            }
            setUser(user);
            return user;
        } finally {
            setIsLoading(false);
        }
    };

    const loginWithGoogle = async (accessToken: string) => {
        setIsLoading(true);
        try {
            const response = await fetch(`${API_BASE}/api/v1/auth/google-login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ access_token: accessToken }),
            });

            if (!response.ok) {
                throw new Error('Google login failed');
            }

            const { access_token, user } = await response.json();
            if (access_token) {
                localStorage.setItem('token', access_token);
                setToken(access_token);
            }
            setUser(user);
            return user;
        } finally {
            setIsLoading(false);
        }
    };

    const logout = () => {
        console.debug('[AuthContext] logout');
        localStorage.removeItem('token');
        setToken(null);
        setUser(null);
    };

    const updateProfile = async (data: Partial<User>) => {
        if (!token) return null;
        try {
            let response;
            try {
                response = await fetch(`${API_BASE}/api/v1/auth/profile`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                    body: JSON.stringify(data),
                });
            } catch (fetchErr) {
                console.error('Network error updating profile:', fetchErr);
                throw new Error('Network error connecting to backend. Is the backend running?');
            }

            if (!response.ok) {
                const errTxt = await response.text().catch(() => '');
                throw new Error(errTxt || 'Failed to update profile');
            }

            const updatedUser = await response.json();
            setUser(updatedUser);
            return updatedUser;
        } catch (error) {
            console.error('Profile update error', error);
            return null;
        }
    };

    const value = {
        user,
        token,
        // Consider the user authenticated if a token exists; keep loading separate so
        // components (like LoginPage) can navigate immediately without the provider
        // unmounting children while isLoading is true.
        isAuthenticated: !!token,
        isLoading,
        login,
        loginWithGoogle,
        signup,
        logout,
        updateProfile,
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};
