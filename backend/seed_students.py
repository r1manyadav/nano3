"""
Script to seed 100 students in the database
Run this once to add all students
"""

from app import app, db
from models import Student

def seed_students():
    # Check if students already exist
    existing = Student.query.first()
    if existing:
        print("Students already exist in database. Skipping seed.")
        return
    
    print("Creating 100 students...")
    
    for roll_no in range(1, 101):
        student_id = f"nano{roll_no}"
        password = f"nano{roll_no}"
        
        student = Student(
            email=student_id,
            name=f"Student {roll_no}",
            roll_number=str(roll_no)
        )
        student.set_password(password)
        db.session.add(student)
        
        if roll_no % 10 == 0:
            print(f"  Created {roll_no} students...")
    
    db.session.commit()
    print("✓ All 100 students created successfully!")
    print("\nStudent Credentials:")
    print("Roll No 1:   ID: nano1,   Password: nano1")
    print("Roll No 2:   ID: nano2,   Password: nano2")
    print("Roll No 3:   ID: nano3,   Password: nano3")
    print("...")
    print("Roll No 100: ID: nano100, Password: nano100")

if __name__ == '__main__':
    with app.app_context():
        seed_students()
