from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
from datetime import datetime
import os
import json

from models import db, Teacher, Student, Test, Question, TestResult

load_dotenv()

app = Flask(__name__)

# Configuration
# Use instance folder for database (Flask standard location for instance data)
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
INSTANCE_DIR = os.path.join(BACKEND_DIR, 'instance')
os.makedirs(INSTANCE_DIR, exist_ok=True)  # Ensure instance folder exists
DATABASE_PATH = os.path.join(INSTANCE_DIR, 'nano_test_platform.db')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', f'sqlite:///{DATABASE_PATH}')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)
CORS(app, 
     origins="*",
     allow_headers="*",
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
     supports_credentials=True)

with app.app_context():
    db.create_all()

# ==================== Authentication Routes ====================

@app.route('/api/auth/teacher-login', methods=['POST'])
def teacher_login():
    data = request.get_json()
    teacher_id = data.get('teacher_id')
    password = data.get('password')
    
    if not teacher_id or not password:
        return jsonify({'message': 'Missing credentials'}), 400
    
    # Check hardcoded credentials
    if teacher_id == 'nano123' and password == 'nano123':
        # Find or create teacher in database
        teacher = Teacher.query.filter_by(teacher_id=teacher_id).first()
        if not teacher:
            teacher = Teacher(teacher_id=teacher_id, name='Teacher')
            teacher.set_password(password)
            db.session.add(teacher)
            db.session.commit()
        
        # Create token with string identity and additional claims
        additional_claims = {'id': teacher.id, 'type': 'teacher'}
        access_token = create_access_token(identity=f"teacher_{teacher.id}", additional_claims=additional_claims)
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': teacher.to_dict()
        }), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/api/auth/student-login', methods=['POST'])
def student_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'message': 'Missing credentials'}), 400
    
    student = Student.query.filter_by(email=email).first()
    
    if not student or not student.check_password(password):
        # For demo: create student if doesn't exist
        if not student:
            student = Student(email=email, name=email)
            student.set_password(password)
            db.session.add(student)
            db.session.commit()
            
            # Create token with string identity and additional claims
            additional_claims = {'id': student.id, 'type': 'student'}
            access_token = create_access_token(identity=f"student_{student.id}", additional_claims=additional_claims)
            return jsonify({
                'message': 'Account created and logged in',
                'access_token': access_token,
                'user': student.to_dict()
            }), 200
        
        return jsonify({'message': 'Invalid credentials'}), 401
    
    # Create token with string identity and additional claims
    additional_claims = {'id': student.id, 'type': 'student'}
    access_token = create_access_token(identity=f"student_{student.id}", additional_claims=additional_claims)
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': student.to_dict()
    }), 200


# ==================== Test Routes (Teacher) ====================

