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

def callback(data):
    try:
		pub.publish(data)
    except:
        print("shit broke bro, steering directions that driver.py received are broken")

def full_stop(data):
    try:
        pub.publish(data)
    except:
        print("shit broke bro, full stop execution failed")


def driver():
    rp.init_node('Driver',anonymous = True)
    rp.Subscriber('movement_instructions',AckermannDriveStamped,callback)
    rp.Subscriber('full_stop',AckermannDriveStamped,full_stop)
    pub=rp.Publisher("/vesc/ackermann_cmd_mux/input/navigation",AckermannDriveStamped,queue_size=10)
    rp.spin()


if __name__=="__main__":
    try:
        driver()
    except rp.ROSInterruptException:
        pass
    cv2.destroyAllWindows()
