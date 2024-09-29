import requests
import json
import random
import string

ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IjBCdHpyTWtOUXI2LTlyLTc1VDhfUkEiLCJleHAiOjE3MjgxNTM0ODYsImlhdCI6MTcyNzU0ODY4Nn0.KzPU-T9Rj4ilHlJ65fz6AWbhkqKtIdB3D5ZVtTUDVW4'

def create_session():
    url = "https://api.zoom.us/v2/videosdk/sessions"
    
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    # Generate a random session name
    session_name = ''.join(random.choices(string.ascii_letters, k=7))
    
    # Data to be sent in the POST request
    data = {
        "session_name": f'{session_name}',
        "settings": {
            "auto_recording": "none"
        }
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:  # Updated to match Zoom SDK session creation
        session_info = response.json()
        print("Session created successfully!")
        print("Session ID:", session_info.get("session_id"))
        print("Session Name:", session_info.get("session_name"))
        print("Created At:", session_info.get("created_at"))
        session_id = session_info.get("session_id")

        # Write session info to a file for later use
        with open("session_info.txt", "w") as file:
            file.write(session_id + "\n")
            file.write(session_name)
        
        return session_id, session_name  # Return session details if needed
    else:
        print("Failed to create session")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        return None

def update_livestream(session_id, stream_url, stream_key, page_url):
    url = f"https://api.zoom.us/v2/videosdk/sessions/{session_id}/livestream"
    
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    # Data to be sent in the PATCH request
    data = {
        "stream_url": stream_url,
        "stream_key": stream_key,
        "page_url": page_url
    }
    
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 204:
        print("Live stream updated successfully!")
    else:
        print("Failed to update live stream")
        print("Status Code:", response.status_code)
        print("Response:", response.text)

def update_livestream_status(session_id, stream_url, stream_key, page_url):
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
        "stream_url": stream_url,
        "stream_key": stream_key,
        "page_url": page_url
    }

    response = requests.patch(url, headers=headers, data=json.dumps(data))

    if response.status_code == 204:
        print("Live stream updated successfully!")
    else:
        print("Failed to update live stream")
        print("Status Code:", response.status_code)
        print("Response:", response.text)