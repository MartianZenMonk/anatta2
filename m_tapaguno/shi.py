import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

video = cv.VideoCapture(0)

while True:
		# Reading frame(image) from video
		check, img = video.read()

		gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
		corners = cv.goodFeaturesToTrack(gray,25,0.01,10)
		corners = np.int0(corners)
		for i in corners:
		    x,y = i.ravel()
		    cv.circle(img,(x,y),3,255,-1)
		plt.imshow(img),plt.show()
		
		key = cv2.waitKey(1)
		if q entered whole process will stop
		if key == ord('q'):
		    break

video.release()
# Destroying all the windows
cv.destroyAllWindows()
img = cv.imread('blox.jpg')
