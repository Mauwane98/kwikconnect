import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Menu, X } from 'lucide-react';
import { useCart } from '../context/CartContext';
import { useSearch } from '../context/SearchContext'; // Import useSearch

interface HeaderProps {
  isMain?: boolean;
}

const Header: React.FC<HeaderProps> = ({ isMain = false }) => {
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState('');
  const cart = useCart();
  const { doVendorSearch } = useSearch(); // Get doVendorSearch from context

  return (
  <header data-main-header={isMain ? 'true' : undefined} className="w-full bg-white shadow-sm sticky top-0 z-30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-3 md:py-4">
          <div className="flex items-center gap-4">
            <Link to="/" className="flex items-center gap-3">
              <div className="h-10 w-10 bg-green-600 rounded-full flex items-center justify-center text-white font-bold">KC</div>
              <span className="font-bold text-lg text-neutral-800 hidden sm:inline">KwikConnect</span>
            </Link>
          </div>

          <div className="flex-1 px-4">
            <div className="max-w-2xl mx-auto">
              <input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault();
                    doVendorSearch(search); // Use doVendorSearch from context
                  }
                }}
                aria-label="Search vendors or items"
                placeholder="Search spaza, supermarket, hardware, food or items..."
                className="w-full border border-gray-200 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-300"
              />
            </div>
          </div>

          <nav className="hidden md:flex items-center gap-4">
            <Link to="/become-vendor" className="text-neutral-600 hover:text-green-600">Become a Vendor</Link>
            <Link to="/become-courier" className="text-neutral-600 hover:text-green-600">Become a Courier</Link>
            <Link to="/login" className="text-neutral-600 hover:text-green-600">Sign in</Link>
            <Link to="/signup" className="bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700">Sign up</Link>
            <Link to="/cart" className="text-neutral-600 hover:text-green-600">Cart ({cart.cartCount})</Link>
          </nav>

          <div className="md:hidden">
            <button onClick={() => setOpen(!open)} aria-label="Toggle menu" className="p-2 rounded-md bg-neutral-100">
              {open ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {open && (
        <div className="md:hidden bg-white border-t">
          <div className="px-4 py-4 space-y-2">
            <Link to="/" className="block text-neutral-600">Home</Link>
            <Link to="/cart" className="block text-neutral-600">Cart ({cart.cartCount})</Link>
            <Link to="/become-vendor" className="block text-neutral-600">Become a Vendor</Link>
            <Link to="/become-courier" className="block text-neutral-600">Become a Courier</Link>
            <Link to="/login" className="block text-neutral-600">Sign in</Link>
            <Link to="/signup" className="block bg-green-600 text-white py-2 px-4 rounded-md">Sign up</Link>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;
