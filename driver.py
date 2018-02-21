#!/usr/bin/env python
"""
Author: Will Irwin
Last Modified: 2/21/2018
Title:driver.py
Inputs:

Outputs:

"""
import cv2
import rospy as rp
from ackermann_msgs.msg import AckermannDriveStamped, AckermannDrive
import Control

def callback(data):
    try:
    	rate=rp.Rate(60)
    	drive_msg_stamped = AckermannDriveStamped()
    	drive_msg = AckermannDrive()
           	drive_msg.speed = 0.8
            drive_msg.steering_angle = 1.0
            drive_msg.acceleration = 0
            drive_msg.jerk = 0
            drive_msg.steering_angle_velocity = 0
    	drive_msg_stamped.drive = drive_msg
    	while True:
    		pub.publish(drive_msg_stamped)
    		rate.sleep()
    except CvBridgeError as e:
        print(e)

    # while not rp.is_shutdown():
    # output = dir

    # rp.loginfo(output)
    # pub.publish(output)


def listener():
    rp.init_node('Driver',anonymous = True)
    rp.Subscriber('movement_instructions',Control,callback)
    pub=rp.Publisher("/vesc/ackermann_cmd_mux/input/navigation",AckermannDriveStamped,queue_size=10)
    rp.spin()


if __name__=="__main__":
    try:
        listener()
    except rp.ROSInterruptException:
        pass
    cv2.destroyAllWindows()
