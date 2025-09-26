import React from 'react';
import { Link } from 'react-router-dom';

interface Vendor {
  id: string;
  name: string;
  category: string;
  distance?: string;
  image?: string;
  rating?: number;
  deliveryTime?: string; // Added deliveryTime
}

const VendorCard: React.FC<{ vendor: Vendor }> = ({ vendor }) => {
  return (
    <Link to={`/vendor/${vendor.id}`} className="block">
      <article className="bg-white rounded-lg shadow-md overflow-hidden transform transition hover:scale-102 hover:shadow-lg h-full flex flex-col">
        <div className="relative">
          <img src={vendor.image || 'https://via.placeholder.com/900x520'} alt={vendor.name} className="w-full h-56 md:h-64 object-cover" />
          <div className="absolute top-3 left-3 bg-black bg-opacity-50 text-white text-xs px-2 py-1 rounded">{vendor.category}</div>
          <div className="absolute top-3 right-3 bg-white text-gray-800 text-sm px-2 py-1 rounded shadow">{vendor.rating ? `${vendor.rating} ★` : '—'}</div>
        </div>
        <div className="p-4 md:p-5 flex-grow flex flex-col">
          <h3 className="text-lg md:text-xl font-semibold text-gray-900">{vendor.name}</h3>
          <p className="text-sm text-gray-600 mt-1">{vendor.distance || 'Nearby'}</p>
          <div className="mt-4 flex items-center justify-between flex-grow">
            <div className="text-sm text-gray-700">Estimated: <span className="font-medium">{vendor.deliveryTime || '20–35 mins'}</span></div>
            <div className="bg-green-600 text-white px-4 py-2 rounded-lg shadow hover:bg-green-700 transition">Order</div>
          </div>
        </div>
      </article>
    </Link>
  );
};

export default VendorCard;
