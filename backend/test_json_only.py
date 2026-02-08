#!/usr/bin/env python
"""Simple test for image upload"""

import requests
import json
from io import BytesIO

BASE_URL = 'http://localhost:5000/api'

def test_json_only():
    print("Testing JSON request (no files)...")
    
    # Login
    login_resp = requests.post(f'{BASE_URL}/auth/teacher-login', json={
        'teacher_id': 'nano123',
        'password': 'nano123'
    })
    token = login_resp.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    
    # Create test with JSON only (no image)
    test_data = {
        'name': 'Test Without Image',
        'description': 'Testing JSON',
        'duration': 30,
        'passing_marks': 50,
        'questions': [{
            'text': 'Test question',
            'optionA': 'A',
            'optionB': 'B',
            'optionC': 'C',
            'optionD': 'D',
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
        print("✅ JSON request works!")
        return True
    else:
        print(f"❌ Failed: {resp.text[:200]}")
        return False

if __name__ == '__main__':
    import time
    time.sleep(1)
    test_json_only()
