#!/usr/bin/env python

from math import pi
from time import sleep

import rospy
import tf
from geometry_msgs.msg import Quaternion

from fake_sensor import FakeSensor


def make_quaternion(angle):
    q = tf.transformations.quaternion_from_euler(0, 0, angle)
    return Quaternion(*q)


def publish_value(value):
    angle = value * 2 * pi / 100.0
    q = make_quaternion(angle)
    pub.publish(q)


if __name__ == '__main__':
    rospy.init_node('fake_sensor')
    pub = rospy.Publisher('angle', Quaternion, queue_size=10)
    sensor = FakeSensor()
    sleep(1)
    sensor.register_callback(publish_value)
    # Because we are now using a callback rather than a ROS sleep cycle, we
    # must prevent the program from exiting immediately
    raw_input('Press enter to quit')
