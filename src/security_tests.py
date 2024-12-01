import requests
from src.config import BASE_URL, ENDPOINTS, SQL_PAYLOADS, XSS_PAYLOADS

def test_sql_injection():
    url = f"{BASE_URL}{ENDPOINTS['login']}"
    for payload in SQL_PAYLOADS:
        data = {"userName": payload, "email": "test@example.com", "password": "test"}
        response = requests.post(url, data=data)
        if "Error" not in response.text:
            print(f"Possible SQL Injection vulnerability with payload: {payload}")
        else:
            print(f"Safe against SQL Injection for payload: {payload}")

def test_xss():
    url = f"{BASE_URL}{ENDPOINTS['register']}"
    for payload in XSS_PAYLOADS:
        data = {"fullName": payload, "userName": "user", "email": "test@example.com", "password": "test", "phone": "1234567890"}
        response = requests.post(url, data=data)
        if payload in response.text:
            print(f"Possible XSS vulnerability with payload: {payload}")
        else:
            print(f"Safe against XSS for payload: {payload}")
