import React from 'react';
import { Link } from 'react-router-dom';

const AboutPage: React.FC = () => {
  return (
  <div className="bg-neutral-100 text-neutral-800">
  <section className="kc-container py-16">
          {/* Errands Section */}
          <div className="mt-12">
            <h2 className="text-2xl font-semibold mb-3">Everyday Errands Made Easy</h2>
            <p className="text-neutral-700 mb-4">KwikConnect is more than just deliveries—our couriers help with the tasks that really matter in kasi and rural life:</p>
            <ul className="grid grid-cols-1 md:grid-cols-2 gap-4 text-neutral-700">
              <li className="flex items-center bg-white p-3 rounded-lg shadow-sm">
                <span className="text-2xl mr-3" role="img" aria-label="Collect Medication">💊</span>
                <div>
                  <strong>Collect Medication</strong>
                  <p className="text-sm">We’ll fetch your prescriptions or clinic medication, so you don’t have to wait in long lines or travel far.</p>
                </div>
              </li>
              <li className="flex items-center bg-white p-3 rounded-lg shadow-sm">
                <span className="text-2xl mr-3" role="img" aria-label="Send & Receive Parcels">📦</span>
                <div>
                  <strong>Send & Receive Parcels</strong>
                  <p className="text-sm">Need to drop off or collect a small package, groceries, or important documents? We’ll handle it for you.</p>
                </div>
              </li>
              <li className="flex items-center bg-white p-3 rounded-lg shadow-sm">
                <span className="text-2xl mr-3" role="img" aria-label="Household Errands">🧹</span>
                <div>
                  <strong>Household Errands</strong>
                  <p className="text-sm">Need someone to fetch bottled water, buy paraffin, or help with other household essentials? We’re here to assist.</p>
                </div>
              </li>
              <li className="flex items-center bg-white p-3 rounded-lg shadow-sm">
                <span className="text-2xl mr-3" role="img" aria-label="Grocery Top-Ups">🛒</span>
                <div>
                  <strong>Grocery Top-Ups</strong>
                  <p className="text-sm">Forgot something at the shop or need a quick top-up from the spaza? We’ll pick it up and deliver to your door.</p>
                </div>
              </li>
              <li className="flex items-center bg-white p-3 rounded-lg shadow-sm">
                <span className="text-2xl mr-3" role="img" aria-label="Gas/Refill Exchange">🛢️</span>
                <div>
                  <strong>Gas/Refill Exchange</strong>
                  <p className="text-sm">Need to swap or refill your gas cylinder or paraffin container? We’ll handle the exchange and bring it to your door.</p>
                </div>
              </li>
            </ul>
          </div>
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-bold mb-4">Okwethu - For Our Community</h1>
          <p className="text-lg text-neutral-700 mb-8">KwikConnect is bringing delivery services to kasi and rural areas that big delivery apps ignore. We're not just another delivery app - we're your community's solution for convenient, affordable, and reliable local deliveries.</p>

          <h2 className="text-2xl font-semibold mt-10">Local Shops at Your Service</h2>
          <p className="mt-3 text-neutral-600">We connect you with the businesses you know and trust:</p>
          <ul className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4 text-neutral-600">
            <li className="flex items-center bg-white p-3 rounded-lg shadow-sm">
              <span className="text-2xl mr-3">🏠</span>
              <div>
                <strong>Spaza Shops</strong>
                <p className="text-sm">Your daily essentials from trusted local shops</p>
              </div>
            </li>
            <li className="flex items-center bg-white p-3 rounded-lg shadow-sm">
              <span className="text-2xl mr-3">🥘</span>
              <div>
                <strong>Street Food</strong>
                <p className="text-sm">Kotas, amagwinya, skopo, and more</p>
              </div>
            </li>
            <li className="flex items-center bg-white p-3 rounded-lg shadow-sm">
              <span className="text-2xl mr-3">🥩</span>
              <div>
                <strong>Local Butcheries</strong>
                <p className="text-sm">Quality meat from your neighborhood</p>
              </div>
            </li>
            <li className="flex items-center bg-white p-3 rounded-lg shadow-sm">
              <span className="text-2xl mr-3">💊</span>
              <div>
                <strong>Local Pharmacies</strong>
                <p className="text-sm">Medicine when you need it most</p>
              </div>
            </li>
          </ul>

          <h2 className="text-2xl font-semibold mt-12">Your Neighbors as Delivery Heroes</h2>
          <p className="mt-3 text-neutral-600">We create jobs for local people who know our streets and community:</p>
          <div className="mt-4 bg-white p-6 rounded-lg shadow-sm">
            <ul className="grid grid-cols-1 md:grid-cols-2 gap-4 text-neutral-600">
              <li className="flex items-start">
                <span className="text-2xl mr-3">🚲</span>
                <div>
                  <strong>Bicycle Deliveries</strong>
                  <p className="text-sm">Perfect for short distances, affordable to start</p>
                </div>
              </li>
              <li className="flex items-start">
                <span className="text-2xl mr-3">🛵</span>
                <div>
                  <strong>Motorbike & Car</strong>
                  <p className="text-sm">For longer distances and larger orders</p>
                </div>
              </li>
            </ul>
            <p className="mt-4 text-sm text-neutral-500">* No vehicle? No problem! Start with a bicycle and grow with us *</p>
          </div>

          <h2 className="text-2xl font-semibold mt-12">Order Your Way</h2>
          <p className="mt-3 text-neutral-600">Choose what works best for you:</p>
          <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white p-4 rounded-lg shadow-sm text-center">
              <span className="text-3xl">📱</span>
              <h3 className="font-semibold mt-2">WhatsApp</h3>
              <p className="text-sm text-neutral-600">Quick & easy messaging</p>
            </div>
            <div className="bg-white p-4 rounded-lg shadow-sm text-center">
              <span className="text-3xl">✉️</span>
              <h3 className="font-semibold mt-2">SMS</h3>
              <p className="text-sm text-neutral-600">Works on any phone</p>
            </div>
            <div className="bg-white p-4 rounded-lg shadow-sm text-center">
              <span className="text-3xl">📞</span>
              <h3 className="font-semibold mt-2">Phone Call</h3>
              <p className="text-sm text-neutral-600">Talk to our team directly</p>
            </div>
          </div>

          <h2 className="text-2xl font-semibold mt-12">Built for Our Reality</h2>
          <div className="mt-4 bg-white p-6 rounded-lg shadow-sm">
            <ul className="space-y-4 text-neutral-600">
              <li className="flex items-start">
                <span className="text-xl mr-3">🌟</span>
                <div>
                  <strong>Safe & Trusted</strong>
                  <p className="text-sm">All our delivery people are from the community and verified</p>
                </div>
              </li>
              <li className="flex items-start">
                <span className="text-xl mr-3">💰</span>
                <div>
                  <strong>Fair Prices</strong>
                  <p className="text-sm">Affordable delivery fees that make sense for our community</p>
                </div>
              </li>
              <li className="flex items-start">
                <span className="text-xl mr-3">🤝</span>
                <div>
                  <strong>Community First</strong>
                  <p className="text-sm">Supporting local businesses and creating local jobs</p>
                </div>
              </li>
            </ul>
          </div>

          <div className="mt-12 text-center space-y-6">
            <div className="space-y-4">
              <Link to="/signup" className="bg-primary text-white inline-block py-3 px-8 rounded-lg text-lg hover:bg-primary-dark transition-colors">Join KwikConnect Today</Link>
              <p className="text-neutral-500">Start ordering, delivering, or register your business</p>
            </div>
            
            <div className="flex justify-center space-x-6 text-sm">
              <Link to="/become-vendor" className="text-primary hover:text-primary-dark">Register Your Shop</Link>
              <Link to="/become-courier" className="text-primary hover:text-primary-dark">Work as Courier</Link>
              <Link to="/contact" className="text-primary hover:text-primary-dark">Contact Us</Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default AboutPage;