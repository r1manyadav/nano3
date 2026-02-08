import requests
import json

BASE_URL = "http://localhost:5000/api"

print("=" * 60)
print("ADVANCED TESTING: TEST SUBMISSION & RESULTS")
print("=" * 60)

# Step 1: Student Login
print("\n[STEP 1] Student Login")
print("-" * 60)
student_login = requests.post(f"{BASE_URL}/auth/student-login", json={
    "email": "advtest@example.com",
    "password": "pass123"
})

if student_login.status_code == 200:
    student_token = student_login.json()['access_token']
    print(f"✓ Student logged in successfully")
else:
    print(f"✗ Student login failed: {student_login.text}")
    exit(1)

# Step 2: Get Available Tests
print("\n[STEP 2] Get Available Tests")
print("-" * 60)
get_tests = requests.get(
    f"{BASE_URL}/tests",
    headers={"Authorization": f"Bearer {student_token}"}
)

if get_tests.status_code == 200:
    tests = get_tests.json()
    if len(tests) > 0:
        test_id = tests[0]['id']
        test_name = tests[0]['name']
        print(f"✓ Found {len(tests)} test(s)")
        print(f"  Using Test: [{test_id}] {test_name}")
    else:
        print(f"✗ No tests available")
        exit(1)
else:
    print(f"✗ Failed to get tests: {get_tests.text}")
    exit(1)

# Step 3: Get Test Details
print("\n[STEP 3] Get Test Details")
print("-" * 60)
get_test = requests.get(
    f"{BASE_URL}/tests/{test_id}",
    headers={"Authorization": f"Bearer {student_token}"}
)

if get_test.status_code == 200:
    test_detail = get_test.json()
    questions = test_detail['questions']
    print(f"✓ Retrieved test details")
    print(f"  Total Questions: {len(questions)}")
    for i, q in enumerate(questions, 1):
        print(f"    {i}. {q['question_text'][:50]}...")

# Step 4: Submit Test (answer all questions)
print("\n[STEP 4] Submit Test")
print("-" * 60)
answers = {}
for idx, q in enumerate(questions):
    q_id = str(q['id'])
    # Answer: choose B for first, C for second (based on quiz design)
    if idx == 0:
        answers[q_id] = "B"  # Correct for first question (2+2=4)
    else:
        answers[q_id] = "C"  # Correct for second question (Paris)

submit_test = requests.post(
    f"{BASE_URL}/results/submit",
    json={
        "test_id": test_id,
        "answers": answers,
        "marked_for_review": {},
        "question_status": {str(q['id']): 'answered' for q in questions}
    },
    headers={"Authorization": f"Bearer {student_token}"}
)

if submit_test.status_code == 201:
    result = submit_test.json()['result']
    print(f"✓ Test submitted successfully")
    print(f"  Marks: {result['marks_obtained']}/{result['max_marks']}")
    print(f"  Percentage: {result['percentage']}%")
    print(f"  Status: {'PASSED' if result['is_passed'] else 'FAILED'}")
    print(f"  Correct: {result['correct_count']}, Wrong: {result['wrong_count']}, Unanswered: {result['unanswered_count']}")
    result_id = result['id']
else:
    print(f"✗ Test submission failed: {submit_test.text}")
    exit(1)

# Step 5: Get Student Results
print("\n[STEP 5] Get Student Results")
print("-" * 60)
get_results = requests.get(
    f"{BASE_URL}/results",
    headers={"Authorization": f"Bearer {student_token}"}
)

if get_results.status_code == 200:
    results = get_results.json()
    print(f"✓ Retrieved {len(results)} result(s)")
    if len(results) > 0:
        print(f"  Latest Result ID: {results[-1]['id']}")

# Step 6: Get Detailed Result
print("\n[STEP 6] Get Detailed Result")
print("-" * 60)
get_result_detail = requests.get(
    f"{BASE_URL}/results/{result_id}",
    headers={"Authorization": f"Bearer {student_token}"}
)

if get_result_detail.status_code == 200:
    result_detail = get_result_detail.json()
    print(f"✓ Retrieved detailed result")
    print(f"  Test: {result_detail['test']['name']}")
    print(f"  Student Answer vs Correct Answer:")
    for q in result_detail['questions']:
        student_ans = q.get('student_answer', 'Not answered')
        correct_ans = q.get('correct_answer', 'N/A')
        match = "✓" if student_ans == correct_ans else "✗"
        print(f"    {match} Q: {q['question_text'][:40]}... | Student: {student_ans} | Correct: {correct_ans}")

print("\n" + "=" * 60)
print("ADVANCED TESTING COMPLETED SUCCESSFULLY")
print("=" * 60)
