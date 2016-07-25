from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

#area = cv2.contourArea(box)
#equi_diameter = np.sqrt(4*area/np.pi)


#This looks rather silly with all the [0]'s here, but needs to be done to dig up the correct coordinates
"""leftmost = tuple(c[c.argmin(0)][0][0][0])
rightmost = tuple(c[c.argmax(0)][0][0][0])
topmost = tuple(c[c.argmin(0)][0][1][0])
bottommost = tuple(c[c.argmax(0)][0][1][0])"""


#In case we want to draw extreme coordinates of the object. Simply uncomment these: 
"""cv2.circle(orig, tuple(leftmost), 5, (255, 0, 0), -1)
cv2.circle(orig, tuple(rightmost), 5, (255, 0, 0), -1)
cv2.circle(orig, tuple(topmost), 5, (255, 0, 0), -1)
cv2.circle(orig, tuple(bottommost), 5, (255, 0, 0), -1)

#cv2.imshow("Detected Mole", orig)
#cv2.waitKey(0)"""

#Substract minimum and maximum x and y values from each other. Both vertically and horizontally
# in order to compare which one is longer

width = np.subtract(rightmost, leftmost)
height = np.subtract(topmost, bottommost)


#Calculate diameters and compare them

square1 = abs(np.sqrt(width[0]**2+width[1]**2))
square2 = abs(np.sqrt(height[0]**2+height[1]**2))

maxdiameter = max([square1, square2])


#Following is just for drawing diameter line on the image. Again uncomment if needed:
"""if (maxdiameter == square1):
    dialine = (rightmost, leftmost)
else:
    dialine = (topmost, bottommost)
    
dialine = ((int(dialine[0][0]),int(dialine[0][1])),(int(dialine[1][0]),int(dialine[1][1])))
    
cv2.line(img, tuple(dialine[0]), tuple(dialine[1]), (128, 0, 0), 2)


cv2.imshow("Detected Mole", img)
cv2.waitKey(0)"""    

#print 'diameter:',maxdiameter




