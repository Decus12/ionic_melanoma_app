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


"""**************************************************************************
Calculating the number of pixels in each block
**************************************************************************"""
#Object is divided into 4 different blocks based on the coordinates and midpoints calculated above.
#Using image cropping we divide each block with 255 so that they will only include 1s and 0s. Blocks can then be summed to get the ammount of detected pixels in each.
blocktl = binimg_inv[tlY:Ymid, tlX:Xmid]
blocktr = binimg_inv[trY:Ymid, Xmid:trX]
blockbl = binimg_inv[Ymid:blY, blX:Xmid]
blockbr = binimg_inv[Ymid:brY, Xmid:brX]

blocktl = np.sum(blocktl/255)
blocktr = np.sum(blocktr/255)
blockbl = np.sum(blockbl/255)
blockbr = np.sum(blockbr/255)


#print 'bl:',blockbl
#print 'tl:',blocktl
#print 'tr:',blocktr
#print 'br:',blockbr

"""***********************************************************************
Calculating the insymmetry threshold based on image size
***********************************************************************"""

scale = np.shape(binimg)

height = scale[0]
width = scale[1]

ratio = (width+height)/2

symthreshold = ratio*0.0005
symthreshold2 = ratio*0.001


"""************************************************************************
%Lohkoista saatujen puolikkaiden vertaus metodilla yksi
%***********************************************************************"""

symmetry_sec = 0

#Here we calculate the size of both horizontal and vertical halfs
#Once that's done we will calculate how many pixels each half may differ
#from each other. Based on thsat we can compare halfs to each other and decide
#if there is insymmetry to be found.

topsize = blocktl+blocktr
buttomsize = blockbl+blockbr
leftsize = blocktl+blockbl
rightsize = blocktr+blockbr

#print topsize
#print buttomsize
#print leftsize
#print rightsize

symmthresholdup = topsize*symthreshold
symmthresholdside = leftsize*symthreshold

topthresup = topsize+symmthresholdup
buttomthresup = topsize-symmthresholdup
topthresside = leftsize+symmthresholdside
buttomthresside = leftsize-symmthresholdside

symmthresholdup2 = topsize*symthreshold2
symmthresholdside2 = leftsize*symthreshold2

topthresup2 = topsize+symmthresholdup2
buttomthresup2 = topsize-symmthresholdup2
topthresside2 = leftsize+symmthresholdside2
buttomthresside2 = leftsize-symmthresholdside2


if (topthresup < buttomsize or buttomthresup > buttomsize):
     symmetry_sec=2
elif (topthresup2 < buttomsize or buttomthresup2 > buttomsize):
     symmetry_sec=1


if (topthresside < rightsize or buttomthresside > rightsize):
     symmetry_sec=2
elif (topthresside2 < rightsize or buttomthresside2 > rightsize):
     symmetry_sec=1
        
#print 'symmetry:',symmetry

