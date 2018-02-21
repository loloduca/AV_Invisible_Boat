#!/usr/bin/env python
"""
Author: Will Irwin
Last Modified: 2/12/2018
Title:follower.py
Inputs:

Outputs:

"""
import cv2
import rospy as rp
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import Control



def preprocess(img):
    h,w = img.shape[:2]
    L_Eye = img[0:h,0:w/2]
    R_Eye = img[0:h,w/2:w]
    return L_Eye

def find_line():
    print("needs to be implemented")

def follow_line():
    print("needs to be implemented")


def callback(data):
    bridge = CvBridge()
    control = Control()
    try:
	    #cv2.namedWindow("Image window", cv2.WINDOW_NORMAL)
        cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
	    #cv2.imshow("title",L_Eye)
        #cv2.waitKey(0)
    except CvBridgeError as e:
        print(e)

    img = preprocess(cv_image)
    # line = find_line(img)
    # control.speed,control.steering_angle,control.acceleration,control.jerk,control.steering_angle_velocity = follow_line(line)

    # while not rp.is_shutdown():

    # rp.loginfo(control)
    # pub.publish(control)


def listener():
    rp.init_node('Follower',anonymous = True)
    rp.Subscriber('zed_images',Image,callback)
    pub = rp.Publisher('movement_instructions',Image)
    rp.spin()


if __name__=="__main__":
    try:
        listener()
    except rp.ROSInterruptException:
        pass
    cv2.destroyAllWindows()
