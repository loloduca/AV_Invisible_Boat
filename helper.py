"""
Author: Will Irwin
Last Modified: 2/22/2018
Title:helper.py
Inputs:

Outputs:

"""
import cv2
import os
import numpy as np
import math
import random


def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Or use BGR2GRAY if you read an image with cv2.imread()
    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def hsv(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

def display_img(title,img):
    cv2.imshow(title,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def canny(img, low_threshold, high_threshold):
    return cv2.Canny(img, low_threshold, high_threshold,True)

def gaussian_blur(img, kernel_size):
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def draw_lines(img, lines, color=[255, 0, 0], thickness=7):
    x_left,y_left,x_right,y_right = [],[],[],[]
    try:
        for line in lines:
            for x1,y1,x2,y2 in line:
                if(x1==x2):
                    continue
                slope = float(y2-y1)/float(x2-x1)
                if(slope>0.0):
                    x_right.append(x1.astype(int))
                    x_right.append(x2.astype(int))
                    y_right.append(y1.astype(int))
                    y_right.append(y2.astype(int))
                elif(slope<0.0):
                    x_left.append(x1.astype(int))
                    x_left.append(x2.astype(int))
                    y_left.append(y1.astype(int))
                    y_left.append(y2.astype(int))
        if(x_right and y_right):
            coeff = np.polyfit(np.array(x_right),np.array(y_right),1)
            poly = np.poly1d(coeff)
            x1,x2 = min(x_right),max(x_right)+200
            y1,y2 = poly(x1).astype(int),poly(x2).astype(int)
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)
        if(x_left and y_left):
            coeff = np.polyfit(np.array(x_left),np.array(y_left),1)
            poly = np.poly1d(coeff)
            x1,x2 = min(x_left)-200,max(x_left)
            y1,y2 = poly(x1).astype(int),poly(x2).astype(int)
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)
    except:
        print("No line was detected")

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    return cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)

def mask(img,lower_color,upper_color):
    mask = cv2.inRange(img, lower_color, upper_color)
    return cv2.bitwise_and(img,img,mask = mask)

def region_of_interest(img,vertices):
    print("Brett needs to write this")
