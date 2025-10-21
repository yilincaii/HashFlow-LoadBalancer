import requests

for i in range(100):
    response = requests.get("http://localhost:5000/api")
    print(response.text)
    