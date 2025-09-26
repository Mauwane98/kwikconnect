# Script to register all user roles in the backend
import requests

BASE_URL = "http://localhost:5000"  # Change if your backend runs on a different port
REGISTER_ENDPOINT = f"{BASE_URL}/api/v1/auth/register"

users = [
    {
        "username": "customer1",
        "email": "customer1@example.com",
        "password": "CustomerPass123",
        "role": "customer"
    },
    {
        "username": "vendor1",
        "email": "vendor1@example.com",
        "password": "VendorPass123",
        "role": "vendor"
    },
    {
        "username": "courier1",
        "email": "courier1@example.com",
        "password": "CourierPass123",
        "role": "courier"
    }
]

def register_user(user):
    response = requests.post(REGISTER_ENDPOINT, json=user)
    try:
        data = response.json()
    except Exception:
        data = response.text
    print(f"Registering {user['role']} ({user['email']}): {response.status_code} - {data}")

if __name__ == "__main__":
    for user in users:
        register_user(user)
