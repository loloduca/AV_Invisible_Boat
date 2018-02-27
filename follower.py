#!/usr/bin/env python
'''
Author(s):  Invisible Boat Team

'''
import cv2
import rospy as rp
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from math import pi

red = [([0,100,100],[7,255,255]),([172,100,100],[179,255,255])]
blue = ([100,60,60],[131,255,255])
green = ([41,100,100],[75,255,255])

# def preprocess():
#
# def find_line():
#
# def follow_line():

# ------ Region of Interest -----
def regionOfInterest(image,ROI):

	# Top Left, Bottom Left, Bottom Right, Top Right
	vertices = np.array([ROI], dtype=np.int32)

	mask = np.zeros_like(image)

	if len (image.shape) > 2:
		channel_count = image.shape[2]
		ignore_color = (255,) * channel_count
	else:
		ignore_color = 255

	cv2.fillPoly(mask, vertices, ignore_color)
	maskedImage = cv2.bitwise_and(image, mask)

	return maskedImage

# --------------- Color Detection ---------------
def colorFilter(image):
	hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

	# Blues
	blue_lower_range = np.array(blue[0], dtype=np.uint8)
	blue_upper_range = np.array(blue[1], dtype=np.uint8)

	blueMask = cv2.inRange(hsv_img, blue_lower_range, blue_upper_range)
	blueFilteredImage = cv2.bitwise_and(image, image, mask = blueMask)

	return blueFilteredImage

# ------ Image Processing -----
def cleanImage(rawImage,ROI):

    # Gaussian Blur to Remove Noise
    blurredImage = blur(rawImage, 13)

    # Crop out all the crap
    croppedImage = regionOfInterest(blurredImage,ROI)

    # Filter out unnecessary colors
    filteredImage = colorFilter(croppedImage)

    # Convert to Greyscale
    cleanedImage = convertGreyscale(filteredImage)
    
    #displayImage(filteredImage)
    return cleanedImage

# ------ Helper Functions -----


def rad(degree):
	return (degree*pi)/180

def convertGreyscale(image):
	return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

def canny(image, low, high):
	return cv2.Canny(image, low, high)

def blur(image, size):
	return cv2.GaussianBlur(image, (size, size), 0)

def genColorMask(image):
	color_thresholds = (image[:,:,0] < white_threshold[0]) | (image[:,:,1] < white_threshold[1]) | (image[:,:,2] < white_threshold[2])
	return color_thresholds

def displayImage(image):
	cv2.namedWindow("Color Detection", cv2.WINDOW_NORMAL)
	cv2.resizeWindow('Color Detection', 1920,1080)
	cv2.imshow("Color Detection", image)
	cv2.waitKey(0)

def processImage(image,ROI):

    # ------ Main -----
    rawImage = image
    overlayImage = rawImage.copy()

    # Set contour threashold. 0 for everything, since the image has already been cleaned
    ret, threshold = cv2.threshold(cleanImage(rawImage,ROI), 0, 255, 0)

    # Find the contours
    contourMask, contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #displayImage(contourMask)

    # Find the center of the contour region, no idea wtf this does, but it works
    lineRegion = max(contours,key=cv2.contourArea)
    imageMoment = cv2.moments(lineRegion)
    centerX = int(imageMoment['m10'] / imageMoment['m00'])
    centerY = int(imageMoment['m01'] / imageMoment['m00'])

    # Draw the contours on the image
    cv2.drawContours(overlayImage, lineRegion, -1, (0,255,0), 5)

    # Draw circle at the center of the contour
    cv2.circle(overlayImage, (centerX, centerY), 7, (0, 0, 255), -1)

    # Display the image
    return overlayImage

 
def callback(data):
    bridge = CvBridge()
    L_offset = 0
    R_offset = 0
    try:
        #cv2.namedWindow("Image window", cv2.WINDOW_NORMAL)
        cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
        displayImage(cv_image)
        h,w = cv_image.shape[:2]
        eye_w = w/2
        L_Eye = cv_image[0:h,0:(w/2)]
        R_Eye = cv_image[0:h,(w/2):w]
        output = np.zeros((h,w,3))
        L_ROI = [(round(eye_w*1/4),h),(round(eye_w*2/3),round(h*1/2)),(round(eye_w),h*2/3),(round(eye_w),h)]
        R_ROI = [(0,h),(0,h*2/3),(round(eye_w*1/3),round(h*1/2)),(round(eye_w*3/4),h)]
        L_Image = processImage(L_Eye, L_ROI)
        R_Image = processImage(R_Eye, R_ROI)
        output[0:h,0:(w/2)] = L_Image
        output[0:h,(w/2):w] = R_Image
        output = np.array(output, dtype = "uint8")
        cv2.imshow("title",output)
        cv2.waitKey(1)
    except CvBridgeError as e:
        print(e)

    # img = preprocess(data.data)
    # line = find_line(img)
    # dir = follow_line(line)

    # while not rp.is_shutdown():
    # output = dir

    # rp.loginfo(output)
    # pub.publish(output)


def listener():
    rp.init_node('Follower',anonymous = True)
    rp.Subscriber('zed_images',Image,callback)
    pub = rp.Publisher('movement_instructions',Image,queue_size=10)
    rp.spin()


if __name__=="__main__":
    try:
        listener()
    except rp.ROSInterruptException:
        pass
    cv2.destroyAllWindows()
