import cv2
import numpy as np
from PIL import Image
import os

# Path for face image database
database_path = "dataset"
img_dirs = [x[0] for x in os.walk(database_path)][1::]

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

# get the images and label data
faceSamples=[]
ids = []

for path in img_dirs:
    path = str(path)
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     


    for imagePath in imagePaths:

        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')

        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)

        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)


recognizer.train(faceSamples, np.array(ids))

print ("\n[INFO] Training faces. It will take a few seconds. Wait ...")

# Save the model into trainer/trainer.yml
recognizer.write('trainer/trainer.yml')

# Print the numer of faces trained and end program
print("\n[INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
