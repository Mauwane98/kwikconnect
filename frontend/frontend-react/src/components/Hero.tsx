import React, { useState } from 'react';

interface HeroProps {
  onFindRestaurants: () => void;
}

const Hero: React.FC<HeroProps> = ({ onFindRestaurants }) => {
  const [address, setAddress] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // In future we can pass `address` back to parent; for now just trigger the search view
    onFindRestaurants();
  };

  return (
    <section className="bg-green-600 text-white">
      <div className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">Your kasi, delivered</h1>
        <p className="text-lg mb-8">Order from local spaza shops, kota stands, taverns and more — delivered by people from your community.</p>
        <div className="max-w-2xl mx-auto">
          <form onSubmit={handleSubmit} className="flex items-center bg-white rounded-full shadow-lg overflow-hidden">
            <label htmlFor="hero-address" className="sr-only">Enter your address</label>
            <input
              id="hero-address"
              type="text"
              placeholder="Enter your street, township or village"
              value={address}
              onChange={(e) => setAddress(e.target.value)}
              className="w-full px-6 py-4 text-gray-700 focus:outline-none"
            />
            <button type="submit" className="bg-green-500 text-white px-6 md:px-8 py-3 md:py-4 font-semibold hover:bg-green-600 transition-colors">
              Start to order
            </button>
          </form>
        </div>
      </div>
    </section>
  );
};

export default Hero;