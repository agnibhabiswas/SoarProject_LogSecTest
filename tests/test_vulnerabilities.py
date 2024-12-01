import unittest
import requests
import logging
from concurrent.futures import ThreadPoolExecutor
from src.bug_reporter import write_bug_report

BASE_URL = "http://127.0.0.1:5000"

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class TestVulnerabilities(unittest.TestCase):

    # 1. XSS Attack in login request
    def test_xss_attack(self):
        payload = {
            "userName": "<script>alert('XSS')</script>",
            "email": "johndoe@example.com",
            "password": "67890"
        }
        logger.info("Testing XSS attack with payload: %s", payload)
        response = requests.post(f"{BASE_URL}/client_login", data=payload)

        if response.status_code != 200:
            bug_data = [
                "XSS Attack failed",
                "XSS attack did not bypass or trigger expected response",
                "High",
                "8/10",
                f"Payload: {payload}"
            ]
            write_bug_report(bug_data)
            logger.error("XSS attack failed with status code: %d", response.status_code)
        else:
            logger.info("XSS attack test passed.")

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("token", response.json())

    # 2. Simultaneous multiple requests (concurrency test)
    def test_concurrent_requests(self):
        def login_request():
            payload = {
                "userName": "johndoe",
                "email": "john.doe@example.com",
                "password": "67890"
            }
            logger.info("Sending concurrent login request with payload: %s", payload)
            response = requests.post(f"{BASE_URL}/client_login", data=payload)
            if response.status_code != 200:
                bug_data = [
                    "Concurrent request failed",
                    "Concurrency test returned non-200 status code",
                    "Medium",
                    "6/10",
                    f"Payload: {payload}"
                ]
                write_bug_report(bug_data)
                logger.error("Concurrent request failed with status code: %d", response.status_code)
            else:
                logger.info("Concurrent login request passed.")

            self.assertEqual(response.status_code, 200)

        with ThreadPoolExecutor(max_workers=10) as executor:
            logger.info("Starting concurrent requests...")
            executor.map(login_request, range(10))

    # 3. JWT Token Expiry
    def test_expired_token(self):
        expired_token = "expired-jwt-token-placeholder"  # Replace with an actual expired token if available
        headers = {
            "Authorization": f"Bearer {expired_token}"
        }
        response = requests.get(f"{BASE_URL}/client_data", headers=headers)
        if response.status_code != 401:
            bug_data = [
                "Expired JWT token not handled correctly",
                "Expired JWT token did not return expected 401 status code",
                "High",
                "9/10",
                f"Token: {expired_token}"
            ]
            write_bug_report(bug_data)
            logger.error("Expired token test failed with status code: %d", response.status_code)
        else:
            logger.info("Expired token test passed.")

        self.assertEqual(response.status_code, 401)

if __name__ == "__main__":
    unittest.main()
