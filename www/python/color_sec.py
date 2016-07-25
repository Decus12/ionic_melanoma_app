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
inte1 = np.zeros(256,)
inte2 = np.zeros(256,)
inte3 = np.zeros(256,)
ammount1 = 0
ammount2 = 0
ammount3 = 0
point = range(1,256)


"""**************************************************************************
Masking the moles surrounding and histogram array
**************************************************************************"""
#Here we mask areas we don't want to take into account when we calculate color uniformity
binimg_inv = cv2.bitwise_not(binimg)
masked = cv2.bitwise_and(gray,gray,mask = binimg_inv)

#cv2.imshow('res',masked)
#cv2.waitKey(0)

#In order to form the histogram from the object we want we need to separate it from the whole image
#This is to prevent histogram from being flooded with unwanted intensity information from else where
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

#Finally we calculate threshold points at the top of the largest intensity ammount and at 4/5 and 3/5 of it                
thres1 = max(hist)
thresspread = np.divide(thres1,5)
thres2 = np.multiply(thresspread,4)
thres3 = np.multiply(thresspread,3)

"""**************************************************************************
Calculating intensity amounts at threshold points
**************************************************************************"""

size = np.shape(hist)
#print 'size',(size)

#Here we calculate how many intensities there are at each threshold point

for I in xrange (0,size[0]): 
    #for J in xrange (0,size[1]):
        if thres1 == hist[I]:
            ammount1=ammount1+1

        if thres1 == hist[I]:
            inte1[I] = hist[I]
        else: 
            inte1[I] = 0


for I in xrange (0,size[0]): 
    #for J in xrange (0,size[1]):
        if thres2 <= hist[I]:
            ammount2=ammount2+1

        if thres2 <= hist[I]:
            inte2[I] = hist[I]
        else: 
            inte2[I] = 0
        #print (inte2)     


for I in xrange (0,size[0]): 
    #for J in xrange (0,size[1]):
        if thres3 <= hist[I]:
            ammount3=ammount3+1

        if thres3 <= hist[I]:
            inte3[I] = hist[I]
        else: 
            inte3[I] = 0



"""**************************************************************************
Searching the points that are equal or greater than threshold
**************************************************************************"""
points1 = np.zeros(ammount1,)
points2 = np.zeros(ammount2,)
points3 = np.zeros(ammount3,)
haa1 = 0-1
haa2 = 0-1
haa3 = 0-1


#From histogram we now calculate the ammount intensities that are greater than above
#threshold points    
for I in xrange (0,size[0]):
    haa1 = haa1+1
    #for J in xrange (0,[1]):
    if inte1[I] > 0:
        points1[I-haa1]= point[I]
        haa1 = haa1-1

for I in xrange (0,size[0]):
    haa2 = haa2+1
    #for J in xrange (0,[1]):
    if inte2[I] > 0:

        points2[I-haa2]=point[I]
        haa2 = haa2-1

for I in xrange (0,size[0]):
    #for J in xrange (0,[1]):
    haa3 = haa3+1
    if inte3[I] > 0:
        points3[I-haa3]=point[I]
        haa3 = haa3-1

#print(points2)        
"""**************************************************************************
Distance of intensities from each other
**************************************************************************"""
#Now we calculate how far away each intensity is from each other at threshold points
#The idea is that if two large ammounts of intensities are far from each other
#then they differ greatly and color is not uniform. However, two large intensity ammounts that are close
#each other imply that color is uniform with just minor differences in color shades
#which can be considered normal.


points1size = np.shape(points1)
if points1size > 1:

    last = points1[np.subtract(points1size,1)]
    points1ToSubstract = np.delete(points1,[0])
    points1ToSubstract = np.append(points1ToSubstract,[last])
    #print(points1ToSubstract)

    points1 = abs(points1 - points1ToSubstract)

    #print(points1)
else:
    points1 = [0]

points2size = np.shape(points2)
if points2size > 1:
    last = points2[np.subtract(points2size,1)]
    points2ToSubstract = np.delete(points2,[0])
    points2ToSubstract = np.append(points2ToSubstract,[last])
    #print(points2ToSubstract)

    points2 = abs(points2 - points2ToSubstract)

    #print(points2)
else:
    points2 = [0]

points3size = np.shape(points3)
if points3size > 1:    
    last = points3[np.subtract(points3size,1)]
    points3ToSubstract = np.delete(points3,[0])
    points3ToSubstract = np.append(points3ToSubstract,[last])
    #print(points3ToSubstract)

    points3 = abs(points3 - points3ToSubstract)

    #print(points3)
else:
    points1 = [0]



"""**************************************************************************
Defining the allowed distance
**************************************************************************"""


for I in xrange (0,points1size[0]):
    #for J in xrange (0,[1]):
        if points1[I] >= 10:
            diff1=100
        else:
            diff1=0

for I in xrange (0,points2size[0]):
    #for J in xrange (0,[1]):
        if points2[I] >= 10:
            diff2=10
        else:
            diff2=0

for I in xrange (0,points3size[0]):
    #for J in xrange (0,[1]):
        if points3[I] >= 10:
            diff3= 1
        else:
            diff3=0

"""******************************************************************
Size of the intensity spread
******************************************************************"""
spread1 = np.shape(points1)
spread2 = np.shape(points2)
spread3 = np.shape(points3)

spread1 = spread1[0]
spread2 = spread2[0]
spread3 = spread3[0]

#print (spread1)
#print (spread2)
#print (spread3)
"""**************************************************************************
Uniformity level
**************************************************************************"""
uniformity_sec = diff1 + diff2 + diff3
if uniformity_sec >= 100 or spread1 >= 5:
    uniformity_sec = 3
elif uniformity_sec >= 10 and uniformity_sec < 100 or spread2 >= 35:
        uniformity_sec = 2
elif uniformity_sec >=1 and uniformity_sec < 10 or spread3 >= 50:
        uniformity_sec = 1
elif uniformity_sec == 0:
        uniformity_sec = 0

"""**************************************************************************
Result
**************************************************************************"""
#print 'uniformity:',uniformity