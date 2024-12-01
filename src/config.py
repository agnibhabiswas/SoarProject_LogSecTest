BASE_URL = "http://127.0.0.1:5000"

ENDPOINTS = {
    "register": "/client_registeration",
    "login": "/client_login"
}

SQL_PAYLOADS = ["' OR '1'='1", "' OR 1=1 --", "'; DROP TABLE users; --"]
XSS_PAYLOADS = ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>"]
