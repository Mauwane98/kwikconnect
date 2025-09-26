import React from 'react';
import { useCart, CartItem } from '../context/CartContext';

const CartSidebar: React.FC = () => {
  const { cartItems } = useCart();
  const total = cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0);

  return (
    <aside className="w-80 bg-white p-4 rounded-lg shadow">
      <h3 className="font-semibold mb-2">Cart</h3>
      {cartItems.length === 0 ? <p className="text-sm text-gray-500">Empty</p> : (
        <div className="space-y-2">
          {cartItems.map((it: CartItem) => (
            <div key={it.id} className="flex justify-between text-sm">
              <div>{it.name} x{it.quantity}</div>
              <div>R {(it.price * it.quantity).toFixed(2)}</div>
            </div>
          ))}
          <div className="mt-3 font-bold">Total R {total.toFixed(2)}</div>
        </div>
      )}
    </aside>
  );
};

export default CartSidebar;