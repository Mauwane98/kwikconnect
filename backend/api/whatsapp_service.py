# backend/api/whatsapp_service.py

from backend.mongo import get_mongo_client
from bson.objectid import ObjectId # Import ObjectId for MongoDB _id
from flask import current_app # To access app config for Twilio client
from twilio.rest import Client # To send messages to vendors

from backend.models.vendor import Vendor # New import
from backend.models.product import Product # New import

# Get MongoDB client and collection for sessions and orders
db = get_mongo_client()
sessions_collection = db.whatsapp_sessions
orders_collection = db.whatsapp_orders # New collection for orders

STATE_IDLE = 'idle'
STATE_LISTING_VENDORS = 'listing_vendors'
STATE_LISTING_MENU = 'listing_menu'
STATE_SELECTING_VENDOR = 'selecting_vendor'
STATE_ADDING_ITEMS = 'adding_items'
STATE_CONFIRMING_ORDER = 'confirming_order'
STATE_AWAITING_DELIVERY_ADDRESS = 'awaiting_delivery_address'
STATE_ORDER_PLACED = 'order_placed'
STATE_AWAITING_ORDER_ID = 'awaiting_order_id'

def send_whatsapp_message(to_number: str, message: str) -> bool:
    """Sends a WhatsApp message using Twilio client from app config."""
    try:
        twilio_config = current_app.config['WHATSAPP_CONFIG']
        client = Client(twilio_config['account_sid'], twilio_config['auth_token'])
        from_number = twilio_config['whatsapp_number']

        client.messages.create(
            from_=f'whatsapp:{from_number}',
            body=message,
            to=f'whatsapp:{to_number}'
        )
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send WhatsApp message to {to_number}: {e}")
        return False

