#!/usr/bin/env python

import numpy

import cv2
import cv_bridge
import rospy

from sensor_msgs.msg import Image


class Follower:
    def __init__(self):
        self.bridge = cv_bridge.CvBridge()
        cv2.namedWindow("window", 1)
        self.image_sub = rospy.Subscriber('camera/rgb/image_raw', Image,
                                          self.image_callback)

    def image_callback(self, msg):
        image = self.bridge.imgmsg_to_cv2(msg)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_yellow = numpy.array([50, 50, 170])
        upper_yellow = numpy.array([255, 255, 190])
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        cv2.bitwise_and(image, image, mask=mask)
        cv2.imshow("window", mask)
        cv2.waitKey(3)


rospy.init_node('follower')
follower = Follower()
rospy.spin()
