#!/usr/bin/env python

from math import pi

import rospy
import tf
from geometry_msgs.msg import Quaternion

from chapter15.srv import FakeSensor, FakeSensorResponse
import fake_sensor


def make_quaternion(angle):
    q = tf.transformations.quaternion_from_euler(0, 0, angle)
    return Quaternion(*q)


def callback(request):
    angle = sensor.value * 2 * pi / 100.0
    q = make_quaternion(angle)
    return FakeSensorResponse(q)


if __name__ == '__main__':
    sensor = fake_sensor.FakeSensor()
    rospy.init_node('fake_sensor')
    rate = rospy.Rate(100.0)
    service = rospy.Service('angle', FakeSensor, callback)
    while not rospy.is_shutdown():
        rate.sleep()
