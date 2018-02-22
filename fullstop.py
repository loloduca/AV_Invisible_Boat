#!/usr/bin/env python
"""
Author: Will Irwin
Last Modified: 2/12/2018
Title:FullStop.py
Inputs:

Outputs:

"""
import cv2
import rospy as rp
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from ackermann_msgs.msg import AckermannDriveStamped, AckermannDrive
import helper as hp

bridge = CvBridge()

def detect_lines(img):
    black_roi = np.copy(img)

    vertices = [[80,540],[920,540],[470,300]]
    roi = hp.region_of_interest(img,vertices)

    black_roi[roi] = [0, 0, 0]
    black_roi = img - black_roi

    res_blue = hp.mask(black_roi, np.array([20,50,50]), np.array([30,255,255]))#needs proper hsv values to mask


    gray = hp.grayscale(res_blue)
    blur = hp.gaussian_blur(gray,5)
    edges = hp.canny(blur,40,60)
    hough = hp.hough_lines(edges,1,np.pi/180,threshold=1,min_line_len=55,max_line_gap=70)
    if hough.size == 0:
        return False
    return True

###need way to instant stop, this just turns all settings to 0
def halt():
    drive_msg_stamped = AckermannDriveStamped()
    drive_msg = AckermannDrive()

    drive_msg.speed = 0.0
    drive_msg.steering_angle = 0.0
    drive_msg.acceleration = 0
    drive_msg.jerk = 0
    drive_msg.steering_angle_velocity = 0

    drive_msg_stamped.drive = drive_msg
    pub.publish(drive_msg_stamped)

def zed(data):
    try:
        cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
        if not detect_lines(cv_image):
            halt()
    except:
        print("Something went wrong with full stop zed")

def lidar(data):
    print("Not Implemented")

def full_stop():
    rp.init_node('FullStop',anonymous = True)
    rp.Subscriber('preprocessed_zed',Image,zed)
    rp.Subscriber('lidar_data',Image,lidar)
    pub = rp.Publisher('full_stop',AckermannDriveStamped)
    rp.spin()


if __name__=="__main__":
    try:
        full_stop()
    except rp.ROSInterruptException:
        pass
