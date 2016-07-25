from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2


"""**************************************************************************
**************************************************************************
color uniformity
**************************************************************************
**************************************************************************"""


"""**************************************************************************
Masking the moles surrounding and histogram array
**************************************************************************"""
#Here we mask areas we don't want to take into account when we calculate color uniformity
binimg_inv = cv2.bitwise_not(binimg)
masked = cv2.bitwise_and(gray,gray,mask = binimg_inv)

#cv2.imshow('res',masked)
#cv2.waitKey(0)

#In order to form the histogram from the object we want we need to separate it from the whole image
#This is to prevent histogram from being flooded with unwanted intensity information from elsewhere
#in the image. This also enables this script to give different results for multiple objects in the image

tY = min([tlY,trY]) #top Y-coordinate
bY = max([blY,brY]) #buttom Y-coordinate
lX = min([tlX,blX]) #left X-coordinate
rX = max([trX,brX]) #right X-coordinate
   
moleinte = masked[tY:bY, lX:rX]
#cv2.imshow("cropped", moleinte)
#cv2.waitKey(0)
#print moleinte3


#forming the histogram for later calculations. The first member of the array which represents 
#black pixels from masking operation above we manually set to 0 so it's not taken into account later
hist,bins = np.histogram(moleinte.ravel(),256,[0,256])
hist[0] = 0
#print (hist)

"""***********************************************************************
Calculating signal to noise ratio
***********************************************************************""" 
#Using histogram (=hist) we can now calculate it's color mean and variance (=eveness). Variance increases the more there are 
#members of hist that differ greatly from it's mean.
#Square of variance equals standard deviation (=colorSd) which can then be used to calculate signal to noise ratio.
histsize = np.shape(hist)
eveness = np.zeros(histsize[0],)

colorMean = sum(hist)/histsize[0]

for e in xrange (0,histsize[0]):
    eveness[e] = hist[e]**2

colorSd = np.sqrt(sum(eveness)/histsize[0])

colorSnr = colorMean/colorSd
#print 'colorSnr:', colorSnr

"""**************************************************************************
Uniformity level
**************************************************************************"""
#Unlike normal snr, the ideal mole we want is concentrated in one spot of the histogram and therefore it differs greatly
#from "expected" value. For this reason smaller values actually indicate more even color and larger less even.
if colorSnr < 0.55:
    uniformity_prio = 0
elif colorSnr > 0.55 and colorSnr < 0.6:
    uniformity_prio = 1
elif colorSnr > 0.6:
    uniformity_prio = 2




"""**************************************************************************
Result
**************************************************************************"""
#print 'uniformity:',uniformity