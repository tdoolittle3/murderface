import cv2
import argparse

global f, image

def onclick(event, x, y, flags, param):
	
	if event == cv2.EVENT_LBUTTONDOWN:
		f.write(str(x) + " " + str(y) + "\n")
		cv2.circle(image, (x,y), 2, (0, 255, 0)) 
		print "x: ",x,", y: ",y

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image", required=True, help="Image path")
ap.add_argument("-o","--output", required=True, help="Output filename")
args = vars(ap.parse_args())

f = open(args["output"], 'w')

image = cv2.imread(args["image"])
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", onclick)

while True:
	# display the image and wait for a keypress
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF
 
	# if the 'r' key is pressed, reset the cropping region
	if key == ord("r"):
		image = clone.copy()
 
	# if the 'c' key is pressed, break from the loop
	elif key == ord("c"):
		break

# close all open windows
cv2.destroyAllWindows()
f.close()
