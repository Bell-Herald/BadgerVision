import requests
import json

lines = []
with open('session_info.txt', 'r') as file:
    lines = file.readlines()
session_id = lines[0].strip()
session_name = lines[1].strip()
print(session_id, session_name)

ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IjBCdHpyTWtOUXI2LTlyLTc1VDhfUkEiLCJleHAiOjE3MjgxNTM0ODYsImlhdCI6MTcyNzU0ODY4Nn0.KzPU-T9Rj4ilHlJ65fz6AWbhkqKtIdB3D5ZVtTUDVW4'

url = f"https://api.zoom.us/v2/videosdk/sessions/{session_id}/livestream"

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

data = {
    "action": "start",
    "settings": {
        "active_speaker_name": True,
        "display_name": "Jill Chill",
        "layout": "speaker_view",
        "close_caption": "burnt-in"
  },
    "stream_url": "rtmp://162.243.166.134:1935/live_321", 
    "stream_key": "live_321", 
    "page_url": "http://localhost:3000/"
}

response = requests.patch(url, headers=headers, data=json.dumps(data))

if response.status_code == 204:
    print("Live stream updated successfully!")
else:
    print("Failed to update live stream")
    print("Status Code:", response.status_code)
    print("Response:", response.text)
