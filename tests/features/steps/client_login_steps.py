import random
import string
from locust import HttpUser, task

class BDDTestUser(HttpUser):
    host = "http://127.0.0.1:5000"

    @task
    def test_login(self):
        # Replace with actual login data or dynamically fetched data
        login_data = {
            "userName": "testUser",
            "email": "testUser@example.com",
            "password": "password123"
        }
        response = self.client.post("/client_login", data=login_data)
        assert response.status_code == 200, f"Login failed: {response.text}"