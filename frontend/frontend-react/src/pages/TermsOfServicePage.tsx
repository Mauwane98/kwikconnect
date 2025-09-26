import React from 'react';

const TermsOfServicePage: React.FC = () => {
  return (
    <div className="bg-white py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-extrabold text-neutral-900 text-center">Terms of Service</h1>
        <p className="mt-4 text-lg text-neutral-500 text-center">Last updated: September 24, 2025</p>

        <div className="mt-10 prose prose-primary lg:prose-lg text-neutral-600 mx-auto">
          <p>
            Welcome to KwikConnect! These terms and conditions outline the rules and regulations for the use of our platform.
          </p>

          <h2 className="mt-8 text-2xl font-bold text-neutral-900">1. Introduction</h2>
          <p>
            By accessing this platform, we assume you accept these terms and conditions. Do not continue to use KwikConnect if you do not agree to all of the terms and conditions stated on this page.
          </p>

          <h2 className="mt-8 text-2xl font-bold text-neutral-900">2. User Accounts</h2>
          <p>
            When you create an account with us, you must provide information that is accurate, complete, and current at all times. Failure to do so constitutes a breach of the Terms, which may result in immediate termination of your account on our service.
          </p>
           <p>
            You are responsible for safeguarding the password that you use to access the service and for any activities or actions under your password.
          </p>

          <h2 className="mt-8 text-2xl font-bold text-neutral-900">3. Content</h2>
          <p>
            Our Service allows you to post, link, store, share and otherwise make available certain information, text, graphics, videos, or other material. You are responsible for the Content that you post on or through the Service, including its legality, reliability, and appropriateness.
          </p>
          
          <h2 className="mt-8 text-2xl font-bold text-neutral-900">4. Prohibited Uses</h2>
          <p>
              You may use our platform only for lawful purposes. You may not use our platform:
          </p>
          <ul>
              <li>In any way that violates any applicable national or international law or regulation.</li>
              <li>For the purpose of exploiting, harming, or attempting to exploit or harm minors in any way by exposing them to inappropriate content or otherwise.</li>
              <li>To transmit, or procure the sending of, any advertising or promotional material, including any "junk mail", "chain letter," "spam," or any other similar solicitation.</li>
          </ul>

          <h2 className="mt-8 text-2xl font-bold text-neutral-900">5. Termination</h2>
          <p>
            We may terminate or suspend your account and bar access to the service immediately, without prior notice or liability, under our sole discretion, for any reason whatsoever and without limitation, including but not limited to a breach of the Terms.
          </p>

          <h2 className="mt-8 text-2xl font-bold text-neutral-900">6. Changes to Service</h2>
          <p>
            We reserve the right to withdraw or amend our Service, and any service or material we provide via the Service, in our sole discretion without notice. 
          </p>

          <h2 className="mt-8 text-2xl font-bold text-neutral-900">Contact Us</h2>
          <p>
            If you have any questions about these Terms, please contact us at support@kwikconnect.co.za.
          </p>
        </div>
      </div>
    </div>
  );
};

export default TermsOfServicePage;