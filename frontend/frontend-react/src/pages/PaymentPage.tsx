import React from 'react';

const PaymentPage: React.FC = () => {
  return (
    <div className="bg-neutral-100 min-h-full">
      <div className="kc-container py-8">
        <h1 className="text-2xl font-bold mb-4">Payments</h1>
        <div className="bg-white p-6 rounded-lg shadow">
          <p>Payment integration placeholder. Hook up Stripe/Paystack/Flutterwave here.</p>
        </div>
      </div>
    </div>
  );
};

export default PaymentPage;