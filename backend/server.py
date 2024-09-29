
import socketio
import eventlet
import json
import time
import session_backend
import cv2
from deepface import DeepFace
import face_recognition
from PIL import Image as im
import time
import numpy as np

port = "3000"
ip_address = "162.243.166.134"

sio = socketio.SimpleClient()

###Initialize server
# create a Socket.IO server
#sio = socketio.Server(cors_allowed_origins='*')  # Allow requests from any origin

# wrap with a WSGI application
#app = socketio.WSGIApp(sio)

###Listen to events


#Catches custom eventpip install --upgrade setuptools
@sio.on('chat-to-server-message')
def chat_to_server_event(sid, data):
    print("EVENT: chat_to_server_event | ID:", sid, "| DATA:", data)
    sio.emit('my event', {'data': 'foobar'})

#Catches disconnect
@sio.event
def disconnect(sid):
    print('EVENT: disconnect | ID:', sid)

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

RTMP_URL = "rtmp://162.243.166.134:1935/live/test" #I think extra configs needed in nginx.conf

mapping = {} #Stores encodings

storage_refresh_minutes = 1 #number of minutes after which to show embeddings again
recent_faces = {} #dict of captures and their time made in the last storage_refresh_minutes
recent_emotions = {} #dict of emotions recognized in the last storage_refresh_minutes

cap = cv2.VideoCapture(RTMP_URL)

print("got caputre")

def play_tone(face_encoding):
    #print("PLAYing tone:", face_encoding)
    sio.emit('play_tone', {'face_encoding': face_encoding})

def play_emotion(emotion):
    sio.emit('play_emotion', {'emotion': emotion})

def check_if_in_mapping(face_encoding):
    for key in mapping:
        face_encoding_array = np.array(face_encoding)
        result = face_recognition.compare_faces([face_encoding_array], np.array(key))

        if result[0]:
            return True

    return False

def caputure_from_video():
    name = ""#Where is name coming from??
    process_this_frame = 0
    frame_skips = 100 #Use (1/frame_skips) frames; ex) 1/3 skips 2 of 3 frames
    frame_count = 0
    while cap.isOpened():  # Untill end of file/error occured
      ret, frame = cap.read()

      #Delete old values from recent_faces and recent_captures
      for recent_face in list(recent_faces.keys()):
        if time.time() + storage_refresh_minutes - recent_faces[recent_face] <= 0:
           del recent_faces[recent_face]
      for recent_emotion in list(recent_emotions.keys()):
        if time.time() + storage_refresh_minutes - recent_emotions[recent_emotion] <= 0:
           del recent_emotions[recent_emotion]

      #Skip frames until frame_skips is reached
      if ret and (frame_count % frame_skips == 0):

        face_locations = face_recognition.face_locations(frame)
        if face_locations:
        # Compute the facial encodings for the faces detected
            face_encodings = face_recognition.face_encodings(frame, known_face_locations=face_locations)
            
            # You can now proceed with the face encodings (e.g., comparing or storing them)
            print("Face encodings:", len(face_encodings))
        else:
            print("No face locations detected")
            continue
        
        #Encodings are sorted from left to right
        #face_encodings = sorted(face_encodings, key=lambda x: x.known_face_locations[3])

        #Play a tone for each unique face if not played recently and record faces
        for face_encoding in face_encodings:
          tuple_face_encoding = tuple(face_encoding)
          if not check_if_in_mapping(face_encoding):
            mapping[tuple_face_encoding] = name
            
          #If tone was not played recenrly for this face, play it
          if tuple_face_encoding not in recent_faces:
            play_tone(face_encoding)

          #Record that the tone has been played
          recent_faces[tuple_face_encoding] = time.time()
               
        #Emotion Detection With DeepFace
        data = im.fromarray(frame)
        data.save("image_for_deepface.jpg")

        # try:
        emotion_analysis = DeepFace.analyze(
        img_path = "image_for_deepface.jpg",
        actions = ['emotion'],
        enforce_detection = False
        )

        #Play emotion if it was not recently played
        if(emotion_analysis[0]['dominant_emotion'] not in recent_emotions):
            play_emotion(emotion_analysis[0]['dominant_emotion'])

        #Update that the emotion was played recently
        recent_emotions[emotion_analysis[0]['dominant_emotion']] = time.time()

        print("DeepFace Analysis", emotion_analysis[0]['dominant_emotion'])
        # except:
        #    print("Deepface failed")

      frame_count +=1            
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("STEP 1")
    caputure_from_video()
    print("STEP 2")
    sio.connect('http://' + ip_address + ':' + port)
#    eventlet.wsgi.server(eventlet.listen(('', 4000)), app)
    print("Server started")