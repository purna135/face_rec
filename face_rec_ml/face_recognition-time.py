import cv2
import numpy as np
import os
from speech import speak
import threading
import time

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0
names = {0:"None", 1:"Purna", 2:"Alok", 3:"Motu", 4:"Rajesh", 5:"Jayant"}
name = ""
t = 0
text = "Sorry, I can't recognise you"

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

while True:

    ret, img =cam.read()
    img = cv2.flip(img, 1) # Flip vertically

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for (x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # Check if confidence is less than 100 ==> "0" is perfect match
        if (confidence < 80):
            id = names[id]
            if name != id and (time.time() - t)>4:
                name=id
                t1 = threading.Thread(target = speak, args=(f"Hello {id}", ))
                t1.setDaemon(True)
                t1.start()
                t = time.time()

        else:
            id = "unknown"
            if name != id and (time.time() - t)>4:
                name=id
                t1 = threading.Thread(target = speak, args=(text,))
                t1.setDaemon(True)
                t1.start()
                t = time.time()

        confidence = "  {0}%".format(round(100 - confidence))

        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, confidence, (x+5,y+h-5), font, 1, (255,255,0), 1)  

    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

print("\n [INFO] Exiting Program...")
cam.release()
cv2.destroyAllWindows()
