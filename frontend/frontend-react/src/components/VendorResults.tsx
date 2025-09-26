import React from 'react';
import VendorCard from './VendorCard';

interface Vendor {
  id: string;
  name: string;
  category: string;
  distance?: string;
  image?: string;
  rating?: number;
  deliveryTime?: string;
}

const VendorResults: React.FC<{ vendors: Vendor[] }> = ({ vendors }) => {
  if (!vendors.length) {
    return <div className="text-center text-gray-600 py-8">No vendors found nearby. Try searching 'spaza' or 'kota'.</div>;
  }

  return (
    <section className="py-8">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-3xl md:text-4xl font-bold">Vendors near you</h2>
            <p className="text-gray-600">Orders via app, WhatsApp or a quick call — local couriers deliver.</p>
          </div>
          <div className="text-sm text-gray-600">Showing {vendors.length} results</div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {vendors.map((v) => (
            <div key={v.id} className="animate-fade-in">
              <VendorCard vendor={v} />
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default VendorResults;
