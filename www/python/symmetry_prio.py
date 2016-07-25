from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2


#Calculate mid points between X and Y axis, which can then be used to calculate objects middle points
#which is then needed to divide object into 4 separate blocks.

M = cv2.moments(c)
Xmid = int(M['m10']/M['m00'])
Ymid = int(M['m01']/M['m00'])

#print (Xmid,Ymid)

#Alternate method to calculate midpoints. Will result in slightly different coordinates but not much.
"""smaX = min(tltrX,blbrX)

Xmid = np.int(round(abs(tltrX-blbrX)/2+smaX))

smaY = min(tlblY,trbrY)

Ymid = np.int(round(abs(tlblY-trbrY)/2+smaY))"""


tlX = np.int(round(tl[0]))
tlY = np.int(round(tl[1]))
trX = np.int(round(tr[0]))
trY = np.int(round(tr[1]))
blX = np.int(round(bl[0]))
blY = np.int(round(bl[1]))
brX = np.int(round(br[0]))
brY = np.int(round(br[1]))


#We need to make sure we are using extreme ends of the detected object, therefore we have to compare top and buttom values.
#After that we use these coordinates to split the object into upper and lower half.
Ymin = min(tlY,trY)
Ymax = max(blY,brY)
Xmin = min(tlX,blX)
Xmax = max(trX,brX)

blockUp = binimg_inv[Ymin:Ymid, Xmin:Xmax]
blockDown = binimg_inv[Ymid:Ymax, Xmin:Xmax]

#We can use opencv's shape comparison to decide whether or not mole's upper and lower parts are symmetrical.
#In order to do this we rotate the lower part 180 degrees, which will flip it both vertically and horizontally.
#This ensures that no matter the moles angle in the image, symmetrical sides will look very similar while insymmetrical
#will stand out either horizontally or vertically. 

rows,cols = blockDown.shape

M = cv2.getRotationMatrix2D((cols/2,rows/2),180,1)
blockDown = cv2.warpAffine(blockDown,M,(cols,rows))

"""cv2.imshow("blockUp", blockUp)
cv2.waitKey(0)
cv2.imshow("blockDown", blockDown)
cv2.waitKey(0)"""

sym = cv2.matchShapes(blockUp,blockDown,1,0.0)
#print 'sym:', sym


#By default we assume that moles are symmetrical and therefore we set it to 0. The closer to 0 above sym variable is the more #symmetrical the sides are.
#Threshold numbers here are very small, but these thresholds gave pretty good results with the few test images I used. 
symmetry_prio = 0


if sym > 0.004:
     symmetry_prio=2
elif sym > 0.003:
     symmetry_prio=1
        
#print 'symmetry:',symmetry

