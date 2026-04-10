import requests
import time
import subprocess
import os

def test_reset_endpoint():
    print("Starting local server for validation...")
    # Start the server in the background
    server_process = subprocess.Popen(["python", "-m", "server.app"])
    time.sleep(5)  # Wait for server to start

    try:
        # Test 1: Health Check
        print("Testing /health endpoint...")
        health_resp = requests.get("http://127.0.0.1:7860/health")
        print(f"Health Response: {health_resp.status_code} - {health_resp.json()}")

        # Test 2: Reset Endpoint (POST)
        print("Testing /reset endpoint (POST)...")
        # Most OpenEnv autograders send an empty JSON body
        reset_resp = requests.post("http://127.0.0.1:7860/reset", json={})
        
        if reset_resp.status_code == 200:
            print("SUCCESS: /reset returned 200 OK")
            print(f"Observation: {reset_resp.json()}")
        else:
            print(f"FAILURE: /reset returned {reset_resp.status_code}")
            print(f"Response: {reset_resp.text}")

    except Exception as e:
        print(f"Error during test: {e}")
    finally:
        print("Shutting down server...")
        server_process.terminate()

if __name__ == "__main__":
    test_reset_endpoint()
