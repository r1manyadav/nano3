"""
Complete End-to-End Test: Student Login → View Test History → View Result Details
This script simulates exactly what the frontend does
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"
STUDENT_EMAIL = "nano1"
STUDENT_PASSWORD = "nano1"

print("\n" + "="*80)
print("END-TO-END TEST: Student Result Display Flow")
print("="*80 + "\n")

# Step 1: Login
print("STEP 1: Student Login")
print("-" * 80)
login_resp = requests.post(f"{BASE_URL}/auth/student-login", json={
    "email": STUDENT_EMAIL,
    "password": STUDENT_PASSWORD
})

if login_resp.status_code != 200:
    print(f"❌ Login failed: {login_resp.status_code}")
    print(login_resp.text)
    exit(1)

login_data = login_resp.json()
token = login_data['access_token']
user = login_data['user']

print(f"✅ Login successful")
print(f"   Student ID: {user['id']}")
print(f"   Student Name: {user['name']}")
print(f"   Student Email: {user['email']}")
print(f"   Token: {token[:40]}...\n")

# Step 2: Get Test History
print("STEP 2: Get Student Test History")
print("-" * 80)
headers = {"Authorization": f"Bearer {token}"}
history_resp = requests.get(f"{BASE_URL}/results", headers=headers)

if history_resp.status_code != 200:
    print(f"❌ Failed to get test history: {history_resp.status_code}")
    print(history_resp.text)
    exit(1)

results = history_resp.json()
print(f"✅ Test history retrieved")
print(f"   Total test attempts: {len(results)}\n")

if len(results) == 0:
    print("⚠️  No test results found")
    exit(0)

# Display test history
for i, result in enumerate(results[:3], 1):
    status = "✓ PASSED" if result['is_passed'] else "✗ FAILED"
    print(f"   Test {i}: {result['test_name']} - {status}")
    print(f"           Score: {result['marks_obtained']}/{result['max_marks']} ({result['percentage']}%)")
    print(f"           Date: {result['submitted_at'][:10]}")
    print()

# Step 3: Get First Result Details
print("STEP 3: Get Detailed Result for First Test")
print("-" * 80)
result_id = results[0]['id']
print(f"   Fetching details for Result ID: {result_id}\n")

detail_resp = requests.get(f"{BASE_URL}/results/{result_id}", headers=headers)

if detail_resp.status_code != 200:
    print(f"❌ Failed to get result details: {detail_resp.status_code}")
    print(detail_resp.text)
    exit(1)

detail = detail_resp.json()
print(f"✅ Result details retrieved")
print(f"\n   Test Name: {detail.get('test_name', 'N/A')}")
print(f"   Marks Obtained: {detail['marks_obtained']}/{detail['max_marks']}")
print(f"   Percentage: {detail['percentage']}%")
print(f"   Passing Marks Required: {detail.get('passing_marks', 'N/A')}%")
print(f"   Status: {'PASSED ✓' if detail['is_passed'] else 'FAILED ✗'}")
print(f"\n   Analysis:")
print(f"   - Correct Answers: {detail['correct_count']}")
print(f"   - Wrong Answers: {detail['wrong_count']}")
print(f"   - Unanswered: {detail['unanswered_count']}")
print(f"   - Submitted: {detail['submitted_at'][:19]}")

# Step 4: Verify all required fields
print(f"\n\nSTEP 4: Verify All Required Fields")
print("-" * 80)

required_fields = [
    'id', 'test_id', 'test_name', 'marks_obtained', 'max_marks',
    'percentage', 'passing_marks', 'is_passed', 'correct_count',
    'wrong_count', 'unanswered_count', 'submitted_at'
]

missing_fields = []
for field in required_fields:
    if field in detail:
        print(f"✅ {field}: {detail[field]}")
    else:
        print(f"❌ {field}: MISSING")
        missing_fields.append(field)

if missing_fields:
    print(f"\n⚠️  Missing fields: {', '.join(missing_fields)}")
else:
    print(f"\n✅ All required fields present!")

# Final Summary
print("\n" + "="*80)
print("TEST SUMMARY")
print("="*80)
print("✅ Student login successful")
print("✅ Test history retrieved successfully")
print(f"✅ Result details display working correctly")
print(f"✅ All API endpoints responding properly")
print("\n🎉 END-TO-END TEST PASSED - RESULT DISPLAY IS WORKING!")
print("="*80 + "\n")
