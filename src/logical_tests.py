import requests
from src.config import BASE_URL, ENDPOINTS

def test_register_input_validation():
    url = f"{BASE_URL}{ENDPOINTS['register']}"
    invalid_data = [
        {"fullName": "", "userName": "user1", "email": "user1@example.com", "password": "123", "phone": "12345"},
        {"fullName": "John", "userName": "johndoe", "email": "not-an-email", "password": "12345", "phone": "9876543210"}
    ]

    for data in invalid_data:
        response = requests.post(url, data=data)
        print(f"Testing data: {data} => Status Code: {response.status_code}, Response: {response.text}")
