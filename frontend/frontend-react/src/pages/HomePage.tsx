import React, { useState } from 'react';
import Hero from '../components/Hero';
import FeaturedRestaurants from '../components/FeaturedRestaurants';
import HowItWorks from '../components/HowItWorks';
import AppPromotion from '../components/AppPromotion';
import VendorResults from '../components/VendorResults';
import { useSearch } from '../context/SearchContext';

const HomePage: React.FC = () => {
  const [addressEntered, setAddressEntered] = useState(false);
  const { vendors, isLoadingVendors, vendorsError } = useSearch();

  const handleAddressSearch = () => {
    setAddressEntered(true);
  };

  const whatsappNumber = process.env.REACT_APP_WHATSAPP_NUMBER || '+27123456789';
  const formatWaLink = (num: string) => {
    const cleaned = (num || '+27123456789').replace(/^\+/, '');
    return `https://wa.me/${cleaned}`;
  }
  const whatsappMessage = encodeURIComponent("Hello, I'd like to order from my area. Please help. My address: ");

  return (
    <div className="min-h-screen bg-gray-50">
      <Hero onFindRestaurants={handleAddressSearch} />

      <section className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto text-center">
          <p className="text-gray-700">Use the search box at the top to find local shops, stock and services near you.</p>
        </div>

        {vendorsError && <div className="max-w-2xl mx-auto mt-3 text-sm text-red-600">Could not load live vendors ({vendorsError}). Showing local suggestions.</div>}

        <div className="max-w-2xl mx-auto mt-6 flex flex-col sm:flex-row gap-3 items-center justify-between">
          <div className="text-sm text-gray-700">No app? No problem — send a WhatsApp message or call and we’ll place your order for you.</div>
          <div className="flex gap-3">
            <a
              className="inline-flex items-center gap-2 bg-green-600 text-white px-4 py-2 rounded-lg"
              href={formatWaLink(whatsappNumber) + `?text=${whatsappMessage}`}
              target="_blank"
              rel="noreferrer noopener"
            >
              Order on WhatsApp
            </a>
            <a href={`tel:${whatsappNumber}`} className="inline-flex items-center gap-2 bg-gray-200 text-gray-900 px-4 py-2 rounded-lg">
              Call to order
            </a>
          </div>
        </div>
      </section>

      {addressEntered && (
        <>
          {isLoadingVendors ? (
            <div className="text-center p-8">Loading vendors...</div>
          ) : vendors.length > 0 ? (
            <VendorResults vendors={vendors} />
          ) : (
            <FeaturedRestaurants />
          )}
        </>
      )}
      <HowItWorks />

      {/* Informational sections for kasi/rural messaging */}
      <section className="py-12">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transform transition duration-300 hover:scale-102">
              <h3 className="text-xl font-bold mb-2">For customers</h3>
              <p className="text-gray-700 mb-4">Find local spazas, supermarkets, hardware stores, kota stalls, butcheries, taverns and more. Order groceries, medicine, household items, small hardware supplies or a hot meal — we’ll deliver or arrange collection. Order in the app, send a WhatsApp message or call and we’ll help you place the order.</p>
              <a className="inline-block bg-green-600 text-white px-4 py-2 rounded shadow-sm hover:shadow-md transition" href="#vendor-section">Browse local vendors</a>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transform transition duration-300 hover:scale-102">
              <h3 className="text-xl font-bold mb-2">For couriers</h3>
              <p className="text-gray-700 mb-4">Deliver short local trips and earn in your community. Use a bicycle, motorbike or car — flexible hours, reliable pay and short distances keep work simple.</p>
              <a className="inline-block bg-green-600 text-white px-4 py-2 rounded shadow-sm hover:shadow-md transition" href="/courier-signup">Become a courier</a>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transform transition duration-300 hover:scale-102">
              <h3 className="text-xl font-bold mb-2">For vendors</h3>
              <p className="text-gray-700 mb-4">List your spaza, supermarket, hardware or food stall and start receiving orders from people nearby. Simple signup, phone or WhatsApp notifications and straightforward payments make it easy to join.</p>
              <a className="inline-block bg-green-600 text-white px-4 py-2 rounded shadow-sm hover:shadow-md transition" href="/vendor-signup">Register your shop</a>
            </div>
          </div>
        </div>
      </section>

      <section className="py-8 bg-white">
        <div className="container mx-auto px-4">
          <h3 className="text-2xl font-bold mb-4">Errands & deliveries</h3>
          <p className="text-gray-700 mb-4">Need medicine, bottled water or something from the spaza? Create an errand — couriers in your area can pick it up and deliver it to you.</p>
          <div className="flex gap-3">
            <a href="/create-errand" className="bg-green-600 text-white px-4 py-2 rounded">Create an errand</a>
            <a href="/how-it-works" className="px-4 py-2 border rounded">Learn how errands work</a>
          </div>
        </div>
      </section>

      <section className="py-8">
        <div className="container mx-auto px-4">
          <h3 className="text-2xl font-bold mb-4">How to order (quick)</h3>
          <ol className="list-decimal list-inside text-gray-700 space-y-2">
            <li>Enter your street, township or village.</li>
            <li>Search for what you need — spaza, kota, bread, milk, pap & vleis, or household essentials.</li>
            <li>Choose vendor and place order (cash on delivery supported).</li>
            <li>Or send a WhatsApp message or call — we will take your order by phone.</li>
          </ol>
        </div>
      </section>

      <section className="py-12 bg-green-50">
        <div className="container mx-auto px-4 text-center">
          <h3 className="text-2xl font-bold mb-2">Keep money in the kasi</h3>
          <p className="text-gray-700 mb-4">Kwik Connect helps local people sell more and earn more — vendors, couriers and customers all win when we trade locally.</p>
          <a href="/about" className="inline-block bg-green-600 text-white px-4 py-2 rounded">About Kwik Connect</a>
        </div>
      </section>

      <AppPromotion />
    </div>
  );
};

export default HomePage;
