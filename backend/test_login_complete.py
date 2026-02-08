import requests
import json

BASE_URL = "http://localhost:5000/api"

print("=" * 60)
print("COMPREHENSIVE LOGIN & APP TESTING")
print("=" * 60)

# Test 1: Teacher Login
print("\n[TEST 1] Teacher Login")
print("-" * 60)
teacher_login_response = requests.post(f"{BASE_URL}/auth/teacher-login", json={
    "teacher_id": "nano123",
    "password": "nano123"
})

print(f"Status: {teacher_login_response.status_code}")
if teacher_login_response.status_code == 200:
    teacher_data = teacher_login_response.json()
    teacher_token = teacher_data['access_token']
    print(f"✓ Teacher Login SUCCESS")
    print(f"  User: {teacher_data['user']['teacher_id']}")
    print(f"  Token: {teacher_token[:30]}...")
else:
    print(f"✗ Teacher Login FAILED: {teacher_login_response.text}")
    teacher_token = None

# Test 2: Student Login
print("\n[TEST 2] Student Login")
print("-" * 60)
student_login_response = requests.post(f"{BASE_URL}/auth/student-login", json={
    "email": "testuser@example.com",
    "password": "test123"
})

print(f"Status: {student_login_response.status_code}")
if student_login_response.status_code == 200:
    student_data = student_login_response.json()
    student_token = student_data['access_token']
    print(f"✓ Student Login SUCCESS")
    print(f"  User: {student_data['user']['email']}")
    print(f"  Token: {student_token[:30]}...")
else:
    print(f"✗ Student Login FAILED: {student_login_response.text}")
    student_token = None

# Test 3: Create a Test (as Teacher)
if teacher_token:
    print("\n[TEST 3] Create Test")
    print("-" * 60)
    test_data = {
        "name": "Sample Quiz",
        "description": "A test quiz for demonstration",
        "duration": 30,
        "passing_marks": 40,
        "questions": [
            {
                "text": "What is 2 + 2?",
                "optionA": "3",
                "optionB": "4",
                "optionC": "5",
                "optionD": "6",
                "correct": "B"
            },
            {
                "text": "What is the capital of France?",
                "optionA": "London",
                "optionB": "Berlin",
                "optionC": "Paris",
                "optionD": "Madrid",
                "correct": "C"
            }
        ]
    }
    
    create_test_response = requests.post(
        f"{BASE_URL}/tests",
        json=test_data,
        headers={"Authorization": f"Bearer {teacher_token}"}
    )
    
    print(f"Status: {create_test_response.status_code}")
    if create_test_response.status_code == 201:
        test_info = create_test_response.json()
        test_id = test_info['test']['id']
        print(f"✓ Test Created Successfully")
        print(f"  Test ID: {test_id}")
        print(f"  Name: {test_info['test']['name']}")
    else:
        print(f"✗ Test Creation FAILED: {create_test_response.text}")
        test_id = None

# Test 4: Get Tests (as Student)
if student_token:
    print("\n[TEST 4] Get Available Tests")
    print("-" * 60)
    get_tests_response = requests.get(
        f"{BASE_URL}/tests",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    
    print(f"Status: {get_tests_response.status_code}")
    if get_tests_response.status_code == 200:
        tests = get_tests_response.json()
        print(f"✓ Retrieved {len(tests)} test(s)")
        if tests:
            print(f"  First Test: {tests[0]['name']}")

# Test 5: Health Check
print("\n[TEST 5] Health Check")
print("-" * 60)
health_response = requests.get(f"{BASE_URL}/health")
print(f"Status: {health_response.status_code}")
if health_response.status_code == 200:
    print(f"✓ Backend Health: OK")
else:
    print(f"✗ Health Check FAILED")

print("\n" + "=" * 60)
print("TESTING COMPLETED")
print("=" * 60)
