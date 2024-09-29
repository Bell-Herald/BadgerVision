import cv2
from deepface import DeepFace
import face_recognition

#VALIDATION PRINTS
# print(cv2.__version__)
# print(DeepFace.__version__)
# print(face_recognition.__version__)

RTMP_URL = "rtmp://162.243.166.134:1935/live_321" #I think extra configs needed in nginx.conf

mapping = {} #Log first instace of an image to embedding, map to name; 
            #    embedding -> name, should later be in some DB
            #    (128,) len vector -> name(string)

cap = cv2.VideoCapture(RTMP_URL)

def play_tone(face_encoding):
    print("PLAY TONE: send message to client made up of the compressed face_encoding so they can play it")



def check_if_in_mapping(face_encoding):

    for key in mapping.keys():
        result = face_recognition.compare_faces([face_encoding], key)

        if result[0]:
            return True
    
    return False

def caputure_from_video():
    name = ""#Where is name coming from??
    process_this_frame = True
    while cap.isOpened():  # Untill end of file/error occured
        ret, frame = cap.read()
    
        if ret and process_this_frame:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            rgb_small_frame = small_frame[:, :, ::-1]

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding in face_encodings:
                if check_if_in_mapping(face_encoding):
                    play_tone(face_encoding)
                else:
                    mapping[face_encoding] = name
                    
            process_this_frame = not process_this_frame
    
    cap.release()
    cv2.destroyAllWindows()
            