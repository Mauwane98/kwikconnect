import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { CartProvider } from './context/CartContext';
import { SearchProvider } from './context/SearchContext';
import MainLayout from './layouts/MainLayout';
import GuestLayout from './layouts/GuestLayout';
import BoltLayout from './layouts/BoltLayout';
import AuthLayout from './layouts/AuthLayout';
import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import AdminDashboard from './pages/AdminDashboard';
import VendorDashboard from './pages/VendorDashboard';
import CourierDashboard from './pages/CourierDashboard';
import CustomerDashboard from './pages/CustomerDashboard';
import ProfilePage from './pages/ProfilePage';
import ProtectedRoute from './components/ProtectedRoute';
import BecomeVendorPage from './pages/BecomeVendorPage';
import BecomeCourierPage from './pages/BecomeCourierPage';
import NewOrder from './pages/NewOrder';
import OrderHistory from './pages/OrderHistory';
import PaymentPage from './pages/PaymentPage';
import Unauthorized from './pages/Unauthorized';
import CartPage from './pages/CartPage';
import VendorPage from './pages/VendorPage';
import ManageProductsPage from './pages/ManageProductsPage';
import NewProductPage from './pages/NewProductPage';

function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <SearchProvider>
          <Router>
            <Routes>
              {/* Guest Routes */}
              <Route element={<BoltLayout />}>
                <Route path="/" element={<HomePage />} />
                <Route path="/vendor/:id" element={<VendorPage />} />
              </Route>
              <Route element={<GuestLayout />}>
                <Route path="/about-us" element={<AboutPage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/signup" element={<SignupPage />} />
                <Route path="/become-vendor" element={<BecomeVendorPage />} />
                <Route path="/become-courier" element={<BecomeCourierPage />} />
              </Route>

              {/* Authenticated Routes */}
              <Route element={<AuthLayout />}>
                <Route path="/admin-dashboard" element={<ProtectedRoute allowedRoles={['admin']}><AdminDashboard /></ProtectedRoute>} />
                <Route path="/vendor-dashboard" element={<ProtectedRoute allowedRoles={['vendor']}><VendorDashboard /></ProtectedRoute>} />
                <Route path="/vendor-dashboard/products" element={<ProtectedRoute allowedRoles={['vendor']}><ManageProductsPage /></ProtectedRoute>} />
                <Route path="/vendor-dashboard/products/new" element={<ProtectedRoute allowedRoles={['vendor']}><NewProductPage /></ProtectedRoute>} />
                <Route path="/courier-dashboard" element={<ProtectedRoute allowedRoles={['courier']}><CourierDashboard /></ProtectedRoute>} />
                <Route path="/customer-dashboard" element={<ProtectedRoute allowedRoles={['customer']}><CustomerDashboard /></ProtectedRoute>} />
                <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
                <Route path="/new-order" element={<ProtectedRoute allowedRoles={['customer']}><NewOrder /></ProtectedRoute>} />
                <Route path="/order-history" element={<ProtectedRoute allowedRoles={['customer']}><OrderHistory /></ProtectedRoute>} />
                <Route path="/cart" element={<ProtectedRoute allowedRoles={['customer']}><CartPage /></ProtectedRoute>} />
                <Route path="/payments" element={<ProtectedRoute><PaymentPage /></ProtectedRoute>} />
                <Route path="/unauthorized" element={<Unauthorized />} />
              </Route>
              
              {/* Fallback for routes that need MainLayout but are not specifically guest or auth */}
              <Route element={<MainLayout />}>
                {/* You can add other general routes here, like about-us, contact, etc. */}
              </Route>
            </Routes>
          </Router>
        </SearchProvider>
      </CartProvider>
    </AuthProvider>
  );
}

export default App;