#!/usr/bin/env python
'''
Author(s):  Invisible Boat Team

'''
import rospy as rp
import cv2
from cv_bridge import CvBridge, CvBridgeError
from operator import itemgetter
from sensor_msgs.msg import Image
from math import pi
from ackermann_msgs.msg import AckermannDriveStamped, AckermannDrive
from car_utils import imgproc

red = [([0,100,100],[7,255,255]),([172,100,100],[179,255,255])]
blue = ([100,80,60],[131,255,255])
green = ([41,100,100],[75,255,255])

move_pub = rp.Publisher('movement_instructions',AckermannDriveStamped,queue_size=10)


# ------ Helper Functions -----


def rad(degree):
	return (degree*pi)/180

old_errors = [0]
def steeringControl(error):
    kp = 0.15
    ki = 0.0
    kd = 0.05
    
    proportional = error
    integral = sum(old_errors)
    derivative = old_errors[-2]+error

    output = ((kp * proportional) + (ki*integral) + (kd*derivative))
    if(output<-1):
        output = -1
    if(output>1):
        output = 1

    return -output

bridge = CvBridge()
drive_msg_stamped = AckermannDriveStamped()
drive_msg = AckermannDrive()
zed = imgproc()
h,w = 376,1344
zed.set_ROI(ROI = [((w*1/8),h),((w*1/3),(h/2)),((w/2),(h*2/3)),((w*2/3),(h/2)),((w*7/8),h)])
def callback(data):
    global old_errors
    try:
        zed.set_display(rp.get_param('~display'))
        zed.set(bridge.imgmsg_to_cv2(data, "bgr8"))
        impulse = zed.get_impulse(4,13,blue)
        if impulse != None:
            impulse/=(180)
            old_errors += [impulse]
            if len(old_errors) > 100:
                old_errors = old_errors[1:]
            drive_msg.speed,drive_msg.steering_angle,drive_msg.acceleration,drive_msg.jerk,drive_msg.steering_angle_velocity = follow_line(impulse)
            drive_msg_stamped.drive = drive_msg
            move_pub.publish(drive_msg_stamped)
    except CvBridgeError as e:
        print(e)

def follow_line(impulse):
    try:
        speed = 0.5
        steering_angle = steeringControl(impulse)
        print "Steering: %f"%steering_angle
        acceleration = 0
        jerk = 0
        steering_angle_velocity = 0
        return speed,steering_angle,acceleration,jerk,steering_angle_velocity
    except:
        print("not implemented yet")

def listener():
    rp.Subscriber('zed_images',Image,callback,queue_size=1)
    rp.spin()


if __name__=="__main__":
    try:
        rp.init_node('Follower',anonymous = True)
        listener()
    except rp.ROSInterruptException:
        pass
    cv2.destroyAllWindows()
