"""
Author: Will Irwin
Last Modified: 2/12/2018
Title:zed.py
Inputs:

Outputs:

"""
import cv2
import rospy as rp
from rospy.numpy_msg import numpy_msg
import numpy as np


def get_zed_data():
    rp.init_node('Zed',anonymous = True)
    pub = rp.Publisher('zed_images',numpy_msg(Ints),queue_size = 10)
    rate = rp.rate(21)#21Hz

    while not rp.is_shutdown():
        cap = cv2.VideoCapture(0)
        while(cap.isOpened()):
            ret, frame = cap.read()
            output = frame
            rp.loginfo(output)
            pub.publish(output)
            rate.sleep()
        cap.release()

if __name__=="__main__":
    try:
        get_zed_data()
    except rp.ROSInterruptException:
        pass