@app.route('/api/tests', methods=['POST'])
@jwt_required()
def create_test():
    claims = get_jwt()
    if claims.get('type') != 'teacher':
        return jsonify({'message': 'Only teachers can create tests'}), 403
    
    data = request.get_json()
    print(f"[DEBUG] Received test data: {data}")
    
    # Validate required fields
    if not data.get('name'):
        return jsonify({'message': 'Test name is required'}), 422
    if not data.get('questions') or len(data.get('questions', [])) == 0:
        return jsonify({'message': 'At least one question is required'}), 422
    
    try:
        # Create test
        test = Test(
            teacher_id=claims['id'],
            name=data.get('name'),
            description=data.get('description', ''),
            duration=int(data.get('duration', 30)),
            passing_marks=int(data.get('passing_marks', 40))
        )
        db.session.add(test)
        db.session.flush()
        
        # Add questions with base64-encoded images
        questions_data = data.get('questions', [])
        for idx, q_data in enumerate(questions_data):
            # Validate question fields
            print(f"[DEBUG] Processing question {idx + 1}: {q_data.keys()}")
            
            if not q_data.get('text'):
                return jsonify({'message': f'Question {idx + 1}: Question text is required'}), 422
            if not q_data.get('optionA') or not q_data.get('optionB') or not q_data.get('optionC') or not q_data.get('optionD'):
                missing = []
                if not q_data.get('optionA'): missing.append('A')
                if not q_data.get('optionB'): missing.append('B')
                if not q_data.get('optionC'): missing.append('C')
                if not q_data.get('optionD'): missing.append('D')
                return jsonify({'message': f'Question {idx + 1}: Missing options: {", ".join(missing)}'}), 422
            if not q_data.get('correct'):
                return jsonify({'message': f'Question {idx + 1}: Correct answer is required'}), 422
            
            # Get base64-encoded image if provided
            image_data = q_data.get('image', None)
            if image_data:
                print(f"[DEBUG] Question {idx + 1} has image (size: {len(image_data)} chars)")
            
            question = Question(
                test_id=test.id,
                question_text=q_data.get('text'),
                option_a=q_data.get('optionA'),
                option_b=q_data.get('optionB'),
                option_c=q_data.get('optionC'),
                option_d=q_data.get('optionD'),
                correct_answer=q_data.get('correct'),
                order=idx + 1,
                image=image_data  # Store base64-encoded image
            )
            db.session.add(question)
        
        db.session.commit()
        print(f"[DEBUG] Test created successfully: {test.id}")
        
        return jsonify({
            'message': 'Test created successfully',
            'test': test.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] Exception creating test: {str(e)}")
        return jsonify({'message': f'Error creating test: {str(e)}'}), 500


@app.route('/api/tests', methods=['GET'])
@jwt_required()
def get_tests():
    claims = get_jwt()
    
    if claims.get('type') == 'teacher':
        tests = Test.query.filter_by(teacher_id=claims['id']).all()
    else:
        tests = Test.query.filter_by(is_active=True).all()
    
    return jsonify([test.to_dict() for test in tests]), 200


@app.route('/api/tests/<int:test_id>', methods=['GET'])
def get_test(test_id):
    test = Test.query.get(test_id)
    
    if not test:
        return jsonify({'message': 'Test not found'}), 404
    
    return jsonify(test.to_dict(include_questions=True)), 200


@app.route('/api/tests/<int:test_id>', methods=['PUT'])
@jwt_required()
def update_test(test_id):
    claims = get_jwt()
    test = Test.query.get(test_id)
    
    if not test:
        return jsonify({'message': 'Test not found'}), 404
    
    if test.teacher_id != claims['id']:
        return jsonify({'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    test.name = data.get('name', test.name)
    test.description = data.get('description', test.description)
    test.duration = data.get('duration', test.duration)
    test.passing_marks = data.get('passing_marks', test.passing_marks)
    test.is_active = data.get('is_active', test.is_active)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Test updated successfully',
        'test': test.to_dict()
    }), 200


@app.route('/api/tests/<int:test_id>', methods=['DELETE'])
@jwt_required()
def delete_test(test_id):
    claims = get_jwt()
    test = Test.query.get(test_id)
    
    if not test:
        return jsonify({'message': 'Test not found'}), 404
    
    if test.teacher_id != claims['id']:
        return jsonify({'message': 'Unauthorized'}), 403
    
    db.session.delete(test)
    db.session.commit()
    
    return jsonify({'message': 'Test deleted successfully'}), 200


# ==================== Test Results Routes ====================

@app.route('/api/results/submit', methods=['POST'])
@app.route('/api/submit-test', methods=['POST'])
@jwt_required()
def submit_test():
    claims = get_jwt()
    if claims.get('type') != 'student':
        return jsonify({'message': 'Only students can submit tests'}), 403
    
    data = request.get_json()
    test_id = data.get('test_id')
    answers = data.get('answers', {})
    marked_for_review = data.get('marked_for_review', {})
    question_status = data.get('question_status', {})  # New: tracks answer/skip/marked_only
    
    test = Test.query.get(test_id)
    if not test:
        return jsonify({'message': 'Test not found'}), 404
    
    # Calculate score with new status-based system
    correct_count = 0
    wrong_count = 0
    unanswered_count = 0
    
    for question in test.questions:
        q_id = str(question.id)
        status = question_status.get(q_id)  # 'answered', 'skipped', 'marked_only', or None
        student_answer = answers.get(q_id)
        
        # Only score if status is 'answered' (not skipped or marked_only)
        if status == 'answered' and student_answer is not None:
            if student_answer == question.correct_answer:
                correct_count += 1
            else:
                wrong_count += 1
        else:
            # Skipped, marked_only, or unanswered = 0 points
            unanswered_count += 1
    
    # Calculate total marks: +4 for correct, -1 for wrong, ensure no negative marks
    total_marks = (correct_count * 4) - (wrong_count * 1)
    total_marks = max(0, total_marks)  # Ensure marks never go below 0
    max_marks = len(test.questions) * 4
    percentage = (total_marks / max_marks * 100) if max_marks > 0 else 0
    is_passed = percentage >= test.passing_marks
    
    # Create result record
    result = TestResult(
        student_id=claims['id'],
        test_id=test_id,
        answers=answers,
        marked_for_review=marked_for_review,
        marks_obtained=total_marks,
        max_marks=max_marks,
        percentage=round(percentage, 2),
        correct_count=correct_count,
        wrong_count=wrong_count,
        unanswered_count=unanswered_count,
        is_passed=is_passed
    )
    
    db.session.add(result)
    db.session.commit()
    
    return jsonify({
        'message': 'Test submitted successfully',
        'result': result.to_dict()
    }), 201


@app.route('/api/results', methods=['GET'])
@jwt_required()
def get_results():
    claims = get_jwt()
    
    # Students get their own results, teachers can't access this
    if claims.get('type') != 'student':
        return jsonify({'message': 'Only students can access their results'}), 403
    
    results = TestResult.query.filter_by(student_id=claims['id']).all()
    return jsonify([result.to_dict() for result in results]), 200


@app.route('/api/results/<int:result_id>', methods=['GET'])
@jwt_required()
def get_result(result_id):
    claims = get_jwt()
    result = TestResult.query.get(result_id)
    
    if not result:
        return jsonify({'message': 'Result not found'}), 404
    
    # Check authorization
    if claims.get('type') == 'student' and result.student_id != claims['id']:
        return jsonify({'message': 'Unauthorized'}), 403
    
    # Get test questions for detailed feedback
    test = Test.query.get(result.test_id)
    result_data = result.to_dict()
    result_data['test'] = test.to_dict()
    
    # Normalize marked_for_review - could be list or dict
    marked_ids = []
    if result.marked_for_review:
        if isinstance(result.marked_for_review, list):
            marked_ids = [str(qid) for qid in result.marked_for_review]
        elif isinstance(result.marked_for_review, dict):
            marked_ids = list(result.marked_for_review.keys())
    
    # Add question details with correct answers
    questions_with_answers = []
    for question in test.questions:
        q_dict = question.to_dict(include_answer=True)
        q_dict['student_answer'] = result.answers.get(str(question.id)) if result.answers else None
        q_dict['is_marked_for_review'] = str(question.id) in marked_ids
        questions_with_answers.append(q_dict)
    
    result_data['questions'] = questions_with_answers
    
    return jsonify(result_data), 200


@app.route('/api/students/<int:student_id>/results', methods=['GET'])
@jwt_required()
def get_student_results(student_id):
    claims = get_jwt()
    
    # Students can only view their own results
    if claims.get('type') == 'student' and claims['id'] != student_id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    results = TestResult.query.filter_by(student_id=student_id).all()
    return jsonify([result.to_dict() for result in results]), 200


@app.route('/api/tests/<int:test_id>/results', methods=['GET'])
@jwt_required()
def get_test_results(test_id):
    claims = get_jwt()
    test = Test.query.get(test_id)
    
    if not test:
        return jsonify({'message': 'Test not found'}), 404
    
    # Only teacher who created the test can view results
    if claims.get('type') != 'teacher' or test.teacher_id != claims['id']:
        return jsonify({'message': 'Unauthorized'}), 403
    
    results = TestResult.query.filter_by(test_id=test_id).all()
    results_data = []
    
    for result in results:
        r_data = result.to_dict()
        r_data['student_email'] = result.student.email
        results_data.append(r_data)
    
    return jsonify(results_data), 200


# ==================== Home Routes ====================

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'OK', 'message': 'Nano Test Platform Backend'}), 200


@app.route('/', methods=['GET'])
def home():
    """Serve the frontend index.html"""
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'frontend'), 'index.html')


@app.route('/<path:filename>', methods=['GET'])
def serve_static(filename):
    """Serve static files from frontend directory"""
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'frontend'), filename)


@app.route('/api/', methods=['GET'])
def api_info():
    """Show API endpoints information"""
    return jsonify({
        'message': 'Nano Institute - MCQ Test Platform Backend',
        'version': '1.0.0',
        'endpoints': {
            'auth': ['/api/auth/teacher-login', '/api/auth/student-login'],
            'tests': ['/api/tests', '/api/tests/<id>'],
            'results': ['/api/results/submit', '/api/results/<id>', '/api/students/<id>/results', '/api/tests/<id>/results']
        }
    }), 200


if __name__ == '__main__':
    # Production-ready startup
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
