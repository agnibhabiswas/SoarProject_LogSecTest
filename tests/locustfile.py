import os
import logging
from locust import HttpUser, task, between
import random
import string

# Ensure logs directory exists
log_dir = "../logs"
os.makedirs(log_dir, exist_ok=True)

# Set up basic logging to file
logger = logging.getLogger('locust')
logger.setLevel(logging.INFO)

# Create a file handler to store logs in the logs folder
file_handler = logging.FileHandler(os.path.join(log_dir, 'locust_log.txt'))
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class LoadTestUser(HttpUser):
    host = "http://127.0.0.1:5000"  # Replace with your Flask app URL
    wait_time = between(1, 2)  # Wait time between tasks

    @task
    def client_register(self):
        # Generate random data for registration
        self.register_data = {
            "fullName": ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=10)),
            "userName": ''.join(random.choices(string.ascii_lowercase, k=10)),
            "email": ''.join(random.choices(string.ascii_lowercase + string.digits, k=5)) + "@example.com",
            "password": ''.join(random.choices(string.ascii_letters + string.digits, k=8)),
            "phone": ''.join(random.choices(string.digits, k=10))
        }

        # Log the request data for debugging
        logger.info(f"Sending registration request: {self.register_data}")

        # Send the POST request as form data
        response = self.client.post("/client_registeration", data=self.register_data)

        # Log the response details
        logger.info(f"Registration response: {response.status_code} - {response.text}")

        if response.status_code != 200:
            # Log error details if the request fails
            logger.error(f"Registration failed with status code {response.status_code}: {response.text}")
        else:
            # Log success details
            logger.info(f"Registration successful: {response.status_code}")

    @task
    def client_login(self):
        # Ensure registration happened first by checking if `register_data` exists
        if hasattr(self, 'register_data'):
            login_data = {
                "userName": self.register_data["userName"],  # Use registered userName
                "email": self.register_data["email"],  # Use registered email
                "password": self.register_data["password"]
            }

            # Log the request data for debugging
            logger.info(f"Sending login request with registered data: {login_data}")

            # Send the POST request as form data
            response = self.client.post("/client_login", data=login_data)

            # Log the response details
            logger.info(f"Login response: {response.status_code} - {response.text}")

            if response.status_code != 200:
                # Log error details if the request fails
                logger.error(f"Login failed with status code {response.status_code}: {response.text}")
            else:
                # Log success details
                logger.info(f"Login successful: {response.status_code}")
        else:
            logger.warning("Attempted login before registration data was available")
