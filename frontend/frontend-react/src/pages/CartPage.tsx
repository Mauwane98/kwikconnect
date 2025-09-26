import React from 'react';
import { useCart } from '../context/CartContext';
import Layout from '../components/Layout'; // Using layout for consistency

const CartPage: React.FC = () => {
  const { cartItems, removeFromCart, updateQuantity } = useCart();

  const calculateTotal = () => {
    return cartItems.reduce((total, item) => total + item.price * item.quantity, 0);
  };

  return (
    <Layout>
      <div className="container mx-auto py-8">
        <h1 className="text-2xl font-bold mb-4">Your Cart</h1>
        <div className="bg-white p-6 rounded-lg shadow">
          {cartItems.length === 0 ? (
            <p>Your cart is empty.</p>
          ) : (
            <div>
              <div className="space-y-4">
                {cartItems.map(item => (
                  <div key={item.id} className="flex justify-between items-center">
                    <div className="flex items-center gap-4">
                      <img src={item.image || 'https://via.placeholder.com/100x100'} alt={item.name} className="w-16 h-16 object-cover rounded" />
                      <div>
                        <div className="font-semibold">{item.name}</div>
                        <div className="text-sm text-neutral-500">R {item.price.toFixed(2)}</div>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <input
                        type="number"
                        min={1}
                        value={item.quantity}
                        onChange={e => updateQuantity(item.id, Number(e.target.value))}
                        className="w-16 border rounded px-2 py-1"
                      />
                      <div>R {(item.price * item.quantity).toFixed(2)}</div>
                      <button onClick={() => removeFromCart(item.id)} className="text-red-600 hover:text-red-800">Remove</button>
                    </div>
                  </div>
                ))}
              </div>
              <div className="flex justify-between items-center mt-6 border-t pt-4">
                <div className="text-lg font-semibold">Total</div>
                <div className="text-lg font-bold">R {calculateTotal().toFixed(2)}</div>
              </div>
              <div className="mt-6 text-right">
                <button className="bg-green-600 text-white px-6 py-3 rounded-lg shadow hover:bg-green-700">
                  Proceed to Checkout
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default CartPage;

