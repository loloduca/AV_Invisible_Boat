#!/usr/bin/env python
"""
Author: Will Irwin
Last Modified: 2/22/2018
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
import helper as hp

def preprocess(img):
    h,w = img.shape[:2]
    L_Eye = img[0:h,0:w/2]
    R_Eye = img[0:h,w/2:w]
    return L_Eye

def find_line(img):
    black_roi = np.copy(img)

    vertices = [[80,540],[920,540],[470,300]]###todo modify this and next line to suit bretts roi function
    roi = hp.region_of_interest(img,vertices)

    black_roi[roi] = [0, 0, 0]
    black_roi = img - black_roi

    res_blue = hp.mask(black_roi, np.array([20,50,50]), np.array([30,255,255]))#todo proper hsv values from davids code

    gray = hp.grayscale(res_blue)
    blur = hp.gaussian_blur(gray,5)
    edges = hp.canny(blur,40,60)
    hough = hp.hough_lines(edges,1,np.pi/180,threshold=1,min_line_len=55,max_line_gap=70)
    composite_line = hp.draw_line(img,hough)
    return composite_line


def follow_line(img):
    try:
        return speed,steering_angle,acceleration,jerk,steering_angle_velocity
    except:
        print("not implemented yet")



def callback(data):
    bridge = CvBridge()
    drive_msg_stamped = AckermannDriveStamped()
    drive_msg = AckermannDrive()
    try:
        cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
        img = preprocess(cv_image)

        output = bridge.cv2_to_imgmsg(img, "bgr8")
        preprocess_pub.publish(output)

        line = find_line(img)
        drive_msg.speed,drive_msg.steering_angle,drive_msg.acceleration,drive_msg.jerk,drive_msg.steering_angle_velocity = follow_line(line)
        drive_msg_stamped.drive = drive_msg
        move_pub.publish(drive_msg_stamped)
    except:
        print("Something went wrong with creating movement message ")




def follower():
    rp.init_node('Follower',anonymous = True)
    rp.Subscriber('zed_images',Image,callback)
    move_pub = rp.Publisher('movement_instructions',AckermannDriveStamped)
    preprocess_pub = rp.Publisher('preprocessed_zed',Image)
    rp.spin()


if __name__=="__main__":
    try:
        follower()
    except rp.ROSInterruptException:
        pass
    cv2.destroyAllWindows()