def handle_incoming_message(message_body: str, sender_id: str):
    """
    This function processes incoming WhatsApp messages.
    """
    
    # Get the user's session from MongoDB, or create a new one if it doesn't exist.
    session = sessions_collection.find_one({'_id': sender_id})
    if not session:
        session = {
            '_id': sender_id,
            'state': STATE_IDLE,
            'current_order': {} # Structured order object
        }
        sessions_collection.insert_one(session)

    message_lower = message_body.lower()
    response_message = ""

    if session['state'] == STATE_IDLE:
        if message_lower in ['hi', 'hello']:
            response_message = "Hello! Welcome to KwikConnect. You can type 'order' to start a new order, 'status' to check an existing order, or 'help' for more options."
        elif message_lower == 'order':
            session['state'] = STATE_LISTING_VENDORS
            vendors = Vendor.find_all()
            if vendors:
                vendor_list = "\n".join([f"{i+1}. {vendor.name}" for i, vendor in enumerate(vendors)])
                response_message = f"Great! Here are our available vendors:\n{vendor_list}\nPlease reply with the number of the vendor you'd like to order from."
            else:
                response_message = "Sorry, no vendors are currently available."
        elif message_lower == 'status':
            session['state'] = STATE_AWAITING_ORDER_ID
            response_message = "Please provide your order ID to check the status."
        elif message_lower == 'help':
            response_message = "You can use the following commands:\n- 'order': Start a new order.\n- 'status': Check the status of an order.\n- 'help': Show this help message."
        else:
            response_message = f"Sorry, I don't understand '{message_body}'. Type 'help' for a list of commands."

    elif session['state'] == STATE_LISTING_VENDORS:
        try:
            vendors = Vendor.find_all()
            vendor_index = int(message_body) - 1
            if 0 <= vendor_index < len(vendors):
                selected_vendor = vendors[vendor_index]
                session['current_order'] = {'sender_id': sender_id, 'vendor_id': str(selected_vendor._id), 'vendor_name': selected_vendor.name, 'items': [], 'status': 'pending', 'total': 0.0, 'vendor_whatsapp': selected_vendor.whatsapp_number}
                
                # Transition to listing menu
                session['state'] = STATE_LISTING_MENU
                products_for_vendor = Product.find_by_vendor(selected_vendor._id)
                if products_for_vendor:
                    menu_list = "\n".join([f"{i+1}. {p.name} (R{p.price:.2f})" for i, p in enumerate(products_for_vendor)])
                    response_message = f"You've selected {selected_vendor.name}. Here's their menu:\n{menu_list}\nPlease reply with the number of the item you'd like to add, or type 'done' to finish ordering."
                else:
                    response_message = f"Sorry, {selected_vendor.name} has no items available. Please select another vendor or type 'cancel'."
            else:
                response_message = "Invalid vendor number. Please choose a number from the list."
        except ValueError:
            response_message = "Invalid input. Please reply with the number of the vendor you'd like to order from."

    elif session['state'] == STATE_LISTING_MENU:
        if message_lower == 'done':
            if session['current_order']['items']:
                session['state'] = STATE_CONFIRMING_ORDER
                items_list = "\n".join([f"- {item['name']} (x{item['qty']}) @ R{item['price']:.2f}" for item in session['current_order']['items']])
                response_message = f"You want to order from {session['current_order']['vendor_name']} the following items:\n{items_list}\nTotal: R{session['current_order']['total']:.2f}\nIs this correct? (yes/no)"
            else:
                response_message = "You haven't added any items yet. Please add items by number, or type 'cancel' to stop the order."
        elif message_lower == 'cancel':
            session['state'] = STATE_IDLE
            session['current_order'] = {}
            response_message = "Order cancelled. How else can I help you?"
        else:
            try:
                product_index = int(message_body) - 1
                vendor_id = ObjectId(session['current_order']['vendor_id']) # Convert back to ObjectId
                products_for_vendor = Product.find_by_vendor(vendor_id)
                
                if 0 <= product_index < len(products_for_vendor):
                    selected_product = products_for_vendor[product_index]
                    
                    # Check if item already in cart, increment quantity
                    found = False
                    for item in session['current_order']['items']:
                        if item['_id'] == str(selected_product._id): # Compare string IDs
                            item['qty'] += 1
                            found = True
                            break
                    if not found:
                        session['current_order']['items'].append({'_id': str(selected_product._id), 'name': selected_product.name, 'price': selected_product.price, 'qty': 1})
                    
                    session['current_order']['total'] = sum(item['price'] * item['qty'] for item in session['current_order']['items'])
                    response_message = f"Added '{selected_product.name}'. Current total: R{session['current_order']['total']:.2f}. Add more items by number, or type 'done' to finish."
                else:
                    response_message = "Invalid item number. Please choose a number from the menu."
            except ValueError:
                response_message = "Invalid input. Please reply with the number of the item you'd like to add, or type 'done' to finish ordering."


    elif session['state'] == STATE_CONFIRMING_ORDER:
        if message_lower == 'yes':
            session['state'] = STATE_AWAITING_DELIVERY_ADDRESS
            response_message = "Great! Please provide your delivery address."
        elif message_lower == 'no':
            session['state'] = STATE_LISTING_MENU # Go back to menu to re-select
            response_message = "No problem. Please re-list your items by number, or type 'cancel' to stop the order."
        else:
            response_message = "Please respond with 'yes' or 'no'."

    elif session['state'] == STATE_AWAITING_DELIVERY_ADDRESS:
        session['current_order']['delivery_address'] = message_body
        
        # Save the order to the orders collection
        order_id = orders_collection.insert_one(session['current_order']).inserted_id
        
        # Notify vendor
        vendor_number = session['current_order']['vendor_whatsapp']
        customer_number = sender_id.replace('whatsapp:', '')
        order_details = "\n".join([f"- {item['name']} (x{item['qty']})" for item in session['current_order']['items']])
        vendor_notification_message = f"New Order (ID: {order_id}) from {customer_number} for {session['current_order']['vendor_name']}:\n{order_details}\nDelivery Address: {session['current_order']['delivery_address']}\nTotal: R{session['current_order']['total']:.2f}\nPlease confirm order."
        send_whatsapp_message(vendor_number, vendor_notification_message)

        session['state'] = STATE_IDLE
        session['current_order'] = {}
        response_message = f"Thank you! Your order (ID: {order_id}) from {session['current_order']['vendor_name']} has been placed and the vendor has been notified. We will send you an update shortly."

    elif session['state'] == STATE_AWAITING_ORDER_ID:
        try:
            order_id = ObjectId(message_body) # Convert string to ObjectId
            order = orders_collection.find_one({'_id': order_id})
            if order:
                response_message = f"Order ID: {order['_id']}\nVendor: {order['vendor_name']}\nStatus: {order['status']}\nItems: {', '.join([f'{item['name']} (x{item['qty']})' for item in order['items']])}\nTotal: R{order['total']:.2f}\nDelivery Address: {order.get('delivery_address', 'Not provided')}"
            else:
                response_message = "Order not found. Please check your Order ID."
        except Exception:
            response_message = "Invalid Order ID format. Please provide a valid Order ID."
        session['state'] = STATE_IDLE # Reset state after checking status

    # Save the updated session to MongoDB.
    sessions_collection.update_one({'_id': sender_id}, {'$set': session}, upsert=True)

    return response_message # Return just the message string
