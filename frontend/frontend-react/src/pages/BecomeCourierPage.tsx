import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Clock, MapPin, DollarSign, Bike, Loader2 } from 'lucide-react';

type Benefit = {
  icon: React.ElementType;
  title: string;
  description: string;
};

const BenefitCard: React.FC<Benefit> = ({ icon: Icon, title, description }) => (
    <div className="bg-white p-6 rounded-lg shadow-md transition-all duration-300 hover:shadow-xl hover:-translate-y-1">
        <div className="flex items-center mb-4">
            <div className="flex-shrink-0">
                <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary text-white">
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


const BecomeCourierPage: React.FC = () => {
    const [formData, setFormData] = useState({
        fullName: '',
        phone: '',
        email: '',
        vehicle: 'bicycle',
    });
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [submitted, setSubmitted] = useState(false);
    
    const benefits: Benefit[] = [
        {
            icon: DollarSign,
            title: 'Earn on Your Schedule',
            description: 'Make money when it works for you. Accept delivery jobs that fit your availability.'
        },
        {
            icon: Clock,
            title: 'Flexible Hours',
            description: 'You are your own boss. Work as much or as little as you want, with no fixed shifts.'
        },
        {
            icon: MapPin,
            title: 'Know Your Community',
            description: 'Discover your town while making deliveries to your neighbors and local businesses.'
        },
        {
            icon: Bike,
            title: 'Easy to Start',
            description: 'Whether you have a bicycle, scooter, or car, you can start earning with KwikConnect.'
        }
    ];

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
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
            // In a real app: await api.post('/courier-applications', formData);
            console.log("Submitting courier application:", formData);
            setSubmitted(true);
        } catch (err) {
            setError("Could not submit application. Please try again.");
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
                        Earn Locally — Deliver for Your Neighbours
                    </h1>
                    <p className="text-lg md:text-xl text-neutral-600 max-w-3xl mx-auto">
                        Join a trusted local network of couriers. Earn income on a flexible schedule while helping neighbours and keeping the economic benefits inside your town.
                    </p>
                </div>
            </section>

            {/* Benefits Section */}
            <section className="py-16">
                <div className="container mx-auto px-4">
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
                            <h2 className="text-3xl font-bold text-neutral-900">Ready to Hit the Road?</h2>
                            <p className="text-neutral-600 mt-2">Sign up today, and we'll guide you through the next steps to become a KwikConnect courier.</p>
                        </div>
                        
                        {submitted ? (
                            <div className="bg-primary-light border-l-4 border-primary text-white p-4 rounded-lg" role="alert">
                                <p className="font-bold">Thanks for your interest!</p>
                                <p>We've received your application and will be in touch with you soon about the next steps.</p>
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
                                        <label htmlFor="fullName" className="block text-sm font-medium text-neutral-700">Full Name</label>
                                        <input type="text" name="fullName" id="fullName" required className="mt-1 block w-full px-3 py-2 bg-white border border-neutral-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary" value={formData.fullName} onChange={handleInputChange} />
                                    </div>
                                     <div>
                                        <label htmlFor="phone" className="block text-sm font-medium text-neutral-700">Phone Number</label>
                                        <input type="tel" name="phone" id="phone" required className="mt-1 block w-full px-3 py-2 bg-white border border-neutral-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary" value={formData.phone} onChange={handleInputChange} />
                                    </div>
                                    <div>
                                        <label htmlFor="email" className="block text-sm font-medium text-neutral-700">Email Address</label>
                                        <input type="email" name="email" id="email" required className="mt-1 block w-full px-3 py-2 bg-white border border-neutral-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary" value={formData.email} onChange={handleInputChange} />
                                    </div>
                                    <div>
                                        <label htmlFor="vehicle" className="block text-sm font-medium text-neutral-700">Primary Vehicle Type</label>
                                        <select id="vehicle" name="vehicle" className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-neutral-300 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm rounded-md" value={formData.vehicle} onChange={handleInputChange}>
                                            <option value="bicycle">Bicycle</option>
                                            <option value="scooter">Scooter/Motorbike</option>
                                            <option value="car">Car</option>
                                        </select>
                                    </div>
                                </div>
                                <div className="mt-8">
                                    <button type="submit" disabled={isLoading} className="w-full flex justify-center items-center bg-primary text-white font-bold py-3 px-6 rounded-lg hover:bg-primary-dark transition duration-300 text-lg disabled:bg-primary-light disabled:cursor-not-allowed">
                                        {isLoading ? <><Loader2 className="mr-2 h-6 w-6 animate-spin" /> Applying...</> : 'Apply Now'}
                                    </button>
                                </div>
                                <p className="text-xs text-neutral-500 mt-4 text-center">By applying, you agree to our <Link to="/terms-of-service" className="underline hover:text-neutral-700">Terms of Service</Link>.</p>
                            </form>
                        )}
                    </div>
                </div>
            </section>
        </div>
    );
}

export default BecomeCourierPage;