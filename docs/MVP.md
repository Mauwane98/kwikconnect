KwikConnect - MVP Specification

Goal
----
Create a hyper-local delivery & errands platform built for kasi and rural areas. The MVP focuses on enabling local vendors (spazas, butcheries, pharmacies, taverns, street food, supermarkets) to offer delivery via community couriers (bicycle, scooter, car) and support ordering via web, WhatsApp, SMS, or phone.

High-level user stories
-----------------------
- As a customer, I can browse local vendors, add items to cart, checkout, and view order history.
- As a vendor, I can register, manage products, set operating hours, and see incoming orders.
- As a courier, I can sign up (choose vehicle), accept delivery jobs, update order status, and earn money.
- As an admin, I can view vendors, approve vendor accounts, and monitor platform activity.

Important design constraints
---------------------------
- Mobile-first and low-bandwidth friendly.
- Support ordering via WhatsApp/SMS/phone (prefilled WhatsApp messages + a backend endpoint to register phone/WhatsApp orders).
- Support bicycle couriers by design (allow "bicycle" as a vehicle type).
- Keep fees low and allow COD (cash-on-delivery) as default; add online payment later.

Data contracts (minimal)
-------------------------
User (Customer/Vendor/Courier)
- id: int
- email: string
- full_name: string
- phone: string
- role: enum[customer,vendor,courier,admin]
- registered_at: timestamp

Vendor
- id, user_id, business_name, description, address, latitude, longitude, is_approved, is_open, operating_hours

Product
- id, vendor_id, name, price_cents, description, image_url, is_available

Courier
- id, user_id, vehicle_type (bicycle/scooter/car), is_active, last_known_location

Order
- id, customer_id, vendor_id, courier_id (nullable), items: [{product_id, qty, price_cents}], total_cents, status(enum: pending, accepted, picked_up, delivered, cancelled), address, phone, created_at

APIs (versioned)
-----------------
Base prefix: /api/v1/
- POST /api/v1/auth/register {email,password,full_name,role} -> 201 {access_token,user}
- POST /api/v1/auth/login {email,password} -> 200 {access_token,user}
- GET /api/v1/vendors -> 200 [{vendor}]
- GET /api/v1/vendors/:id -> 200 {vendor}
- POST /api/v1/vendors (vendor onboarding) -> 201 {vendor}
- GET /api/v1/products?vendor_id= -> 200 [{product}]
- POST /api/v1/orders {customer_id,items,address,phone,payment_method} -> 201 {order}
- GET /api/v1/orders/:id -> 200 {order}
- POST /api/v1/couriers/apply {user details, vehicle_type} -> 201 {application}
- POST /api/v1/whatsapp-order {message, phone, parsed_items, customer_info} -> 201 {order}

Authentication
--------------
- Use JWT access tokens returned at login/register. Tokens stored by frontend and sent in Authorization: Bearer <token>.

Success criteria (MVP)
----------------------
- A user can register and login (customer/vendor/courier).
- Vendors can be created and listed.
- A customer can create an order and see it in order history.
- Couriers can accept an order and update its status.
- WhatsApp/phone orders can be created through a simple endpoint.

Edge cases
----------
- Offline/low-bandwidth: allow orders by phone/WhatsApp by registering from staff side.
- Partial fulfillments (item out of stock): vendor/courier flow to mark items unavailable.
- Payment failures: support COD as fallback.
- Duplicate orders: protect with idempotency keys where possible.

Next steps (implementation plan)
--------------------------------
1. Finalize DB models and run migrations.
2. Implement auth (register/login) and role-based redirects.
3. Implement vendor onboarding and product management.
4. Implement courier onboarding and assignment flow.
5. Implement order creation, cart persistence, and order status updates.
6. Add WhatsApp/order by phone helper endpoints and UI hints.
7. Add tests and prepare Docker Compose for local dev.


Additional Feature: Running errands for you
-------------------------------------------
Everyday Errands Made Easy

KwikConnect is more than just deliveries—our couriers help with the tasks that really matter in kasi and rural life:

- 💊 Collect Medication: We’ll fetch your prescriptions or clinic medication, so you don’t have to wait in long lines or travel far.
- 📦 Send & Receive Parcels: Need to drop off or collect a small package, groceries, or important documents? We’ll handle it for you.
- 🧹 Household Errands: Need someone to fetch water, buy paraffin, or help with other household essentials? We’re here to assist.
- 🛒 Grocery Top-Ups: Forgot something at the shop or need a quick top-up from the spaza? We’ll pick it up and deliver to your door.
- 🛢️ Gas/Refill Exchange: Need to swap or refill your gas cylinder or paraffin container? We’ll handle the exchange and bring it to your door.

No more long walks or waiting in queues—KwikConnect brings real convenience to your doorstep.


