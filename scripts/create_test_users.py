import requests

API_URL = "http://localhost:5000/api/v1/auth/register"

users = [
    {
        "email": "test_customer@example.com",
        "password": "Test1234",
        "username": "test_customer",
        "role": "customer"
    },
    {
        "email": "test_vendor@example.com",
        "password": "Test1234",
        "username": "test_vendor",
        "role": "vendor"
    },
    {
        "email": "test_courier@example.com",
        "password": "Test1234",
        "username": "test_courier",
        "role": "courier"
    }
]

for user in users:
    resp = requests.post(API_URL, json=user)
    print(f"Registering {user['role']} ({user['email']}): {resp.status_code}")
    try:
        print(resp.json())
    except Exception:
        print(resp.text)
