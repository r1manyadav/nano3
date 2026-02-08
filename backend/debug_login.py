import requests
import json

BASE_URL = "http://localhost:5000/api"

# Test student login
print("=== Testing Student Login ===")
login_response = requests.post(f"{BASE_URL}/auth/student-login", json={
    "email": "nano1",
    "password": "nano1"
})

print(f"Status: {login_response.status_code}")
print(f"Response: {json.dumps(login_response.json(), indent=2)}")

if login_response.status_code == 200:
    token = login_response.json()['access_token']
    print(f"\nToken obtained: {token[:50]}...")
    
    # Test results endpoint
    print("\n=== Testing /api/results ===")
    headers = {"Authorization": f"Bearer {token}"}
    result = requests.get(f"{BASE_URL}/results", headers=headers)
    print(f"Status: {result.status_code}")
    
    if result.status_code == 200:
        data = result.json()
        print(f"Number of results: {len(data)}")
        if len(data) > 0:
            print(f"\nFirst Result:")
            print(json.dumps(data[0], indent=2, default=str))
    else:
        print(f"Error: {result.text}")

