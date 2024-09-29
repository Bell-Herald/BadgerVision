import requests
import jwt
import time
import json
import random
import string
import os
import pinata
import qrcode

ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IjBCdHpyTWtOUXI2LTlyLTc1VDhfUkEiLCJleHAiOjE3MjgxNTM0ODYsImlhdCI6MTcyNzU0ODY4Nn0.KzPU-T9Rj4ilHlJ65fz6AWbhkqKtIdB3D5ZVtTUDVW4'
STREAM_URL = "rtmp://162.243.166.134:1935/live"
PINATA_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiI1NjBhZTI4MC1lOWUyLTQ2YzctYjczZS1hOTc4MWY5ZjBkZjUiLCJlbWFpbCI6Im1heC5zLm1hZWRlckBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicGluX3BvbGljeSI6eyJyZWdpb25zIjpbeyJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MSwiaWQiOiJGUkExIn0seyJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MSwiaWQiOiJOWUMxIn1dLCJ2ZXJzaW9uIjoxfSwibWZhX2VuYWJsZWQiOmZhbHNlLCJzdGF0dXMiOiJBQ1RJVkUifSwiYXV0aGVudGljYXRpb25UeXBlIjoic2NvcGVkS2V5Iiwic2NvcGVkS2V5S2V5IjoiNTMyZjRkM2M5MDYzYTEzNjM2MWMiLCJzY29wZWRLZXlTZWNyZXQiOiJlMjM5YWYxMzNiMzNhMWU0ZjVmNDkyYjgzMGM3YjlkZmZlODQwNTk3MTM4OGFlZDY2YWYyZGM2N2E1MmMxNGMzIiwiZXhwIjoxNzU5MTEzNzAyfQ.D8hJHBL4KFHEqdg8_eO88v9RTn38X_WtC9970_STF84"
pinata_config = {
    "pinataJwt": PINATA_JWT,
}

# Create a new session via the Zoom Video SDK API,
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
        
        return session_id, session_name  # Return session details if needed
    else:
        print("Failed to create session")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        return None

# Create a JWT token for the session.
def create_jwt(session_name):
    ZOOM_SDK_KEY = 'YLfqZ1zkO5UCcVBhuqKcYzXUZunSp5ZbKg3q'
    ZOOM_SDK_SECRET = 'oYO7shH2XAk6X8hllehPI3VX74k45676Fl4t'
    iat = int(time.time())
    exp = iat + 60 * 5  # Signature expires in 5 minutes
    payload = {
        'app_key': ZOOM_SDK_KEY,
        'role_type': 1,
        'tpc': session_name,
        'version': 1,
        'iat': iat,
        'exp': exp,
    }
    token = jwt.encode(payload, ZOOM_SDK_SECRET, algorithm='HS256')
    return token

def upload_file_to_pinata(file_path):
    try:
        # Call the upload_file function we defined earlier
        response = pinata.upload_file(
            pinata_config,
            file_path
        )

        # Output the response from Pinata
        print("Upload successful! IPFS Hash:", response.get("IpfsHash"))
        print("Full Response:", response)
        return response

    except pinata.PinataError as e:
        print(f"Error during file upload: {e}")

    finally:
        # Clean up the test file after uploading
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Test file '{file_path}' has been deleted.")

def generate_qrcode():
    session_id, session_name = create_session()
    token = create_jwt(session_name)

    data = {
        "zoomSessionName": session_name,
        "zoomJwt": token,
        "websocketURL": "http://localhost:4000"
    }

    print("DATA: ", data)

    with open('data.json', 'w') as f:
        json.dump(data, f)
    
    response = upload_file_to_pinata("data.json")
    
    print(response)

    # Assuming 'id' is in the response
    session_id_from_response = response['data']['cid']

    print(session_id_from_response)
    # Generate QR code
    qr = qrcode.QRCode(version=3, box_size=20, border=10, error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(session_id_from_response)
    qr.make(fit=True)
    # Convert the QR code to an image in memory
    img = qr.make_image(fill_color="black", back_color="white")

    img.save("qr_code.png") 

# Update the livestream settings to the stream url, stream key, and page url. [deprecated]
# def update_livestream(session_id, stream_url, stream_key, page_url):
#     url = f"https://api.zoom.us/v2/videosdk/sessions/{session_id}/livestream"
    
#     headers = {
#         'Authorization': f'Bearer {ACCESS_TOKEN}',
#         'Content-Type': 'application/json'
#     }
    
#     # Data to be sent in the PATCH request
#     data = {
#         "stream_url": stream_url,
#         "stream_key": stream_key,
#         "page_url": page_url
#     }
    
#     response = requests.patch(url, headers=headers, data=json.dumps(data))
    
#     if response.status_code == 204:
#         print("Live stream updated successfully!")
#     else:
#         print("Failed to update live stream")
#         print("Status Code:", response.status_code)
#         print("Response:", response.text)

# Start the livestream. [deprecated]
# def update_livestream_status(session_id, stream_url, stream_key, page_url):
#     url = f"https://api.zoom.us/v2/videosdk/sessions/{session_id}/livestream"

#     headers = {
#         'Authorization': f'Bearer {ACCESS_TOKEN}',
#         'Content-Type': 'application/json'
#     }

#     data = {
#         "action": "start",
#         "stream_url": stream_url,
#         "stream_key": stream_key,
#         "page_url": page_url
#     }

#     response = requests.patch(url, headers=headers, data=json.dumps(data))

#     if response.status_code == 204:
#         print("Live stream updated successfully!")
#     else:
#         print("Failed to update live stream")
#         print("Status Code:", response.status_code)
#         print("Response:", response.text)

if __name__ == "__main__":
    generate_qrcode()
    # session_id, session_name = create_session()
    # session_jwt = create_jwt(session_name)
    # with open("session_info.txt", "w") as f:
    #     f.write(f"Session ID: {session_id}\n")
    #     f.write(f"Session Name: {session_name}\n")
    #     f.write(f"Session JWT: {session_jwt}\n")
    #     f.write(f"https://badgervision-5a9a2.firebaseapp.com/?sessionName={session_name}&jwt={session_jwt}\n")