
import React from 'react';

const AppPromotion: React.FC = () => {
  return (
    <section className="bg-green-600 text-white">
      <div className="container mx-auto px-4 py-12 md:py-20">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
          <div>
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Kwik Connect — made for our kasi</h2>
            <p className="text-lg mb-6">Use the app for faster ordering, or send us a WhatsApp message — phone and SMS orders are welcome so everyone can use the service.</p>
            <div className="flex space-x-4">
              <a href="/download" className="bg-black text-white px-5 py-2 md:px-6 md:py-3 rounded-lg flex items-center shadow hover:shadow-md transition">Get the app</a>
              <a href={`https://wa.me/${(process.env.REACT_APP_WHATSAPP_NUMBER || '+27XXXXXXXXX').replace(/^\+/, '')}`} className="bg-white text-green-600 px-5 py-2 md:px-6 md:py-3 rounded-lg flex items-center border border-green-200 hover:shadow-sm transition">Order by WhatsApp</a>
            </div>
          </div>
          <div className="text-center">
            <img src="https://via.placeholder.com/240x480" alt="Kwik Connect App" className="max-w-xs mx-auto" />
          </div>
        </div>
      </div>
    </section>
  );
};

export default AppPromotion;
