import cv2, sys

def show_features(image):
	face_cascade = cv2.CascadeClassifier('/home/boon/software/opencv-3.1.0/data/haarcascades/haarcascade_frontalface_alt.xml')

	body_cascade = cv2.CascadeClassifier('/home/boon/software/opencv-3.1.0/data/haarcascades/haarcascade_fullbody.xml')

	upper_body_cascade = cv2.CascadeClassifier('/home/boon/software/opencv-3.1.0/data/haarcascades/haarcascade_upperbody.xml')

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(gray, 1.5, 5)
	bodies = body_cascade.detectMultiScale(gray, 1.5, 5)
	upper_bodies = upper_body_cascade.detectMultiScale(
		gray,
		scaleFactor=1.5,
		minNeighbors=5,
		minSize=(30,30)
	)

	print "Found " + str(len(faces)) + " face(s)."
	print "Found " + str(len(bodies)) + " bodies."
	print "Found " + str(len(upper_bodies)) + " upper bodies."

	for (x,y,w,h) in faces:
		cv2.rectangle(image, (x,y), (x+w,y+h), (255,0,0), 2)

	for (x,y,w,h) in bodies:
		cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)

	for (x,y,w,h) in upper_bodies:
		cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,255), 2)

	cv2.imwrite('result.jpg', image)

if len(sys.argv) > 1 and sys.argv[1][len(sys.argv[1])-3:len(sys.argv[1])] == "jpg":
	image = cv2.imread(sys.argv[1], 1)
	show_features(image)
	exit(0)

import picamera
import io
import numpy

stream = io.BytesIO()

with picamera.PiCamera() as camera:
#	camera.image_effect = 'cartoon' 
	camera.resolution = (640, 480)
#	camera.saturation = 20
#	camera.contrast = 0
#	camera.sharpness = 30
	camera.brightness = 55
	camera.vflip = True
	camera.hflip = True
	camera.capture(stream,format='jpeg')

buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

image = cv2.imdecode(buff, 1)

show_features(image)

camera.close()

