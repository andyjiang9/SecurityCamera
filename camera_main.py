from playsound import playsound
import cv2
import time
import datetime
import numpy as np

cap = cv2.VideoCapture(0)

# set up classcade classifier with an existing cv classifiers
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 3

frame_size = (int(cap.get(3)), int(cap.get(4)))
# "m","p","4","v"
# video format
# fourcc = cv2.VideoWriter_fourcc(*"mp4v")

while True:
    # "_" is placeholder varaible
    _, frame = cap.read()
    
    # turns video/image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # detect faces in grayscale image, scale factor (accuracy and speed of algorithm shd be between 1.1-1.5; lower(~1) = accurate and slower;), minimum numbers of neighbors (1 face in an image is detected as many images [~20], min#neighbors is how many faces = 1 detected face; shd be between 3-6; more = less likely to detect face)
    # returns a list of all face locations
    faces = face_cascade.detectMultiScale(gray,1.1,2)
    #bodies = body_cascade.detectMultiScale(gray,1.1,1)
    
    for i in range(len(faces)):
        if i < len(faces) and (faces[i][1] < 100 or faces[i][2] > 195 or faces[i][2] < 155 or faces[i][3] > 195 or faces[i][3] < 155):
            # print(i)
            new_faces = np.delete(faces,i,0)
            faces = new_faces
            
            
    
    #if len(faces) + len(bodies) > 0:
    if len(faces) > 0:
        if detection:
            # already detected/someone came back before 5 second over
            timer_started = False
        else:
            # first detected
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            #out = cv2.VideoWriter(f"{current_time}.mp4", fourcc, 20, frame_size)
            print("Started Recording!")
    elif detection:
        if timer_started: # after video - 5 seconds after
            if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                detection = False
                timer_started = False
                #out.release()
                print("Stop Recording!")
        else: # face/body just dissapeared
            timer_started = True
            detection_stopped_time = time.time()
    
    #if detection:
        #out.write(frame)
    
    for(x,y,width,height) in faces:
        # draws on the colored "frame", two corners, color of rectangle (BGR NOT RGB), pixel width of rectangle
        cv2.rectangle(frame, (x,y), (x+width,y+height), (255,0,0), 2)
        cv2.putText(frame, str((x,y)), (x+width//4,y+height//4), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0), 2, cv2.LINE_AA)
        cv2.putText(frame, str((width,height)), (x+width//4,y+height//2), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0), 2, cv2.LINE_AA)
        
        if width > 125 and y > 185:
            print('HI')
            # playsound('C:/Users/Andy Jiang/Documents/.code practice/.Project Stuff/Security Camera/sine.wav')
        # print(str(width) + ": " + str(x) + " " + str(y))
        #playsound('C:/Users/Andy Jiang/Documents/.code practice/.Project Stuff/Security Camera/sine.wav')
        # playsound('C:/Users/Andy Jiang/Documents/.code practice/.Project Stuff/OpenCV/sine.wav')

        
    # for(x,y,width,height) in bodies:
    #     cv2.rectangle(frame, (x,y), (x+width,y+height), (255,0,0), 2)
    
    # shows camera on screen
    cv2.imshow("Camera", frame)
    
    # hit q key it stops
    if cv2.waitKey(1) == ord('q'):
        break
    
# saves video
# out.release()
# closes camera
cap.release()
# destroys the window
cv2.destroyAllWindows()
