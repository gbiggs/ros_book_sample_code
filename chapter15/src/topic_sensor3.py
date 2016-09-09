#!/usr/bin/env python

from math import pi
from threading import Lock
from time import sleep

from geometry_msgs.msg import Quaternion
import rospy
import tf

from fake_sensor import FakeSensor


def make_quaternion(angle):
    q = tf.transformations.quaternion_from_euler(0, 0, angle)
    return Quaternion(*q)


def save_value(value):
    global angle
    with lock:
        angle = value * 2 * pi / 100.0


if __name__ == '__main__':
    lock = Lock()

    sensor = FakeSensor()
    sleep(1)
    sensor.register_callback(save_value)

    rospy.init_node('fake_sensor')

    pub = rospy.Publisher('angle', Quaternion, queue_size=10)

    angle = None
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        with lock:
            if angle:
                q = make_quaternion(angle)
                pub.publish(q)
        rate.sleep()
