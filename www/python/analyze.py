from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import time

timestamp1 = time.time()
def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())


# load the image, convert it to grayscale, and blur it slightly
image = cv2.imread(args["image"])
img  = cv2.imread(args["image"],0)
#cv2.imshow("Image", image)
#cv2.waitKey(0)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

gray = cv2.GaussianBlur(gray, (7, 7), 0)
imageSize=np.shape(gray)
objectThreshold=imageSize[0]*imageSize[1]/1000
imgMidpoint = np.divide(imageSize,2)
#print imgMidpoint

ten_percent = (imageSize[1]/10, imgMidpoint[0])
#print ten_percent

ninety_percent = (ten_percent[0]*9,imgMidpoint[0])
#print ninety_percent

crop_left = gray[ten_percent[1]-5:ten_percent[1]+5, ten_percent[0]-5:ten_percent[0]+5] # Crop from x, y, w, h
# NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
#print crop_left
#cv2.imshow("cropped", crop_left)
#cv2.waitKey(0)

crop_right = gray[ninety_percent[1]-5:ninety_percent[1]+5, ninety_percent[0]-5:ninety_percent[0]+5]
#print crop_right
#cv2.imshow("cropped", crop_right)
#cv2.waitKey(0)

crop_middle = gray[imgMidpoint[0]-5:imgMidpoint[0]+5, imgMidpoint[1]-5:imgMidpoint[1]+5]
#print crop_middle
#cv2.imshow("cropped", crop_middle)
#cv2.waitKey(0)

avg_left = np.average(crop_left)
avg_right = np.average(crop_right)
avg_middle = np.average(crop_middle)
#print avg_left
#print avg_right
avglr = (avg_left+avg_right)/2
#print avglr
#print avg_middle
avglrm = (avglr+avg_middle)/2
#print avglrm


avg = np.average(gray)
#print avg
avgam = (avg+avg_middle)/2
#print avgam

ret, binimg = cv2.threshold(gray,avglrm,255,cv2.THRESH_BINARY)
#binimg = cv2.erode(binimg, None, iterations=1)
binimg = cv2.morphologyEx(binimg, cv2.MORPH_OPEN, None)
binimg = cv2.morphologyEx(binimg, cv2.MORPH_CLOSE, None)
binimg = cv2.erode(binimg,None,iterations = 2)
#cv2.imshow("Image", binimg)
#cv2.waitKey(0)


 
# perform edge detection, then perform a dilation + erosion to
# close gaps in between object edges
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)



binimg_inv = cv2.bitwise_not(binimg)
#cv2.imshow("Image", binimg_inv)
#cv2.waitKey(0)
cnts = cv2.findContours(binimg_inv.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_NONE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
 
# sort the contours from left-to-right and initialize the
# 'pixels per metric' calibration variable
(cnts, _) = contours.sort_contours(cnts)

#print "object size Threshold =", objectThreshold

closest1 = imageSize
# loop over the contours individually
for c in cnts:
	# if the contour is not sufficiently large, ignore it
	if cv2.contourArea(c) > objectThreshold:
            #leftmost = tuple(c[c.argmin(0)][0][0][0])
            #rightmost = tuple(c[c.argmax(0)][0][0][0])
            #topmost = tuple(c[c.argmin(0)][0][1][0])
            #bottommost = tuple(c[c.argmax(0)][0][1][0])
            """print "midpointX", imgMidpoint[1]
            print "left",leftmost[0]
            print "right",rightmost[0]
            print "midpointY", imgMidpoint[0]
            print "top",topmost[1]
            print "buttom",bottommost[1]"""
            distance = cv2.pointPolygonTest(c,(imgMidpoint[1],imgMidpoint[0]),True)
            #print distance
            #if imgMidpoint[1] > leftmost[0] and imgMidpoint[1] < rightmost[0] and imgMidpoint[0] < bottommost[1] and imgMidpoint[0] > topmost[1] and distance > 0:
            if distance > 0:    
                

                img = cv2.drawContours(image, c, -1, (0,255,0), 3)
                #cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
                #cv2.imshow("Image", img)
                #cv2.waitKey(0)

                # compute the rotated bounding box of the contour
                orig = image.copy()
                box = cv2.minAreaRect(c)
                box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
                box = np.array(box, dtype="int")

                # order the points in the contour such that they appear
                # in top-left, top-right, bottom-right, and bottom-left
                # order, then draw the outline of the rotated bounding
                # box
                box = perspective.order_points(box)
                cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

                # loop over the original points and draw them
                for (x, y) in box:
                    cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

            # unpack the ordered bounding box, then compute the midpoint
                # between the top-left and top-right coordinates, followed by
                # the midpoint between bottom-left and bottom-right coordinates
                (tl, tr, br, bl) = box
                (tltrX, tltrY) = midpoint(tl, tr)
                (blbrX, blbrY) = midpoint(bl, br)

                # compute the midpoint between the top-left and top-right points,
                # followed by the midpoint between the top-righ and bottom-right
                (tlblX, tlblY) = midpoint(tl, bl)
                (trbrX, trbrY) = midpoint(tr, br)

                # draw the midpoints on the image
                cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
                cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
                cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
                cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)




                # draw lines between the midpoints
                cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
                    (255, 0, 255), 2)
                cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
                    (255, 0, 255), 2)

                # compute the Euclidean distance between the midpoints
                dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
                dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

                # if the pixels per metric has not been initialized, then
                # compute it as the ratio of pixels to supplied metric
                # (in this case, inches)

                # show the output image
                #cv2.imshow("Image", orig)
                #cv2.waitKey(0)
            #print cnts

            #for device: 
                execfile("python/symmetry_prio.py")
                print symmetry_prio
                execfile("python/symmetry_sec.py")
                print symmetry_sec
                execfile("python/color_prio.py")
                print uniformity_prio
                execfile("python/color_sec.py")
                print uniformity_sec
                execfile("python/borders.py")
                print borderEveness

            #for console:     
                """execfile("symmetry_prio.py")
                print 'symmetry primary:', symmetry_prio
                execfile("symmetry_sec.py")
                print 'symmetry secondary:', symmetry_sec
                execfile("color_prio.py")
                print 'uniformity primary:', uniformity_prio
                execfile("color_sec.py")
                print 'uniformity secondary:', uniformity_sec
                execfile("borders.py")
                print 'border eveness:', borderEveness
timestamp2 = time.time()
print "timespent", (timestamp2-timestamp1)"""