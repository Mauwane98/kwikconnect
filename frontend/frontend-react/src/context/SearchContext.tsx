import React, { createContext, useState, useContext, ReactNode } from 'react';

interface Vendor {
  id: string;
  name: string;
  category: string;
  distance?: string;
  image?: string;
  rating?: number;
  deliveryTime?: string;
}

type Filters = { query?: string; category?: string; delivery_time?: string };

interface SearchContextType {
  vendors: Vendor[];
  isLoadingVendors: boolean;
  vendorsError: string | null;
  doVendorSearch: (filters: string | Filters) => Promise<void>;
}

const SearchContext = createContext<SearchContextType | undefined>(undefined);

export const useSearch = () => {
  const context = useContext(SearchContext);
  if (!context) {
    throw new Error('useSearch must be used within a SearchProvider');
  }
  return context;
};

interface SearchProviderProps {
  children: ReactNode;
}

export const SearchProvider: React.FC<SearchProviderProps> = ({ children }) => {
  const [vendors, setVendors] = useState<Vendor[]>([]);
  const [isLoadingVendors, setIsLoadingVendors] = useState(false);
  const [vendorsError, setVendorsError] = useState<string | null>(null);

  const doVendorSearch = async (filters: string | Filters) => {
    const f: Filters = typeof filters === 'string' ? { query: filters } : (filters || {});
    const trimmed = (f.query || '').trim();

    if (!trimmed && !f.category && !f.delivery_time) {
      setVendors([]);
      return;
    }

    const API_BASE = process.env.REACT_APP_API_BASE || (typeof window !== 'undefined' && (['localhost','127.0.0.1'].includes(window.location.hostname) || process.env.NODE_ENV === 'development') ? 'http://127.0.0.1:5000' : '');

    setIsLoadingVendors(true);
    setVendorsError(null);

    try {
      const params = new URLSearchParams();
      if (trimmed) params.append('query', trimmed);
      if (f.category) params.append('category', f.category);
      if (f.delivery_time) params.append('delivery_time', f.delivery_time);

      const resp = await fetch(`${API_BASE}/api/v1/vendors?${params.toString()}`);
      if (!resp.ok) throw new Error(`Backend responded ${resp.status}`);
      const data = await resp.json();

      if (Array.isArray(data)) {
        const mapped = data.map((v: any) => ({
          id: v.id || v._id || v._id?.$oid || String(v._id || ''),
          name: v.name || v.business_name || v.display_name || '',
          category: v.category || v.vendor_type || '',
          distance: v.distance || v.display_distance || '',
          rating: v.rating || 4.3,
          image: v.profile_image_url || v.image || '',
          deliveryTime: v.delivery_time || v.estimated_delivery_time || ''
        }));
        setVendors(mapped);
      } else {
        setVendors([]);
      }
    } catch (err: any) {
      setVendors([]);
      setVendorsError(err?.message || String(err));
    } finally {
      setIsLoadingVendors(false);
    }
  };

  return (
    <SearchContext.Provider value={{ vendors, isLoadingVendors, vendorsError, doVendorSearch }}>
      {children}
    </SearchContext.Provider>
  );
};
