from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()

class Teacher(db.Model):
    __tablename__ = 'teachers'
    
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    tests = db.relationship('Test', back_populates='teacher', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }


class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255))
    roll_number = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    results = db.relationship('TestResult', back_populates='student', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'roll_number': self.roll_number,
            'created_at': self.created_at.isoformat()
        }


class Test(db.Model):
    __tablename__ = 'tests'
    
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    duration = db.Column(db.Integer)  # in minutes
    passing_marks = db.Column(db.Integer)  # percentage
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    teacher = db.relationship('Teacher', back_populates='tests')
    questions = db.relationship('Question', back_populates='test', cascade='all, delete-orphan')
    results = db.relationship('TestResult', back_populates='test', cascade='all, delete-orphan')
    
    def to_dict(self, include_questions=False):
        data = {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'name': self.name,
            'description': self.description,
            'duration': self.duration,
            'passing_marks': self.passing_marks,
            'is_active': self.is_active,
            'question_count': len(self.questions),
            'created_at': self.created_at.isoformat()
        }
        if include_questions:
            data['questions'] = [q.to_dict() for q in self.questions]
        return data


class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)  # A, B, C, or D
    order = db.Column(db.Integer)
    image = db.Column(db.Text, nullable=True)  # Base64 encoded image data
    
    # Relationships
    test = db.relationship('Test', back_populates='questions')
    
    def to_dict(self, include_answer=False):
        data = {
            'id': self.id,
            'question_text': self.question_text,
            'option_a': self.option_a,
            'option_b': self.option_b,
            'option_c': self.option_c,
            'option_d': self.option_d,
            'order': self.order,
            'image': self.image  # Base64 encoded image or None
        }
        if include_answer:
            data['correct_answer'] = self.correct_answer
        return data


class TestResult(db.Model):
    __tablename__ = 'test_results'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    answers = db.Column(db.JSON)  # JSON object with question_id: answer mapping
    marked_for_review = db.Column(db.JSON)  # JSON array of question IDs marked for review
    marks_obtained = db.Column(db.Float)
    max_marks = db.Column(db.Float)
    percentage = db.Column(db.Float)
    correct_count = db.Column(db.Integer)
    wrong_count = db.Column(db.Integer)
    unanswered_count = db.Column(db.Integer)
    is_passed = db.Column(db.Boolean)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    student = db.relationship('Student', back_populates='results')
    test = db.relationship('Test', back_populates='results')
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'test_id': self.test_id,
            'test_name': self.test.name,
            'test': self.test.to_dict(),
            'student_email': self.student.email,
            'marks_obtained': self.marks_obtained,
            'max_marks': self.max_marks,
            'percentage': self.percentage,
            'passing_marks': self.test.passing_marks,
            'score': self.marks_obtained,
            'correct_count': self.correct_count,
            'wrong_count': self.wrong_count,
            'unanswered_count': self.unanswered_count,
            'is_passed': self.is_passed,
            'submitted_at': self.submitted_at.isoformat()
        }
