
import React from 'react';
import { Link } from 'react-router-dom';

const BoltFooter: React.FC = () => {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-xl font-bold mb-4">Kwik Connect</h3>
            <p className="text-gray-400">Your Kasi, Delivered.</p>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4">Company</h3>
            <ul className="space-y-2">
              <li><Link to="/about-us" className="hover:text-green-400">About us</Link></li>
              <li><Link to="/careers" className="hover:text-green-400">Careers</Link></li>
              <li><Link to="/press" className="hover:text-green-400">Press</Link></li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4">Legal</h3>
            <ul className="space-y-2">
              <li><Link to="/terms" className="hover:text-green-400">Terms & Conditions</Link></li>
              <li><Link to="/privacy" className="hover:text-green-400">Privacy Policy</Link></li>
              <li><Link to="/cookies" className="hover:text-green-400">Cookie Policy</Link></li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4">Follow us</h3>
            <div className="flex space-x-4">
              <a href="#" className="hover:text-green-400">Facebook</a>
              <a href="#" className="hover:text-green-400">Twitter</a>
              <a href="#" className="hover:text-green-400">Instagram</a>
            </div>
          </div>
        </div>
        <div className="mt-8 border-t border-gray-800 pt-8 flex justify-between items-center">
          <p className="text-gray-500">&copy; 2025 Kwik Connect. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default BoltFooter;
