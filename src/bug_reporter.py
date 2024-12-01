import csv
import os
import datetime

# Define the CSV file name
BUG_REPORT_FILE = "bug_report.csv"

# Function to write bug report into a CSV file
def write_bug_report(bug_data):
    # Check if the CSV file exists. If not, create it and write headers.
    file_exists = os.path.isfile(BUG_REPORT_FILE)

    with open(BUG_REPORT_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write headers if file does not exist
        if not file_exists:
            writer.writerow(["Bug Title", "Bug Description", "Severity", "Priority", "Steps to Reproduce"])

        # Add a separator line before each test run (timestamp)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([f"--- Test Run started at: {timestamp} ---"])  # Timestamp separator
        writer.writerow([",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,"])  # Comma separator

        # Write the bug report details
        writer.writerow(bug_data)

        # Add a separator line after each test run
        writer.writerow([",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,"])  # Comma separator

        print("Bug report written to CSV.")

# Example usage
# if __name__ == "__main__":
#     bug_data = [
#         "Brute force protection not triggered",
#         "Brute force failed to return 429 status code after multiple failed attempts",
#         "High",
#         "9/10",
#         "1. Send multiple failed login attempts"
#     ]
#     write_bug_report(bug_data)
