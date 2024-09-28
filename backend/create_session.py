import requests
import json
import random
import string

ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IjBCdHpyTWtOUXI2LTlyLTc1VDhfUkEiLCJleHAiOjE3MjgxNTM0ODYsImlhdCI6MTcyNzU0ODY4Nn0.KzPU-T9Rj4ilHlJ65fz6AWbhkqKtIdB3D5ZVtTUDVW4'

url = "https://api.zoom.us/v2/videosdk/sessions"

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

session_name = ''.join(random.choices(string.ascii_letters,k=7))

data = {
    "session_name": f'{session_name}',
    "settings": {
        "auto_recording": "none"
    }
}

response = requests.post(url, headers=headers, data=json.dumps(data))

# Check if the request was successful
if response.status_code == 200:
    session_info = response.json()
    print("Session created successfully!")
    print("Session ID:", session_info.get("session_id"))
    print("Session Name:", session_info.get("session_name"))
    print("Created At:", session_info.get("created_at"))
    session_id = session_info.get("session_id")

    with open("session_info.txt", "w") as file:
        file.write(session_id+"\n")
        file.write(session_name)
else:
    print("Failed to create session")
    print("Status Code:", response.status_code)
    print("Response:", response.text)


