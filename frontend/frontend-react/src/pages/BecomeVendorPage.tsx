import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Store, TrendingUp, Users, Package, Loader2 } from 'lucide-react';

// Define a type for benefit items for better type checking
type Benefit = {
  icon: React.ElementType;
  title: string;
  description: string;
};

// BenefitCard component for displaying individual benefits
const BenefitCard: React.FC<Benefit> = ({ icon: Icon, title, description }) => (
    <div className="bg-white p-6 rounded-lg shadow-md transition-all duration-300 hover:shadow-xl hover:-translate-y-1">
        <div className="flex items-center mb-4">
            <div className="flex-shrink-0">
                <div className="flex items-center justify-center h-12 w-12 rounded-md bg-secondary text-white">
                    <Icon className="h-6 w-6" />
                </div>
            </div>
            <div className="ml-4">
                <h3 className="text-lg font-semibold text-neutral-900">{title}</h3>
            </div>
        </div>
        <p className="text-neutral-600">{description}</p>
    </div>
);

const BecomeVendorPage: React.FC = () => {
    const [formData, setFormData] = useState({
        businessName: '',
        contactName: '',
        phone: '',
        email: ''
    });
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [submitted, setSubmitted] = useState(false);


    const benefits: Benefit[] = [
        {
            icon: TrendingUp,
            title: 'Increase Your Sales',
            description: 'Reach new customers in your area who are looking for the convenience of local delivery.'
        },
        {
            icon: Users,
            title: 'Connect With Your Community',
            description: 'Strengthen your local presence and build loyalty with customers right in your neighborhood.'
        },
        {
            icon: Package,
            title: 'Effortless Delivery Logistics',
            description: 'We handle the delivery for you. Focus on what you do best—running your business.'
        },
        {
            icon: Store,
            title: 'Simple Setup, No Hidden Fees',
            description: 'Get your store online with our easy onboarding process and transparent pricing.'
        }
    ];

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setError(null);

        // Simulate API call
        try {
            await new Promise(resolve => setTimeout(resolve, 1500));
            // In a real app, you'd have: await api.post('/vendor-inquiries', formData);
            console.log("Submitting vendor inquiry:", formData);
            setSubmitted(true);
        } catch (err) {
            setError("Something went wrong. Please try again later.");
        } finally {
            setIsLoading(false);
        }
    };


    return (
        <div className="bg-neutral-100 text-neutral-800">
            {/* Header Section */}
            <section className="bg-white py-16 text-center">
                <div className="container mx-auto px-4">
                    
                    <h1 className="text-4xl md:text-5xl font-bold text-neutral-900 mb-4">
                        Grow Your Business — Keep More Revenue Local
                    </h1>
                    <p className="text-lg md:text-xl text-neutral-600 max-w-3xl mx-auto">
                        Join a platform built for small shops: low fees, clear pricing, and delivery that connects you with nearby customers while keeping money in the community.
                    </p>
                </div>
            </section>

            {/* Benefits Section */}
            <section className="py-16">
                <div className="container mx-auto px-4">
                     <div className="text-center mb-12">
                        <h2 className="text-3xl font-bold text-neutral-900">Why Partner with Us?</h2>
                        <p className="text-neutral-600 mt-2">We're invested in the success of local businesses.</p>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        {benefits.map(benefit => (
                            <BenefitCard key={benefit.title} {...benefit} />
                        ))}
                    </div>
                </div>
            </section>

            {/* Signup Form Section */}
            <section className="bg-white py-16">
                <div className="container mx-auto px-4">
                    <div className="max-w-2xl mx-auto">
                        <div className="text-center mb-10">
                            <h2 className="text-3xl font-bold text-neutral-900">Let's Get Started</h2>
                            <p className="text-neutral-600 mt-2">Fill out the form below, and our local team will get in touch to begin the partnership process.</p>
                        </div>
                        
                        {submitted ? (
                            <div className="bg-secondary-light border-l-4 border-secondary text-white p-4 rounded-lg" role="alert">
                                <p className="font-bold">Thank You!</p>
                                <p>We've received your information and will contact you shortly to discuss our partnership.</p>
                            </div>
                        ) : (
                            <form onSubmit={handleSubmit} className="bg-white shadow-xl rounded-lg p-8 ring-1 ring-neutral-900/5">
                                {error && (
                                    <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6 rounded-md" role="alert">
                                        <p>{error}</p>
                                    </div>
                                )}
                                <div className="space-y-6">
                                    <div>
                                        <label htmlFor="businessName" className="block text-sm font-medium text-neutral-700">Business Name</label>
                                        <input type="text" name="businessName" id="businessName" required className="mt-1 block w-full px-3 py-2 bg-white border border-neutral-300 rounded-md shadow-sm focus:outline-none focus:ring-secondary focus:border-secondary" value={formData.businessName} onChange={handleInputChange} />
                                    </div>
                                    <div>
                                        <label htmlFor="contactName" className="block text-sm font-medium text-neutral-700">Your Full Name</label>
                                        <input type="text" name="contactName" id="contactName" required className="mt-1 block w-full px-3 py-2 bg-white border border-neutral-300 rounded-md shadow-sm focus:outline-none focus:ring-secondary focus:border-secondary" value={formData.contactName} onChange={handleInputChange} />
                                    </div>
                                     <div>
                                        <label htmlFor="phone" className="block text-sm font-medium text-neutral-700">Phone Number</label>
                                        <input type="tel" name="phone" id="phone" required className="mt-1 block w-full px-3 py-2 bg-white border border-neutral-300 rounded-md shadow-sm focus:outline-none focus:ring-secondary focus:border-secondary" value={formData.phone} onChange={handleInputChange} />
                                    </div>
                                    <div>
                                        <label htmlFor="email" className="block text-sm font-medium text-neutral-700">Email Address</label>
                                        <input type="email" name="email" id="email" required className="mt-1 block w-full px-3 py-2 bg-white border border-neutral-300 rounded-md shadow-sm focus:outline-none focus:ring-secondary focus:border-secondary" value={formData.email} onChange={handleInputChange} />
                                    </div>
                                </div>
                                <div className="mt-8">
                                    <button type="submit" disabled={isLoading} className="w-full flex justify-center items-center bg-secondary text-white font-bold py-3 px-6 rounded-lg hover:bg-secondary-dark transition duration-300 text-lg disabled:bg-secondary-light disabled:cursor-not-allowed">
                                        {isLoading ? <><Loader2 className="mr-2 h-6 w-6 animate-spin" /> Submitting...</> : 'Submit Inquiry'}
                                    </button>
                                </div>
                                <p className="text-xs text-neutral-500 mt-4 text-center">By submitting, you agree to our <Link to="/terms-of-service" className="underline hover:text-neutral-700">partnership terms</Link>.</p>
                            </form>
                        )}
                    </div>
                </div>
            </section>
        </div>
    );
}

export default BecomeVendorPage;