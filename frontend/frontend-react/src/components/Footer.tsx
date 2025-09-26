import React from 'react';
import { Link } from 'react-router-dom';

const Footer: React.FC = () => {
  return (
    <footer className="bg-neutral-900 text-neutral-200 py-12 md:py-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-3 gap-8">
        <div>
          <h3 className="font-bold text-lg">KwikConnect</h3>
          <p className="text-sm mt-2 text-neutral-400">Affordable delivery for local shops, multi-store orders, and community couriers — keeping money and jobs in your town.</p>
          <div className="mt-3 text-sm">
            <a href="tel:+0000000000" className="block text-neutral-400 hover:text-primary-light">Call: +000 000 0000</a>
            <a href="https://wa.me/0000000000" className="block text-neutral-400 hover:text-primary-light">WhatsApp: Message us</a>
          </div>
        </div>

        <div>
          <h4 className="font-semibold mb-2">Company</h4>
          <ul className="space-y-1 text-sm text-neutral-400">
            <li><Link to="/about-us">About</Link></li>
            <li><Link to="/careers">Careers</Link></li>
            <li><Link to="/blog">Blog</Link></li>
          </ul>
        </div>

        <div>
          <h4 className="font-semibold mb-2">Support</h4>
          <ul className="space-y-1 text-sm text-neutral-400">
            <li><Link to="/faq">Help Center</Link></li>
            <li><Link to="/terms-of-service">Terms</Link></li>
            <li><Link to="/contact-us">Contact</Link></li>
          </ul>
        </div>
      </div>
      <div className="mt-8 text-center text-sm text-neutral-500">&copy; 2025 KwikConnect. All rights reserved.</div>
    </footer>
  );
};

export default Footer;
