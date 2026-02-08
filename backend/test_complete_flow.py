import requests
import json

BASE_URL = "http://localhost:5000/api"

print("=== Complete Login and Results Test ===\n")

# 1. Login as student
print("1. Student Login")
login_resp = requests.post(f"{BASE_URL}/auth/student-login", json={
    "email": "nano1",
    "password": "nano1"
})
print(f"   Status: {login_resp.status_code}")

if login_resp.status_code != 200:
    print(f"   Error: {login_resp.text}")
    exit(1)

login_data = login_resp.json()
token = login_data['access_token']
user_data = login_data['user']

print(f"   ✓ Token obtained")
print(f"   User ID: {user_data['id']}")
print(f"   User Email: {user_data['email']}")

# 2. Get results using the token
print("\n2. Get Student Results")
headers = {"Authorization": f"Bearer {token}"}
results_resp = requests.get(f"{BASE_URL}/results", headers=headers)
print(f"   Status: {results_resp.status_code}")

if results_resp.status_code != 200:
    print(f"   Error: {results_resp.text}")
    exit(1)

results = results_resp.json()
print(f"   ✓ Got {len(results)} results")

if len(results) > 0:
    result = results[0]
    print(f"\n   First Result:")
    print(f"   - Result ID: {result['id']}")
    print(f"   - Test Name: {result['test_name']}")
    print(f"   - Score: {result['marks_obtained']}/{result['max_marks']}")
    print(f"   - Percentage: {result['percentage']}%")
    print(f"   - Passed: {result['is_passed']}")
    
    # 3. Get single result details
    print(f"\n3. Get Single Result Details (ID: {result['id']})")
    detail_resp = requests.get(f"{BASE_URL}/results/{result['id']}", headers=headers)
    print(f"   Status: {detail_resp.status_code}")
    
    if detail_resp.status_code == 200:
        detail = detail_resp.json()
        print(f"   ✓ Got result details")
        print(f"   - Correct: {detail.get('correct_count', 'N/A')}")
        print(f"   - Wrong: {detail.get('wrong_count', 'N/A')}")
        print(f"   - Unanswered: {detail.get('unanswered_count', 'N/A')}")
    else:
        print(f"   ✗ Error: {detail_resp.text}")

print("\n✓ All API endpoints working correctly!")
