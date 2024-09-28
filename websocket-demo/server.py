import socketio
import eventlet

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

#Catches disconnect
@sio.event
def disconnect(sid):
    print('EVENT: disconnect | ID:', sid)

#Catches other event that was not already caught
@sio.on('*')
def any_event(event, sid, data):
     print('EVENT::', event, "| ID:", sid, "| DATA:", data)
     pass

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
