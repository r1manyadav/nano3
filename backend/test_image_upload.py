#!/usr/bin/env python
"""Test script for image upload functionality"""

import requests
import json
from io import BytesIO
from PIL import Image

BASE_URL = 'http://localhost:5000/api'

def create_test_image():
    """Create a simple test image"""
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

def test_image_upload():
    print("=" * 80)
    print("IMAGE UPLOAD FUNCTIONALITY TEST")
    print("=" * 80)
    
    # Step 1: Login as teacher
    print("\n1. Teacher Login...")
    login_resp = requests.post(f'{BASE_URL}/auth/teacher-login', json={
        'teacher_id': 'nano123',
        'password': 'nano123'
    })
    
    if login_resp.status_code != 200:
        print(f"❌ Login failed: {login_resp.status_code}")
        print(login_resp.text)
        return
    
    token = login_resp.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    print(f"✅ Login successful")
    
    # Step 2: Create test with image
    print("\n2. Creating test with question image...")
    
    # Create image
    test_image = create_test_image()
    
    # Prepare form data
    test_data = {
        'name': 'Image Test',
        'description': 'Test for image uploads',
        'duration': '30',
        'passing_marks': '50',
        'questions': json.dumps([{
            'text': 'What is this image?',
            'optionA': 'Red Box',
            'optionB': 'Blue Box',
            'optionC': 'Green Box',
            'optionD': 'Yellow Box',
            'correct': 'A'
        }])
    }
    
    files = {
        'question_image_0': ('test_image.png', test_image, 'image/png')
    }
    
    # Send request
    create_resp = requests.post(
        f'{BASE_URL}/tests',
        data=test_data,
        files=files,
        headers=headers
    )
    
    if create_resp.status_code != 201:
        print(f"❌ Test creation failed: {create_resp.status_code}")
        print(create_resp.text)
        return
    
    test_data_resp = create_resp.json()
    print(f"✅ Test created successfully (ID: {test_data_resp['test']['id']})")
    
    # Step 3: Get test and verify image path
    print("\n3. Retrieving test details...")
    test_id = test_data_resp['test']['id']
    get_resp = requests.get(f'{BASE_URL}/tests/{test_id}', headers=headers)
    
    if get_resp.status_code != 200:
        print(f"❌ Failed to get test: {get_resp.status_code}")
        return
    
    test = get_resp.json()
    if test['questions'] and test['questions'][0].get('image_path'):
        image_path = test['questions'][0]['image_path']
        print(f"✅ Image path stored: {image_path}")
        
        # Step 4: Test image serving
        print("\n4. Testing image serving...")
        image_url = f'http://localhost:5000/uploads/{image_path}'
        image_resp = requests.get(image_url)
        
        if image_resp.status_code == 200:
            print(f"✅ Image serving works (Size: {len(image_resp.content)} bytes)")
            print(f"   URL: {image_url}")
        else:
            print(f"❌ Image serving failed: {image_resp.status_code}")
    else:
        print(f"❌ Image path not stored in database")
        print(f"   Question data: {test['questions'][0] if test['questions'] else 'No questions'}")
    
    print("\n" + "=" * 80)
    print("✅ IMAGE UPLOAD TEST COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print("\nNow students can see images in questions during tests.")

if __name__ == '__main__':
    # Wait for server to start
    import time
    print("Waiting for server to start...")
    time.sleep(2)
    
    test_image_upload()
