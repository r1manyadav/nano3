import requests
import json

BASE_URL = 'http://localhost:5000/api'

# Login
login = requests.post(f'{BASE_URL}/auth/student-login', json={'email': 'nano1', 'password': 'nano1'})
token = login.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

# Get results
results = requests.get(f'{BASE_URL}/results', headers=headers).json()
print('Results returned from /api/results:\n')
for r in results[:3]:
    print(f'ID: {r.get("id")} | Test: {r.get("test_name")} | Score: {r.get("marks_obtained")}/{r.get("max_marks")}')

print(f'\nFirst complete result:')
print(json.dumps(results[0], indent=2))
