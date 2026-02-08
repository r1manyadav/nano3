"""
Test the new scoring system with 4 button options:
- Save and Next: +4 for correct, -1 for wrong
- Skip: 0 marks (unattempted)
- Save and Mark for Review: +4 for correct, -1 for wrong (+ marked for review)
- Mark for Review only: 0 marks (unattempted, but marked for review)
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

print("\n" + "="*80)
print("NEW SCORING SYSTEM TEST")
print("="*80)

# Login as student
login = requests.post(f'{BASE_URL}/auth/student-login', 
    json={'email': 'nano1', 'password': 'nano1'})
token = login.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

# Get tests list
tests = requests.get(f'{BASE_URL}/tests', headers=headers).json()
test_id = tests[0]['id']

# Get test details with questions
test = requests.get(f'{BASE_URL}/tests/{test_id}', headers=headers).json()

print(f"\nTest Selected: {test['name']} (ID: {test_id})")
print(f"Questions: {len(test['questions'])}")
print(f"\nTest Details:")
print(f"  - Duration: {test['duration']} minutes")
print(f"  - Passing Marks: {test['passing_marks']}%")
print(f"  - Max Marks: {len(test['questions'])} × 4 = {len(test['questions']) * 4}")

# Prepare answers with new status system
print(f"\nNew Scoring System:")
print(f"  ✓ Save & Next    : +4 for correct, -1 for wrong (Attempted)")
print(f"  ⊘ Skip           : 0 marks (Unattempted)")
print(f"  ⭐ Save & Mark    : +4 for correct, -1 for wrong (Attempted + Review)")
print(f"  📋 Mark Only     : 0 marks (Unattempted + Review)")

# Create test submission with mixed statuses
answers = {}
question_status = {}
marked_for_review = {}

for i, q in enumerate(test['questions']):
    q_id = str(q['id'])
    if i == 0:
        # Answer correctly with Save & Next (Answer is B for question 1)
        answers[q_id] = 'B'  # Correct answer for "What is the capital of France?"
        question_status[q_id] = 'answered'
        marked_for_review[q_id] = False
    elif i == 1:
        # Skip
        answers[q_id] = None
        question_status[q_id] = 'skipped'
        marked_for_review[q_id] = False
    # else: don't attempt other questions

print(f"\nSubmitting Test...")
print(f"  Q1: Correct answer (Save & Next) → +4 points")
print(f"  Q2: Skipped → 0 points")

submit = requests.post(f'{BASE_URL}/results/submit', 
    headers=headers,
    json={
        'test_id': test_id,
        'answers': answers,
        'marked_for_review': marked_for_review,
        'question_status': question_status
    })

if submit.status_code == 201:
    result = submit.json()['result']
    print(f"\n✅ Test Submitted Successfully!")
    print(f"\nScoring Results:")
    print(f"  Correct Answers: {result['correct_count']}")
    print(f"  Wrong Answers: {result['wrong_count']}")
    print(f"  Unanswered: {result['unanswered_count']}")
    print(f"  Marks Obtained: {result['marks_obtained']}/{result['max_marks']}")
    print(f"  Percentage: {result['percentage']}%")
    print(f"  Status: {'PASSED ✓' if result['is_passed'] else 'FAILED ✗'}")
    print(f"\n✓ Expected: 4 marks (1 correct × +4)")
    print(f"✓ Actual: {result['marks_obtained']} marks")
    print(f"✓ Match: {'YES ✓' if result['marks_obtained'] == 4 else 'NO ✗'}")
else:
    print(f"\n❌ Error: {submit.status_code}")
    print(submit.json())

print("\n" + "="*80)
