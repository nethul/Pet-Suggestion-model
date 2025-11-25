import requests
import json

url = 'http://127.0.0.1:5000/predict'
headers = {'Content-Type': 'application/json'}
data = {
    "Gender": "male",
    "Age": 25,
    "Salary": 50000,
    "Mental Condition": "Anxiety",
    "Allergies": "yes"
}

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
