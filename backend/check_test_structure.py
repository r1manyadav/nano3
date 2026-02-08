import requests
import json

BASE_URL = "http://localhost:5000/api"

login = requests.post(f'{BASE_URL}/auth/student-login', 
    json={'email': 'nano1', 'password': 'nano1'})
token = login.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

tests = requests.get(f'{BASE_URL}/tests', headers=headers).json()
test = requests.get(f'{BASE_URL}/tests/{tests[0]["id"]}', headers=headers).json()

print("Test structure:")
print(json.dumps(test['questions'][0], indent=2))
