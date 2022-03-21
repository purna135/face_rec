import face_recognition
import picamera
import numpy as np
import threading 

def face_rec():
	camera = picamera.PiCamera()
	camera.resolution = (320, 240)
	output = np.empty((240, 320, 3), dtype=np.uint8)

	# Load a sample picture and learn how to recognize it.
	print("Loading known face image(s)")
	anwesh_image = face_recognition.load_image_file("anwesh.jpeg")
	anwesh_face_encoding = face_recognition.face_encodings(anwesh_image)[0]

	rahul_image = face_recognition.load_image_file("rahul.jpeg")
	rahul_face_encoding = face_recognition.face_encodings(rahul_image)[0]


	known_face_encodings=[
		anwesh_face_encoding,
		rahul_face_encoding
	]

	known_face_names=[
		"Anwesh",
		"Rahul"
	]
	# Initialize some variables
	face_locations = []
	face_encodings = []

	while True:
		print("Capturing image.")
		# Grab a single frame of video from the RPi camera as a numpy array
		camera.capture(output, format="rgb")

		# Find all the faces and face encodings in the current frame of video
		face_locations = face_recognition.face_locations(output)
		print(f"Found {len(face_locations)} faces in image.")
		face_encodings = face_recognition.face_encodings(output, face_locations)

		# Loop over each face found in the frame to see if it's someone we know.
		for face_encoding in face_encodings:
			# See if the face is a match for the known face(s)
			match = face_recognition.compare_faces(known_face_encodings, face_encoding)
			name = "<Unknown Person>"

			if True in match:
				first_match_index = match.index(True)
				name = known_face_names[first_match_index]
			else:
				t = threading.Thread(target=send_mail)
				t.start()
			print(f"I see someone named {name}!")
			
			
			
face_rec()

def send_mail():
	print("sending email....")