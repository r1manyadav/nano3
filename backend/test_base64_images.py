#!/usr/bin/env python
"""
Improved image upload - works with both JSON and FormData
The key insight: we'll support base64 encoded images in JSON, but also support file uploads
"""

import requests
import json
import base64
from io import BytesIO
from PIL import Image

BASE_URL = 'http://localhost:5000/api'

def create_test_image():
    """Create a simple test image and return as base64"""
    img = Image.new('RGB', (200, 150), color='blue')
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    image_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')
    return f'data:image/png;base64,{image_base64}'

def test_with_base64():
    print("=" * 80)
    print("IMAGE UPLOAD TEST - Using Base64 Encoding")
    print("=" * 80)
    
    # Step 1: Login as teacher
    print("\n1. Teacher Login...")
    login_resp = requests.post(f'{BASE_URL}/auth/teacher-login', json={
        'teacher_id': 'nano123',
        'password': 'nano123'
    })
    
    if login_resp.status_code != 200:
        print(f"❌ Login failed: {login_resp.status_code}")
        return
    
    token = login_resp.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    print(f"✅ Login successful")
    
    # Step 2: Create test with base64 image
    print("\n2. Creating test with base64 encoded image...")
    
    image_base64 = create_test_image()
    
    test_data = {
        'name': 'Base64 Image Test',
        'description': 'Test for base64 image uploads',
        'duration': 30,
        'passing_marks': 50,
        'questions': [{
            'text': 'What color is this image?',
            'image': image_base64,  # Include image in question
            'optionA': 'Blue',
            'optionB': 'Red',
            'optionC': 'Green',
            'optionD': 'Yellow',
            'correct': 'A'
        }]
    }
    
    resp = requests.post(
        f'{BASE_URL}/tests',
        json=test_data,
        headers=headers
    )
    
    print(f"Status: {resp.status_code}")
    if resp.status_code == 201:
        print("✅ Test created successfully with base64 image!")
        test_id = resp.json()['test']['id']
        
        # Verify
        print("\n3. Verifying test and image...")
        get_resp = requests.get(f'{BASE_URL}/tests/{test_id}', headers=headers)
        if get_resp.status_code == 200:
            test = get_resp.json()
            if test['questions'] and test['questions'][0].get('image'):
                image_data = test['questions'][0]['image']
                print(f"✅ Image data stored ({len(image_data)} chars)")
                print("   Can be displayed directly in HTML img tag")
        
        return True
    else:
        print(f"❌ Failed: {resp.text[:250]}")
        return False

if __name__ == '__main__':
    import time
    time.sleep(1)
    test_with_base64()
