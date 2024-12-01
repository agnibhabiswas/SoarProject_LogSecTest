import unittest
import requests
import logging
from src.bug_reporter import write_bug_report

BASE_URL = "http://127.0.0.1:5000"

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class TestClientLogin(unittest.TestCase):

    # 1. Test case: Valid login
    def test_valid_login(self):
        payload = {
            "userName": "johndoe",
            "email": "john.doe@example.com",
            "password": "67890"
        }
        response = requests.post(f"{BASE_URL}/client_login", data=payload)
        if response.status_code != 200:
            bug_data = [
                "Valid login failed",
                "Valid login credentials returned non-200 status code",
                "High",
                "8/10",
                "1. Send valid login request"
            ]
            write_bug_report(bug_data)
            logger.error("Test failed: Valid login returned non-200 status code.")
        else:
            logger.info("Valid login test passed.")

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    # 2. Test case: Invalid email
    def test_invalid_email_login(self):
        payload = {
            "userName": "johndoe",
            "email": "wrong.email@example.com",
            "password": "67890"
        }
        response = requests.post(f"{BASE_URL}/client_login", data=payload)
        if response.status_code != 200:
            bug_data = [
                "Invalid email login failed",
                "Incorrect email does not trigger expected error",
                "High",
                "7/10",
                "1. Send login request with invalid email"
            ]
            write_bug_report(bug_data)
            logger.error("Test failed: Invalid email login did not return expected error.")
        else:
            logger.info("Invalid email login test passed.")

        self.assertEqual(response.status_code, 200)
        self.assertIn("msg", response.json())
        self.assertEqual(response.json()["msg"], "In correct email or password")

    # 3. Test case: Invalid password
    def test_invalid_password_login(self):
        payload = {
            "userName": "johndoe",
            "email": "john.doe@example.com",
            "password": "wrongpassword"
        }
        response = requests.post(f"{BASE_URL}/client_login", data=payload)
        if response.status_code != 200:
            bug_data = [
                "Invalid password login failed",
                "Incorrect password does not trigger expected error",
                "High",
                "7/10",
                "1. Send login request with incorrect password"
            ]
            write_bug_report(bug_data)
            logger.error("Test failed: Invalid password login did not return expected error.")
        else:
            logger.info("Invalid password login test passed.")

        self.assertEqual(response.status_code, 200)
        self.assertIn("msg", response.json())
        self.assertEqual(response.json()["msg"], "In correct email or password")

    # 4. Edge case: Empty fields in the request
    def test_empty_fields(self):
        payload = {
            "userName": "",
            "email": "",
            "password": ""
        }
        response = requests.post(f"{BASE_URL}/client_login", data=payload)
        if response.status_code != 400:
            bug_data = [
                "Empty fields not handled properly",
                "Empty fields did not return the expected error code",
                "Medium",
                "6/10",
                "1. Send login request with empty fields"
            ]
            write_bug_report(bug_data)
            logger.error("Test failed: Empty fields did not return 400 status code.")
        else:
            logger.info("Empty fields test passed.")

        self.assertEqual(response.status_code, 400)
        self.assertIn("msg", response.json())

    # 5. Edge case: SQL injection in email
    def test_sql_injection_in_email(self):
        payload = {
            "userName": "johndoe",
            "email": "' OR 1=1 --",  # SQL injection attempt
            "password": "password123"
        }
        response = requests.post(f"{BASE_URL}/client_login", data=payload)
        if response.status_code != 400:
            bug_data = [
                "SQL injection not properly handled",
                "SQL injection attempt did not return expected error code",
                "High",
                "8/10",
                "1. Send login request with SQL injection in email"
            ]
            write_bug_report(bug_data)
            logger.error("Test failed: SQL injection in email did not return expected error code.")
        else:
            logger.info("SQL injection in email test passed.")

        self.assertEqual(response.status_code, 400)
        self.assertIn("msg", response.json())

    # 6. Edge case: Brute force (multiple failed attempts)
    def test_brute_force(self):
        for _ in range(10):
            payload = {
                "userName": "johndoe",
                "email": "wrong.email@example.com",
                "password": "wrongpassword"
            }
            response = requests.post(f"{BASE_URL}/client_login", data=payload)
            if response.status_code == 429:
                break
        if response.status_code != 429:
            bug_data = [
                "Brute force protection not triggered",
                "Brute force failed to return 429 status code after multiple failed attempts",
                "High",
                "9/10",
                "1. Send multiple failed login attempts"
            ]
            write_bug_report(bug_data)
            logger.error("Test failed: Brute force did not trigger rate limit.")
        else:
            logger.info("Brute force protection test passed.")

        self.assertEqual(response.status_code, 429)
        self.assertIn("msg", response.json())

    # 7. Test case: Weak password (low complexity)
    def test_weak_password(self):
        payload = {
            "userName": "johndoe",
            "email": "john.doe@example.com",
            "password": "12345"  # Weak password
        }
        response = requests.post(f"{BASE_URL}/client_login", data=payload)
        if response.status_code == 200:
            bug_data = [
                "Weak password accepted",
                "Weak password was accepted despite low complexity",
                "High",
                "8/10",
                "1. Send login request with weak password"
            ]
            write_bug_report(bug_data)
            logger.error("Test failed: Weak password accepted.")
        else:
            logger.info("Weak password test passed.")

        self.assertNotEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
