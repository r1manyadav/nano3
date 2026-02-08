# Nano Institute - MCQ Test Platform Backend

A comprehensive Flask-based backend for managing MCQ tests, teacher dashboards, and student test attempts.

## Features

- **Teacher Authentication**: Secure login with hardcoded credentials (nano123/nano123)
- **Student Authentication**: Auto-account creation for new students
- **Test Management**: Create, read, update, delete tests with multiple choice questions
- **Test Taking**: Students can attempt tests with save functionality
- **Mark for Review**: Students can mark questions for review during test attempts
- **Results Tracking**: Comprehensive test result storage and analysis
- **Answer Tracking**: Store student answers with marked-for-review status
- **Score Calculation**: Automatic marking with +4 for correct, -1 for wrong

## Tech Stack

- **Framework**: Flask 2.3.0
- **Database**: SQLAlchemy with SQLite
- **Authentication**: JWT (JSON Web Tokens)
- **API Security**: CORS enabled

## Installation

1. Activate virtual environment:
```bash
# Windows
.venv\Scripts\Activate.ps1

# Linux/Mac
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Environment Configuration:
Update `.env` file with your secrets (optional for development):
```
SECRET_KEY=change_this_in_production
JWT_SECRET_KEY=change_this_in_production
DATABASE_URL=sqlite:///nano_test_platform.db
```

## Running the Server

```bash
cd backend
python app.py
```

The server will start at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/teacher-login` - Teacher login
- `POST /api/auth/student-login` - Student login/registration

### Tests (Teacher)
- `POST /api/tests` - Create new test (requires JWT)
- `GET /api/tests` - List all tests
- `GET /api/tests/<id>` - Get test details with questions
- `PUT /api/tests/<id>` - Update test (requires JWT)
- `DELETE /api/tests/<id>` - Delete test (requires JWT)

### Test Submission
- `POST /api/results/submit` - Submit test answers (requires JWT)
- `GET /api/results/<id>` - Get result details (requires JWT)

### Results
- `GET /api/students/<id>/results` - Get student's all results (requires JWT)
- `GET /api/tests/<id>/results` - Get test results (teacher only, requires JWT)

## Request/Response Examples

### Teacher Login
```json
POST /api/auth/teacher-login
{
  "teacher_id": "nano123",
  "password": "nano123"
}

Response:
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "teacher_id": "nano123",
    "name": "Teacher",
    "created_at": "2026-02-07T..."
  }
}
```

### Create Test
```json
POST /api/tests (with Bearer token)
{
  "name": "Biology Chapter 1",
  "description": "Test on basic biology concepts",
  "duration": 30,
  "passing_marks": 40,
  "questions": [
    {
      "text": "What is the basic unit of life?",
      "optionA": "Atom",
      "optionB": "Cell",
      "optionC": "Molecule",
      "optionD": "Organ",
      "correct": "B"
    }
  ]
}
```

### Submit Test
```json
POST /api/results/submit (with Bearer token)
{
  "test_id": 1,
  "answers": {
    "1": "B",
    "2": "A",
    "3": null
  },
  "marked_for_review": {
    "2": true
  }
}
```

## Database Models

### Teacher
- id, teacher_id (unique), password_hash, name, email, created_at
- Relationships: tests

### Student
- id, email (unique), password_hash, name, roll_number, created_at
- Relationships: results

### Test
- id, teacher_id (FK), name, description, duration, passing_marks, is_active, created_at
- Relationships: teacher, questions, results

### Question
- id, test_id (FK), question_text, option_a/b/c/d, correct_answer, order
- Relationships: test

### TestResult
- id, student_id (FK), test_id (FK), answers (JSON), marked_for_review (JSON)
- marks_obtained, max_marks, percentage, correct_count, wrong_count, is_passed, submitted_at
- Relationships: student, test

## Project Structure

```
backend/
├── app.py              # Main Flask application
├── models.py           # SQLAlchemy models
├── requirements.txt    # Dependencies
├── .env               # Environment variables
└── README.md          # This file
```

## Demo Credentials

**Teacher:**
- ID: `nano123`
- Password: `nano123`

**Student:**
- Auto-created on first login with email and password

## Development Notes

- JWT tokens are required for most endpoints except public routes
- Token is included in request header: `Authorization: Bearer <token>`
- All passwords are hashed using werkzeug security
- SQLite database auto-creates on first run
- CORS is enabled for frontend integration

## Future Enhancements

- [ ] Email verification for students
- [ ] Improve teacher registration process
- [ ] Add test scheduling
- [ ] Add analytics dashboard
- [ ] Export results to PDF
- [ ] Add question bank management
- [ ] Implement test proctoring
