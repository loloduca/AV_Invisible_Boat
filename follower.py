"""
Author: Will Irwin
Last Modified: 2/12/2018
Title:follower.py
Inputs:

Outputs:

"""
import cv2
import rospy as rp
from rospy.numpy_msg import numpy_msg
import numpy as np

# def preprocess():
#
# def find_line():
#
# def follow_line():
#
#
# def callback(data):
    # rp.loginfo(rp.get_caller_id())+" I heard %s", data.data)

    # img = preprocess(data.data)
    # line = find_line(img)
    # dir = follow_line(line)
    cv2.imshow("ZED",data.data)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # while not rp.is_shutdown():
    output = dir
    rp.loginfo(output)
    pub.publish(output)


def listener():
    rp.init_node('Follower'Anonymous = True)
    rp.Subscriber('zed_receiver',numpy_msg(Ints),callback)
    # pub = rp.Publisher('movement_instructions',numpy_msg(Floats),queue_size = 10)
    rp.spin()


if __name__=="__main__":
    try:
        listener()
    except rp.ROSInterruptException:
        pass
