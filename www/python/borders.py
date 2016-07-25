from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2


"""***************************************************
******************************************************
Border Eveness
******************************************************
***************************************************"""
#An algorith to decide whether or not moles borders are uneven.
#We are using signal to noise ratio to calculate the how much "noise"
#there is in moles borders compared to ideal shape that is expected based
#on it's signal mean 
        
"""***********************************************************************
Creating the vector from detected border coordinates
***********************************************************************"""

#Detected borders are stored in the variable c, which contains matrix of x and y coordinates.
#By going through c we can subtract y values from x values and place them in vektor k.
#By subtracting y from x, vector k forms a signal wave which ideally rises and falls once if moles borders are ok.
#Wave rises when x grows but y doesn't and vice versa. Similarly it falls when x gets smaller but y grows and
#vice versa.

csize = np.shape(c)
k = np.zeros(csize[0],)
variance = np.zeros(csize[0],)

for s in xrange(0,csize[0]):
    k[s] = np.subtract(c[s,0,0],c[s,0,1])

"""***********************************************************************
Calculating signal to noise ratio
***********************************************************************""" 
#Using vector k we can now calculate it's mean and variance. Variance increases the more there are 
#members of k that differ greatly from it's mean. In other words it's bigger if moles borders are uneven.
#Square of variance equals standard deviation (sd) which can then be used to calculate signal to noise ratio.


mean = sum(k)/csize[0]

for v in xrange (0,csize[0]):
    variance[v] = k[v]**2

sd = np.sqrt(sum(variance)/csize[0])

snr = mean/sd
#print snr

"""***********************************************************************
Deciding whether mole's borders are uneven 
***********************************************************************"""
#Normally in snr values greater that 1 imply more signal than noise.
#However, since mole is never completely even it will always have some "noise".
#Therefore the first if here is for the cases where we consider moles borders to be even.
#First else if is for borderline cases where it's not quote clear and finally the last is 
#obviosly when we consider moles borders to be uneven.

#NOTE!!! I pulled these thresholds from my arse. They have not been throughly tested and are just for demo
#purposes for now.

if snr > 0.2:
    borderEveness = 0
elif snr < 0.2 and snr > 0.1:
    borderEveness = 1
elif snr < 0.1:
    borderEveness = 2

#print 'border:',borderEveness