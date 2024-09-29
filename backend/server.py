
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
import os

port = "3000"
ip_address = "162.243.166.134"

sio = socketio.Client()

def load_mapping_from_json(file_path):
    # Check if the file exists and is non-empty
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        # Open and load the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
            
            # Convert the keys back to tuples of floats, if needed
            mapping = {tuple(map(float, key.split(','))): value for key, value in data.items()}
    else:
        # If the file doesn't exist or is empty, return an empty dict
        mapping = {}

    return mapping

def save_mapping_to_json(mapping, file_path):
    # Convert the tuple keys to strings to store them in JSON
    data = {','.join(map(str, key)): value for key, value in mapping.items()}
    
    # Save the dictionary to the JSON file
    with open(file_path, 'w') as file:
        json.dump(data, file)

RTMP_URL = None
mapping = load_mapping_from_json("mappings.json") #Stores encodings

storage_refresh_minutes = 1 #number of minutes after which to show embeddings again
recent_faces = {} #dict of captures and their time made in the last storage_refresh_minutes
recent_emotions = {} #dict of emotions recognized in the last storage_refresh_minutes

###Initialize server
# create a Socket.IO server
#sio = socketio.Server(cors_allowed_origins='*')  # Allow requests from any origin

# wrap with a WSGI application
#app = socketio.WSGIApp(sio)

###Listen to events

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


#Create an RTMP_Listener after hearing back from the client
@sio.on('session_name')
def initiate_RTMP_from_session_name(sid, name):
    RTMP_URL = "rtmp://162.243.166.134:1935/live/{name}" #I think extra configs needed in nginx.conf
    cap = cv2.VideoCapture(RTMP_URL)
    print("got caputre")
    caputure_from_video(cap, sid)

# Backup: Create an RTMP_Listener on the server-side by reading from text file.
def initiate_RTMP_from_file(sid):
    with open("session_name.txt", "r") as file:
        name = file.read()
        RTMP_URL = f"rtmp://162.243.166.134:1935/live/{name}"
    cap = cv2.VideoCapture(RTMP_URL)
    caputure_from_video(cap, sid)

#Catches other event that was not already caught
@sio.on('*')
def any_event(event, sid, data):
     print('EVENT::', event, "| ID:", sid, "| DATA:", data)
     pass

def play_tone(face_encoding, sid):
    #print("PLAYing tone:", face_encoding)
    sio.emit('play_tone', {'face_encoding': face_encoding, "sid": sid})

def play_emotion(emotion, sid):
    sio.emit('play_emotion', {'emotion': emotion, 'sid': sid})

def check_if_in_mapping(face_encoding):
    for key in mapping:
        face_encoding_array = np.array(face_encoding)
        result = face_recognition.compare_faces([face_encoding_array], np.array(key))

        if result[0]:
            return True

    return False

def caputure_from_video(cap, sid):
    name = "" #Leave name as blank if not known
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
            if(mapping[tuple_face_encoding] == ""):
                #If unnamed, play tone
                play_tone(face_encoding, sid)
            else:
                #Otherwise, play name
                play_emotion(mapping[tuple_face_encoding], sid)

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
            play_emotion(emotion_analysis[0]['dominant_emotion'], sid)

        #Update that the emotion was played recently
        recent_emotions[emotion_analysis[0]['dominant_emotion']] = time.time()

        print("DeepFace Analysis", emotion_analysis[0]['dominant_emotion'])
        # except:
        #    print("Deepface failed")

      frame_count +=1            
    
    cap.release()
    cv2.destroyAllWindows()
    save_mapping_to_json(mapping, "mappings.json")

if __name__ == "__main__":
    print("STEP 1")
    sio.connect('http://' + ip_address + ':' + port)
    sio.emit('C2_AUTHORIZATION', sio.sid)
    print("CS2 UP")
    initiate_RTMP_from_file(sio.sid)