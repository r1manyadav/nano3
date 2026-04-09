import pytest
import json
import os
from datetime import datetime


@pytest.fixture
def teacher_token(client):
    """Get a valid teacher JWT token."""
    response = client.post('/api/auth/teacher-login', 
        json={'teacher_id': 'nano123', 'password': 'nano123'},
        content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    return data['access_token']


@pytest.fixture
def student_token(client):
    """Get a valid student JWT token."""
    response = client.post('/api/auth/student-login',
        json={'email': 'test.student@example.com', 'password': 'password123'},
        content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    return data['access_token']


# ==================== Authentication Tests ====================

class TestAuthentication:
    """Test authentication endpoints."""
    
    def test_teacher_login_success(self, client):
        """Test successful teacher login with correct credentials."""
        response = client.post('/api/auth/teacher-login',
            json={'teacher_id': 'nano123', 'password': 'nano123'},
            content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'access_token' in data
        assert data['message'] == 'Login successful'
        assert data['user']['teacher_id'] == 'nano123'
    
    def test_teacher_login_invalid_credentials(self, client):
        """Test teacher login with invalid credentials."""
        response = client.post('/api/auth/teacher-login',
            json={'teacher_id': 'nano123', 'password': 'wrongpassword'},
            content_type='application/json')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'Invalid credentials' in data['message']
    
    def test_teacher_login_missing_credentials(self, client):
        """Test teacher login with missing credentials."""
        response = client.post('/api/auth/teacher-login',
            json={'teacher_id': 'nano123'},
            content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Missing credentials' in data['message']
    
    def test_student_login_new_account(self, client):
        """Test student login creates new account on first login."""
        response = client.post('/api/auth/student-login',
            json={'email': 'newstudent@example.com', 'password': 'password123'},
            content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'access_token' in data
        assert 'Account created and logged in' in data['message']
        assert data['user']['email'] == 'newstudent@example.com'
    
    def test_student_login_existing_account(self, client):
        """Test student login with existing account."""
        # First login (creates account)
        client.post('/api/auth/student-login',
            json={'email': 'student@example.com', 'password': 'password123'},
            content_type='application/json')
        
        # Second login
        response = client.post('/api/auth/student-login',
            json={'email': 'student@example.com', 'password': 'password123'},
            content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Login successful'


# ==================== Test Management Tests ====================

class TestManagement:
    """Test test creation, retrieval, update, and deletion."""
    
    def test_create_test_success(self, client, teacher_token):
        """Test successful test creation with questions."""
        test_data = {
            'name': 'Sample Test',
            'description': 'A sample test for testing',
            'duration': 30,
            'passing_marks': 40,
            'questions': [
                {
                    'text': 'What is 2+2?',
                    'optionA': '3',
                    'optionB': '4',
                    'optionC': '5',
                    'optionD': '6',
                    'correct': 'B'
                },
                {
                    'text': 'What is the capital of France?',
                    'optionA': 'London',
                    'optionB': 'Berlin',
                    'optionC': 'Paris',
                    'optionD': 'Madrid',
                    'correct': 'C'
                }
            ]
        }
        
        response = client.post('/api/tests',
            json=test_data,
            headers={'Authorization': f'Bearer {teacher_token}'},
            content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'Test created successfully'
        assert data['test']['name'] == 'Sample Test'
        assert data['test']['question_count'] == 2
    
    def test_create_test_missing_name(self, client, teacher_token):
        """Test test creation fails without name."""
        test_data = {
            'description': 'No name test',
            'questions': [
                {
                    'text': 'Question?',
                    'optionA': 'A',
                    'optionB': 'B',
                    'optionC': 'C',
                    'optionD': 'D',
                    'correct': 'A'
                }
            ]
        }
        
        response = client.post('/api/tests',
            json=test_data,
            headers={'Authorization': f'Bearer {teacher_token}'},
            content_type='application/json')
        
        assert response.status_code == 422
        data = json.loads(response.data)
        assert 'Test name is required' in data['message']
    
    def test_create_test_no_questions(self, client, teacher_token):
        """Test test creation fails without questions."""
        test_data = {
            'name': 'Empty Test',
            'questions': []
        }
        
        response = client.post('/api/tests',
            json=test_data,
            headers={'Authorization': f'Bearer {teacher_token}'},
            content_type='application/json')
        
        assert response.status_code == 422
        data = json.loads(response.data)
        assert 'At least one question is required' in data['message']
    
    def test_create_test_missing_options(self, client, teacher_token):
        """Test test creation fails with incomplete options."""
        test_data = {
            'name': 'Test with missing options',
            'questions': [
                {
                    'text': 'Incomplete question?',
                    'optionA': 'A',
                    'optionB': 'B',
                    'correct': 'A'
                    # Missing optionC and optionD
                }
            ]
        }
        
        response = client.post('/api/tests',
            json=test_data,
            headers={'Authorization': f'Bearer {teacher_token}'},
            content_type='application/json')
        
        assert response.status_code == 422
        data = json.loads(response.data)
        assert 'Missing options' in data['message']
    
    def test_get_tests_teacher(self, client, teacher_token):
        """Test teacher can retrieve their own tests."""
        # Create a test first
        test_data = {
            'name': 'Teacher Test',
            'questions': [
                {
                    'text': 'Q1',
                    'optionA': 'A',
                    'optionB': 'B',
                    'optionC': 'C',
                    'optionD': 'D',
                    'correct': 'A'
                }
            ]
        }
        
        client.post('/api/tests',
            json=test_data,
            headers={'Authorization': f'Bearer {teacher_token}'},
            content_type='application/json')
        
        # Retrieve tests
        response = client.get('/api/tests',
            headers={'Authorization': f'Bearer {teacher_token}'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['name'] == 'Teacher Test'
    
    def test_get_test_by_id(self, client, teacher_token):
        """Test retrieving a specific test with questions."""
        # Create a test
        test_data = {
            'name': 'Specific Test',
            'questions': [
                {
                    'text': 'Q1?',
                    'optionA': 'A',
                    'optionB': 'B',
                    'optionC': 'C',
                    'optionD': 'D',
                    'correct': 'B'
                }
            ]
        }
        
        create_response = client.post('/api/tests',
            json=test_data,
            headers={'Authorization': f'Bearer {teacher_token}'},
            content_type='application/json')
        test_id = json.loads(create_response.data)['test']['id']
        
        # Retrieve specific test
        response = client.get(f'/api/tests/{test_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Specific Test'
        assert 'questions' in data
        assert len(data['questions']) == 1
    
    def test_get_nonexistent_test(self, client):
        """Test retrieving non-existent test returns 404."""
        response = client.get('/api/tests/9999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'Test not found' in data['message']
    
    def test_update_test(self, client, teacher_token):
        """Test updating a test."""
        # Create a test
        test_data = {
            'name': 'Original Name',
            'duration': 30,
            'questions': [
                {
                    'text': 'Q1',
                    'optionA': 'A',
                    'optionB': 'B',
                    'optionC': 'C',
                    'optionD': 'D',
                    'correct': 'A'
                }
            ]
        }
        
        create_response = client.post('/api/tests',
            json=test_data,
            headers={'Authorization': f'Bearer {teacher_token}'},
            content_type='application/json')
        test_id = json.loads(create_response.data)['test']['id']
        
        # Update test
        update_data = {
            'name': 'Updated Name',
            'duration': 60,
            'passing_marks': 50
        }
        
        response = client.put(f'/api/tests/{test_id}',
            json=update_data,
            headers={'Authorization': f'Bearer {teacher_token}'},
            content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['test']['name'] == 'Updated Name'
        assert data['test']['duration'] == 60
    
    def test_delete_test(self, client, teacher_token):
        """Test deleting a test."""
        # Create a test
        test_data = {
            'name': 'Test to Delete',
            'questions': [
                {
                    'text': 'Q1',
                    'optionA': 'A',
                    'optionB': 'B',
                    'optionC': 'C',
                    'optionD': 'D',
                    'correct': 'A'
                }
            ]
        }
        
        create_response = client.post('/api/tests',
            json=test_data,
            headers={'Authorization': f'Bearer {teacher_token}'},
            content_type='application/json')
        test_id = json.loads(create_response.data)['test']['id']
        
        # Delete test
        response = client.delete(f'/api/tests/{test_id}',
            headers={'Authorization': f'Bearer {teacher_token}'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'deleted successfully' in data['message']
        
        # Verify test is deleted
        verify_response = client.get(f'/api/tests/{test_id}')
        assert verify_response.status_code == 404


# ==================== Test Submission & Scoring Tests ====================

class TestSubmission:
    """Test test submission and scoring logic."""
    
    def test_submit_test_all_correct(self, client, teacher_token, student_token):
        """Test submitting test with all correct answers."""
        # Create test
        test_data = {
            'name': 'Scoring Test',
            'questions': [
                {
                    'text': 'Q1',
                    'optionA': 'A',
                    'optionB': 'B',
                    'optionC': 'C',
                    'optionD': 'D',
                    'correct': 'A'
                },
                {
                    'text': 'Q2',
                    'optionA': 'A',
                    'optionB': 'B',
                    'optionC': 'C',
                    'optionD': 'D',
                    'correct': 'C'
                }
            ]
        }
        
        create_response = client.post('/api/tests',
            json=test_data,
            headers={'Authorization': f'Bearer {teacher_token}'},
            content_type='application/json')
        test_id = json.loads(create_response.data)['test']['id']
        
        # Get test to retrieve question IDs
        test_response = client.get(f'/api/tests/{test_id}')
        questions = json.loads(test_response.data)['questions']
        q1_id = questions[0]['id']
        q2_id = questions[1]['id']
        
        # Submit test with correct answers
        submission_data = {
            'test_id': test_id,
            'answers': {
                str(q1_id): 'A',
                str(q2_id): 'C'
            },
            'question_status': {
                str(q1_id): 'answered',
                str(q2_id): 'answered'
            }
        }
        
        response = client.post('/api/results/submit',
            json=submission_data,
            headers={'Authorization': f'Bearer {student_token}'},
            content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['result']['correct_count'] == 2
        assert data['result']['wrong_count'] == 0
        assert data['result']['marks_obtained'] == 8  # 2 correct * 4 points
    
    def test_submit_test_mixed_answers(self, client, teacher_token, student_token):
        """Test submitting test with mix of correct, wrong, and unanswered."""
        # Create test
        test_data = {
            'name': 'Mixed Answers Test',
            'questions': [
                {'text': 'Q1', 'optionA': 'A', 'optionB': 'B', 'optionC': 'C', 'optionD': 'D', 'correct': 'A'},
                {'text': 'Q2', 'optionA': 'A', 'optionB': 'B', 'optionC': 'C', 'optionD': 'D', 'correct': 'B'},
                {'text': 'Q3', 'optionA': 'A', 'optionB': 'B', 'optionC': 'C', 'optionD': 'D', 'correct': 'C'}
            ]
        }
        
        create_response = client.post('/api/tests',
            json=test_data,
            headers={'Authorization': f'Bearer {teacher_token}'},
            content_type='application/json')
        test_id = json.loads(create_response.data)['test']['id']
        
        # Get questions
        test_response = client.get(f'/api/tests/{test_id}')
        questions = json.loads(test_response.data)['questions']
        q_ids = [str(q['id']) for q in questions]
        
        # Submit: Q1 correct, Q2 wrong, Q3 skipped
        submission_data = {
            'test_id': test_id,
            'answers': {
                q_ids[0]: 'A',  # Correct
                q_ids[1]: 'C',  # Wrong (should be B)
                q_ids[2]: None  # Skipped
            },
            'question_status': {
                q_ids[0]: 'answered',
                q_ids[1]: 'answered',
                q_ids[2]: 'skipped'
            }
        }
        
        response = client.post('/api/results/submit',
            json=submission_data,
            headers={'Authorization': f'Bearer {student_token}'},
            content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['result']['correct_count'] == 1
        assert data['result']['wrong_count'] == 1
        assert data['result']['unanswered_count'] == 1
        # Score: 1*4 (correct) - 1*1 (wrong) = 3
        assert data['result']['marks_obtained'] == 3
    
    def test_submit_test_no_questions(self, client, teacher_token, student_token):
        """Test submitting non-existent test."""
        submission_data = {
            'test_id': 9999,
            'answers': {}
        }
        
        response = client.post('/api/results/submit',
            json=submission_data,
            headers={'Authorization': f'Bearer {student_token}'},
            content_type='application/json')
        
        assert response.status_code == 404


# ==================== Authorization Tests ====================

class TestAuthorization:
    """Test authorization and permission checks."""
    
    def test_student_cannot_create_test(self, client, student_token):
        """Test that students cannot create tests."""
        test_data = {
            'name': 'Student Created Test',
            'questions': [
                {
                    'text': 'Q1',
                    'optionA': 'A',
                    'optionB': 'B',
                    'optionC': 'C',
                    'optionD': 'D',
                    'correct': 'A'
                }
            ]
        }
        
        response = client.post('/api/tests',
            json=test_data,
            headers={'Authorization': f'Bearer {student_token}'},
            content_type='application/json')
        
        assert response.status_code == 403
        data = json.loads(response.data)
        assert 'Only teachers can create tests' in data['message']
    
    def test_teacher_cannot_submit_test(self, client, teacher_token):
        """Test that teachers cannot submit tests."""
        submission_data = {
            'test_id': 1,
            'answers': {}
        }
        
        response = client.post('/api/results/submit',
            json=submission_data,
            headers={'Authorization': f'Bearer {teacher_token}'},
            content_type='application/json')
        
        assert response.status_code == 403
        data = json.loads(response.data)
        assert 'Only students can submit tests' in data['message']
    
    def test_unauthenticated_cannot_create_test(self, client):
        """Test that unauthenticated users cannot create tests."""
        test_data = {
            'name': 'Test',
            'questions': [
                {
                    'text': 'Q1',
                    'optionA': 'A',
                    'optionB': 'B',
                    'optionC': 'C',
                    'optionD': 'D',
                    'correct': 'A'
                }
            ]
        }
        
        response = client.post('/api/tests',
            json=test_data,
            content_type='application/json')
        
        assert response.status_code == 401


# ==================== Run Tests ====================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
