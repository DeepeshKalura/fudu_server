import requests

url = "http://localhost:6969"

for i in range(20):
    response = requests.get(url)
    print(f"Request {i+1}: Status Code: {response.status_code}, Response: {response.text}")