import React from 'react';
import { useCart } from '../context/CartContext';

interface Product {
  id: string;
  name: string;
  price: number;
  image?: string;
}

const ProductCard: React.FC<{ product: Product }> = ({ product }) => {
  const { addToCart } = useCart();

  const handleAddToCart = () => {
    addToCart(product);
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <img src={product.image || 'https://via.placeholder.com/300x200'} alt={product.name} className="w-full h-40 object-cover" />
      <div className="p-4">
        <h3 className="text-lg font-semibold">{product.name}</h3>
        <p className="text-gray-800 font-bold mt-2">R {product.price.toFixed(2)}</p>
        <button 
          onClick={handleAddToCart}
          className="mt-4 w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition"
        >
          Add to Cart
        </button>
      </div>
    </div>
  );
};

export default ProductCard;
