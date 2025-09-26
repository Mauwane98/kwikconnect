
import React from 'react';
import { MapPin, Search, ShoppingCart } from 'lucide-react';

const HowItWorks: React.FC = () => {
  return (
    <section className="py-20 bg-gray-50">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">How it works</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12 text-center">
          <div className="flex flex-col items-center">
            <div className="bg-green-100 rounded-full p-6 mb-6">
              <MapPin className="h-10 w-10 text-green-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">1. Tell us where you are</h3>
            <p className="text-gray-600">Enter your street, township or village so we can show vendors nearby.</p>
          </div>
          <div className="flex flex-col items-center">
            <div className="bg-green-100 rounded-full p-6 mb-6">
              <Search className="h-10 w-10 text-green-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">2. Pick a spaza, kota or shop</h3>
            <p className="text-gray-600">Search for bread, kota, pap & vleis, milk, medicine or your favourite local shop — spaza, supermarket, hardware or food stall.</p>
          </div>
          <div className="flex flex-col items-center">
            <div className="bg-green-100 rounded-full p-6 mb-6">
              <ShoppingCart className="h-10 w-10 text-green-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">3. Delivered by local people</h3>
            <p className="text-gray-600">Couriers from your community deliver — on foot, by bicycle or car. Keep money local.</p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
