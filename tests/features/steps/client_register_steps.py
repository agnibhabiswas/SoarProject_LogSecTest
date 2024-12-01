import random
import string
from locust import HttpUser, task

class BDDTestUser(HttpUser):
    host = "http://127.0.0.1:5000"

    def generate_random_data(self):
        return {
            "fullName": ''.join(random.choices(string.ascii_letters, k=10)),
            "userName": ''.join(random.choices(string.ascii_lowercase, k=10)),
            "email": ''.join(random.choices(string.ascii_lowercase + string.digits, k=5)) + "@example.com",
            "password": ''.join(random.choices(string.ascii_letters + string.digits, k=8)),
            "phone": ''.join(random.choices(string.digits, k=10)),
        }

    @task
    def test_registration(self):
        register_data = self.generate_random_data()
        response = self.client.post("/client_registeration", data=register_data)
        assert response.status_code == 200, f"Registration failed: {response.text}"
