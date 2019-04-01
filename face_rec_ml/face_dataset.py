import cv2
import os

cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# For each person, enter one numeric face id
face_name = input('Enter user Name: ')
face_id = input('Enter user ID: ')

fn_dir = 'dataset'
fn_name = face_name  # name of the person
path = os.path.join ( fn_dir, fn_name )
if not os.path.isdir ( path ):
    os.mkdir ( path )

print("\n[INFO] Initializing face capture...")
# Initialize individual sampling face count
count = 0

while(True):

    ret, img = cam.read()
    img = cv2.flip(img, 1) # flip video image vertically
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1

        # Save the captured image into the datasets folder
        cv2.imwrite("{}/{}.{}.{}{}".format(path,face_name, face_id, count, ".jpg"), gray[y:y+h,x:x+w])
        cv2.imshow('image', img)

    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= 30: # Take 30 face sample and stop video
         break

print("\n[INFO] Exiting Program...")
cam.release()
cv2.destroyAllWindows()