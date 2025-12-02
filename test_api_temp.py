import requests
import json

url = 'http://localhost:5000/predict'
data = {
    "Gender": "Male",
    "Age": 25,
    "Salary": 150000,
    "Mental Condition": "Loneliness",
    "Allergies": "No"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
