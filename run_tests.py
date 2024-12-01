from src.logical_tests import test_register_input_validation
from src.security_tests import test_sql_injection, test_xss


def run_all_tests():
    print("Running Logical Tests...")
    test_register_input_validation()

    print("\nRunning Security Tests...")
    test_sql_injection()
    test_xss()


if __name__ == "__main__":
    run_all_tests()
