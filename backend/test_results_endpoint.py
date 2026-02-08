import requests
import json

BASE_URL = "http://localhost:5000/api"

# Get a student token
login_response = requests.post(f"{BASE_URL}/students/login", json={
    "email": "nano1",
    "password": "nano1"
})

if login_response.status_code == 200:
    token = login_response.json()['token']
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n=== Testing /api/results endpoint ===")
    result = requests.get(f"{BASE_URL}/results", headers=headers)
    print(f"Status: {result.status_code}")
    
    if result.status_code == 200:
        data = result.json()
        print(f"Results count: {len(data)}")
        if len(data) > 0:
            print(f"\nFirst Result:")
            print(json.dumps(data[0], indent=2, default=str))
        else:
            print("No results found")
    else:
        print(f"Error: {result.text}")
else:
    print("Failed to login")
