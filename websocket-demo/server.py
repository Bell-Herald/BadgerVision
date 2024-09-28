import socketio
import eventlet
import json
import qrcode


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
    session_name = None
    print('EVENT: connect | ID:', sid)

#    qr = qrcode.QRCode(version=3, box_size=20, border=10, error_correction=qrcode.constants.ERROR_CORRECT_H)
#    qr.add_data(socketio_Url) #WHICH URL??
#    qr.make(fit=True)
#    img = qr.make_image(fill_color="black", back_color="white")
#    img.save("qr_code.png") #Send this image over

    #Send zoom information
    #TODO: Initializae zoom_Jwt
    sio.emit('zoom_initialization', {'data': session_name})

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

