# import the necessary packages
import numpy as np
import argparse
import cv2
import regions

# regions.Regions(xIntercept, width, length, yIntercept, rows, columns)
regions = regions.Regions(50,400,400,50,3,3)
videoCapture = cv2.VideoCapture(0)

while True:

	ret, image = videoCapture.read()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.blur(gray,(5,5))

	# detect circles in the image
	circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.4, 30)

	# ensure at least some circles were founds
	if circles is not None:
		# convert the (x, y) coordinates and radius of the circles to integers
		circles = np.round(circles[0, :]).astype("int")

		# loop over the (x, y) coordinates and radius of the circles
		for (x, y, r) in circles:
			# draw the circle in the output image, then draw a rectangle
			# corresponding to the center of the circle

			cv2.circle(image, (x, y), r, (0, 255, 0), 4)
			cv2.rectangle(image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
			print "Region", regions.checkRegion(x,y)
			print "X: ", x, "Y: ", y


	# show the output image
	fontIndex = 0

	#draw all the regions
	for i in xrange(regions.totalYintercepts-1):
	    for ii in xrange(regions.totalXintercepts-1):

	        x1 = regions.xIntercepts()[ii]
	        x2 = regions.xIntercepts()[ii + 1]
	        y1 = regions.yIntercepts()[i]
	        y2 = regions.yIntercepts()[i+1]
	        cv2.rectangle(image,(x1,y1),(x2,y2),(0,255,0),2)
	        fontIndex = fontIndex + 1
	        font = cv2.FONT_HERSHEY_SIMPLEX
	        cv2.putText(image,str(fontIndex),(x1 +5,y1+25), font, 0.7,(255,255,255),2)

	cv2.imshow('Video',image)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

videoCapture.release()
cv2.destroyAllWindows()
