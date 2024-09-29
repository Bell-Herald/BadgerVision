import socketio
import eventlet
import json
import time
import current_datetime
import jwt


###Initialize server
# create a Socket.IO server
sio = socketio.Server(cors_allowed_origins='*')  # Allow requests from any origin

# wrap with a WSGI application
app = socketio.WSGIApp(sio)


###Listen to events

#Catches custom event
@sio.on('chat-to-server-message')
def chat_to_server_event(sid, data):
    print("EVENT: chat_to_server_event | ID:", sid, "| DATA:", data)
    sio.emit('my event', {'data': 'foobar'})

#Catches connect
@sio.event
def connect(sid, environ, auth):
    print('EVENT: connect | ID:', sid)

    # Get unique session name through date and time
    current_datetime = datetime.now()
    session_name = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

    ZOOM_SDK_KEY = 'your_sdk_key'
    ZOOM_SDK_SECRET = 'your_sdk_secret'
    iat = int(time.time())
    exp = iat + 60 * 5  # Signature expires in 5 minutes
    payload = {
        'sdkKey': ZOOM_SDK_KEY,
        'mn': '',  # Session name/meeting number
        'role': 1,  # Host role
        'iat': iat,
        'exp': exp,
        'appKey': ZOOM_SDK_KEY,
        'tokenExp': exp
    }
    token = jwt.encode(payload, ZOOM_SDK_SECRET, algorithm='HS256')

    sio.emit('zoom_initialization', {'data': {'token': token, 'session_name': session_name}})

#Catches disconnect
@sio.event
def disconnect(sid):
    print('EVENT: disconnect | ID:', sid)

#Catches request for adding face to server for first phase
#Expects JSON data in the following format
#{
#  "name": "person name",
#  "url": "face url"
#}
@sio.on('face_added')
def face_added(sid, data):
    parsed_data = json.loads(data)
    name = None
    url = None

    if "name" in parsed_data:
        name = parsed_data["name"]
    else:
        raise Exception("Invalid syntax for face_added, name not included")
    if "url" in parsed_data:
        url = parsed_data["url"]
        raise Exception("Invalid syntax for face_added, url not included")
    
    print("TODO: save face to Pinata here")

#Catches other event that was not already caught
@sio.on('*')
def any_event(event, sid, data):
     print('EVENT::', event, "| ID:", sid, "| DATA:", data)
     pass

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)


"""
When a face is recognized:
    sio.emit('face_recognized', {'data': TONE})
"""