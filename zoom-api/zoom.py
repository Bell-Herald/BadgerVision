import requests

url = "https://api.zoom.us/v2/videosdk/sessions"
jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IjBCdHpyTWtOUXI2LTlyLTc1VDhfUkEiLCJleHAiOjE3MjgxNTEyODMsImlhdCI6MTcyNzU0NjQ4M30.h7ONcY7jZSvaTtw5gYPF5L2qnWe4XnIwAVa8F1xQO8A"

headers = {
    "authorization": "Bearer " + jwt,
    "content-type": "application/json",
    # "content-length": "28",
    "host": "api.zoom.us",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "connection": "close",
}

def create_session():
    payload = {
        "session_name": "test"
    }
    response = requests.post(url, headers=headers, data=payload)
    print(response.status_code)
    # print(response.json())

def list_sessions():
    response = requests.get(url, headers=headers)
    print(response.status_code)
    print(response.json())

if __name__ == "__main__":
    create_session()
    # list_sessions()