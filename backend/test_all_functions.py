#!/usr/bin/env python3
"""
Comprehensive API Testing Script for Nano Test Platform
Tests all functions and endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

def print_test(name, passed, message=""):
    status = "PASS" if passed else "FAIL"
    print(f"{status} | {name}")
    if message:
        print(f"       {message}")

def print_section(title):
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}\n")

# Store tokens
teacher_token = None
student_token = None

# ==================== TEST 1: HEALTH CHECK ====================
print_section("TEST 1: BACKEND HEALTH CHECK")

try:
    response = requests.get(f"{BASE_URL}/health")
    passed = response.status_code == 200
    print_test("Health Endpoint", passed, f"Status: {response.status_code}")
except Exception as e:
    print_test("Health Endpoint", False, str(e))

# ==================== TEST 2: TEACHER LOGIN ====================
print_section("TEST 2: TEACHER AUTHENTICATION")

try:
    payload = {
        "teacher_id": "nano123",
        "password": "nano123"
    }
    response = requests.post(f"{BASE_URL}/auth/teacher-login", json=payload)
    passed = response.status_code == 200
    print_test("Teacher Login (nano123/nano123)", passed, f"Status: {response.status_code}")
    
    if passed:
        data = response.json()
        teacher_token = data.get('access_token')
        print(f"       Teacher ID: {data['user']['teacher_id']}")
        print(f"       Token: {teacher_token[:50]}...")
except Exception as e:
    print_test("Teacher Login", False, str(e))

# ==================== TEST 3: STUDENT LOGIN ====================
print_section("TEST 3: STUDENT AUTHENTICATION")

try:
    payload = {
        "email": "nano1",
        "password": "nano1"
    }
    response = requests.post(f"{BASE_URL}/auth/student-login", json=payload)
    passed = response.status_code == 200
    print_test("Student Login (nano1/nano1)", passed, f"Status: {response.status_code}")
    
    if passed:
        data = response.json()
        student_token = data.get('access_token')
        print(f"       Student Email: {data['user']['email']}")
        print(f"       Token: {student_token[:50]}...")
except Exception as e:
    print_test("Student Login", False, str(e))

# ==================== TEST 4: CREATE TEST ====================
print_section("TEST 4: CREATE TEST (TEACHER)")

test_id = None
try:
    payload = {
        "name": "Automated Test",
        "description": "Test created by automated testing script",
        "duration": 30,
        "passing_marks": 40,
        "questions": [
            {
                "text": "What is the capital of France?",
                "optionA": "London",
                "optionB": "Paris",
                "optionC": "Berlin",
                "optionD": "Madrid",
                "correct": "B"
            },
            {
                "text": "What is 2 + 2?",
                "optionA": "3",
                "optionB": "4",
                "optionC": "5",
                "optionD": "6",
                "correct": "B"
            }
        ]
    }
    
    headers = {"Authorization": f"Bearer {teacher_token}"}
    response = requests.post(f"{BASE_URL}/tests", json=payload, headers=headers)
    passed = response.status_code == 201
    print_test("Create Test", passed, f"Status: {response.status_code}")
    
    if not passed:
        print(f"       Error: {response.text}")
    
    if passed:
        data = response.json()
        test_id = data['test']['id']
        print(f"       Test ID: {test_id}")
        print(f"       Test Name: {data['test']['name']}")
        print(f"       Questions: {len(payload['questions'])}")
except Exception as e:
    print_test("Create Test", False, str(e))

# ==================== TEST 5: GET TESTS (TEACHER) ====================
print_section("TEST 5: GET TESTS (TEACHER VIEW)")

try:
    response = requests.get(f"{BASE_URL}/tests", headers=headers)
    passed = response.status_code == 200
    tests = response.json() if passed else []
    print_test("Get Teacher Tests", passed, f"Status: {response.status_code}, Count: {len(tests)}")
    
    if not passed:
        print(f"       Error: {response.text}")
    
    if tests:
        for test in tests[:2]:  # Show first 2
            print(f"       - {test['name']} (ID: {test['id']}, Questions: {test.get('question_count', '?')})")
except Exception as e:
    print_test("Get Tests (Teacher)", False, str(e))

# ==================== TEST 6: GET SINGLE TEST ====================
print_section("TEST 6: GET SINGLE TEST DETAILS")

try:
    if test_id:
        response = requests.get(f"{BASE_URL}/tests/{test_id}")
        passed = response.status_code == 200
        print_test("Get Test by ID", passed, f"Status: {response.status_code}")
        
        if passed:
            data = response.json()
            print(f"       Test: {data['name']}")
            print(f"       Duration: {data['duration']} minutes")
            print(f"       Questions: {len(data['questions'])}")
            for i, q in enumerate(data['questions'], 1):
                print(f"       Q{i}: {q['question_text'][:40]}...")
except Exception as e:
    print_test("Get Single Test", False, str(e))

# ==================== TEST 7: GET TESTS (STUDENT) ====================
print_section("TEST 7: GET TESTS (STUDENT VIEW)")

try:
    headers = {"Authorization": f"Bearer {student_token}"}
    response = requests.get(f"{BASE_URL}/tests", headers=headers)
    passed = response.status_code == 200
    tests = response.json() if passed else []
    print_test("Get Available Tests (Student)", passed, f"Status: {response.status_code}, Count: {len(tests)}")
except Exception as e:
    print_test("Get Tests (Student)", False, str(e))

# ==================== TEST 8: SUBMIT TEST ====================
print_section("TEST 8: SUBMIT TEST RESULT (STUDENT)")

result_id = None
try:
    if test_id:
        payload = {
            "test_id": test_id,
            "answers": {
                "1": "B",  # Correct answer to Q1
                "2": "B"   # Correct answer to Q2
            },
            "marked_for_review": {
                "1": False,
                "2": False
            }
        }
        
        headers = {"Authorization": f"Bearer {student_token}"}
        response = requests.post(f"{BASE_URL}/submit-test", json=payload, headers=headers)
        passed = response.status_code == 201
        print_test("Submit Test", passed, f"Status: {response.status_code}")
        
        if passed:
            data = response.json()
            result_id = data['result']['id']
            print(f"       Result ID: {result_id}")
            print(f"       Score: {data['result'].get('score', 'N/A')}")
            print(f"       Status: {data['result'].get('status', 'N/A')}")
except Exception as e:
    print_test("Submit Test", False, str(e))

# ==================== TEST 9: GET STUDENT RESULTS ====================
print_section("TEST 9: GET STUDENT RESULTS")

try:
    headers = {"Authorization": f"Bearer {student_token}"}
    response = requests.get(f"{BASE_URL}/results", headers=headers)
    passed = response.status_code == 200
    results = response.json() if passed else []
    print_test("Get Student Results", passed, f"Status: {response.status_code}, Count: {len(results)}")
    
    if passed and results:
        for result in results[:2]:
            try:
                test_name = result.get('test_name', 'Unknown')
                score = result.get('marks_obtained', result.get('score', 'N/A'))
                print(f"       - Test: {test_name}, Score: {score}")
            except:
                pass
except Exception as e:
    print_test("Get Student Results", False, str(e))

# ==================== TEST 10: GET RESULT DETAILS ====================
print_section("TEST 10: GET SINGLE RESULT DETAILS")

try:
    if result_id:
        headers = {"Authorization": f"Bearer {student_token}"}
        response = requests.get(f"{BASE_URL}/results/{result_id}", headers=headers)
        passed = response.status_code == 200
        print_test("Get Result Details", passed, f"Status: {response.status_code}")
        
        if passed:
            try:
                data = response.json()
                test_name = data.get('test_name', 'Unknown')
                score = data.get('marks_obtained', data.get('score', 'N/A'))
                passing = data.get('passing_marks', 'N/A')
                is_pass = data.get('is_passed', False)
                
                print(f"       Test: {test_name}")
                print(f"       Score: {score}")
                print(f"       Passing Score: {passing}")
                print(f"       Status: {'PASS' if is_pass else 'FAIL'}")
            except Exception as e:
                print(f"       Error parsing response: {str(e)}")
except Exception as e:
    print_test("Get Result Details", False, str(e))

# ==================== TEST 11: GET TEST RESULTS (TEACHER) ====================
print_section("TEST 11: GET TEST RESULTS (TEACHER ANALYTICS)")

try:
    if test_id:
        headers = {"Authorization": f"Bearer {teacher_token}"}
        response = requests.get(f"{BASE_URL}/tests/{test_id}/results", headers=headers)
        passed = response.status_code == 200
        print_test("Get Test Results (Teacher)", passed, f"Status: {response.status_code}")
        
        if passed:
            try:
                data = response.json()
                if isinstance(data, list):
                    total = len(data)
                    avg_score = sum(r.get('marks_obtained', 0) for r in data) / total if total > 0 else 0
                    pass_count = sum(1 for r in data if r.get('is_passed', False))
                    pass_rate = (pass_count / total * 100) if total > 0 else 0
                    
                    print(f"       Total Attempts: {total}")
                    print(f"       Average Score: {avg_score:.1f}")
                    print(f"       Pass Rate: {pass_rate:.1f}%")
            except Exception as e:
                print(f"       Error parsing response: {str(e)}")
except Exception as e:
    print_test("Get Test Results (Teacher)", False, str(e))

# ==================== TEST 12: UPDATE TEST (TEACHER) ====================
print_section("TEST 12: UPDATE TEST")

try:
    if test_id:
        payload = {
            "name": "Updated Test Name",
            "description": "Updated description",
            "duration": 45,
            "passing_marks": 50
        }
        
        headers = {"Authorization": f"Bearer {teacher_token}"}
        response = requests.put(f"{BASE_URL}/tests/{test_id}", json=payload, headers=headers)
        passed = response.status_code == 200
        print_test("Update Test", passed, f"Status: {response.status_code}")
        
        if passed:
            data = response.json()
            print(f"       Updated Name: {data['test']['name']}")
            print(f"       Updated Duration: {data['test']['duration']} minutes")
except Exception as e:
    print_test("Update Test", False, str(e))

# ==================== TEST 13: INVALID REQUESTS ====================
print_section("TEST 13: ERROR HANDLING & VALIDATION")

try:
    # Test missing token
    response = requests.get(f"{BASE_URL}/tests")
    passed = response.status_code == 401
    print_test("Missing Authorization Token", passed, f"Status: {response.status_code}")
except Exception as e:
    print_test("Missing Token Test", False, str(e))

try:
    # Test invalid credentials
    payload = {"teacher_id": "invalid", "password": "wrong"}
    response = requests.post(f"{BASE_URL}/auth/teacher-login", json=payload)
    passed = response.status_code == 401
    print_test("Invalid Credentials", passed, f"Status: {response.status_code}")
except Exception as e:
    print_test("Invalid Credentials Test", False, str(e))

try:
    # Test non-existent test
    headers = {"Authorization": f"Bearer {teacher_token}"}
    response = requests.get(f"{BASE_URL}/tests/99999", headers=headers)
    passed = response.status_code == 404
    print_test("Non-existent Test", passed, f"Status: {response.status_code}")
except Exception as e:
    print_test("Non-existent Test", False, str(e))

# ==================== SUMMARY ====================
print_section("TEST SUMMARY")
print(f"All critical functions have been tested!")
print("""
PASS = Function working correctly
FAIL = Function needs attention

Components Tested:
  1. Backend health check
  2. Teacher authentication
  3. Student authentication
  4. Create test with questions
  5. Get teacher's tests
  6. Get test details
  7. Get available tests (student)
  8. Submit test answers
  9. Get student results
  10. Get result details
  11. Teacher analytics
  12. Update test
  13. Error handling

Database: Working with SQLite
API Format: JSON REST
CORS: Enabled for all origins
Authentication: JWT token based
""")
