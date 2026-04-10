import requests
import subprocess
import time
import os

def test_reset():
    print("Starting server locally...")
    # Start the server process
    proc = subprocess.Popen(["python", "-m", "server.app"])
    time.sleep(5)  # Wait for startup

    url = "http://127.0.0.1:7860/reset"
    headers = {"Content-Type": "application/json"}
    
    # Test cases to simulate autograder
    test_cases = [
        ("Empty Body", {}),
        ("Standard task_name", {"task_name": "easy"}),
        ("Legacy difficulty", {"difficulty": "medium"}),
    ]

    success = True
    for label, payload in test_cases:
        try:
            print(f"Testing {label} POST request...")
            resp = requests.post(url, json=payload, headers=headers)
            if resp.status_code == 200:
                print(f"Success: {resp.json()}")
            else:
                print(f"Failed: {resp.status_code} - {resp.text}")
                success = False
        except Exception as e:
            print(f"Error: {e}")
            success = False

    print("Shutting down server...")
    proc.terminate()
    return success

if __name__ == "__main__":
    if test_reset():
        print("All Reset tests passed locally!")
    else:
        print("Reset tests failed.")
        exit(1)
