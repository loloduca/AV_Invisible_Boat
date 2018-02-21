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
from ackermann_msgs.msg import AckermannDriveStamped, AckermannDrive


def preprocess(img):
    h,w = img.shape[:2]
    L_Eye = img[0:h,0:w/2]
    R_Eye = img[0:h,w/2:w]
    return L_Eye

def find_line():
    print("needs to be implemented")

def follow_line():
    print("needs to be implemented")
    return speed,steering_angle,acceleration,jerk,steering_angle_velocity


def callback(data):
    bridge = CvBridge()
    drive_msg_stamped = AckermannDriveStamped()
    drive_msg = AckermannDrive()
    try:
        cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
	    #cv2.imshow("title",L_Eye)
        #cv2.waitKey(0)

        img = preprocess(cv_image)
        # line = find_line(img)
        # drive_msg.speed,drive_msg.steering_angle,drive_msg.acceleration,drive_msg.jerk,drive_msg.steering_angle_velocity = follow_line(line)
        drive_msg_stamped.drive = drive_msg
        # while not rp.is_shutdown():

        # rp.loginfo(drive_msg_stamped)
        # pub.publish(drive_msg_stamped)
    except CvBridgeError as e:
        print(e)




def follower():
    rp.init_node('Follower',anonymous = True)
    rp.Subscriber('zed_images',Image,callback)
    pub = rp.Publisher('movement_instructions',AckermannDriveStamped)
    rp.spin()


if __name__=="__main__":
    try:
        follower()
    except rp.ROSInterruptException:
        pass
    cv2.destroyAllWindows()
