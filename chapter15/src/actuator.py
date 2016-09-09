#!/usr/bin/env python

from math import fabs

import rospy
import actionlib
from std_msgs.msg import Float32
from chapter15.msg import RotationAction, RotationFeedback, RotationResult

from chapter15.srv import Light, LightResponse
from fake_actuator import FakeActuator


def volume_callback(msg):
    volume = min(100, max(0, int(msg.data * 100)))
    print('Setting volume to {}'.format(volume))
    actuator.volume = volume


def light_callback(request):
    actuator.toggle_light(request.on)
    print('Toggled light to {}'.format(request.on))
    return LightResponse(actuator.light_on)


def rotation_callback(goal):
    feedback = RotationFeedback()
    result = RotationResult()

    print('Setting actuator position to {}'.format(goal.orientation))
    actuator.set_position(goal.orientation)
    success = True

    rate = rospy.Rate(10)
    while fabs(goal.orientation - actuator.position) > 0.01:
        if a.is_preempt_requested():
            print('Actuator movement was preempted')
            success = False
            break

        print('Current actuator position: {}'.format(actuator.position))
        feedback.current_orientation = actuator.position
        a.publish_feedback(feedback)
        rate.sleep()

    result.final_orientation = actuator.position
    if success:
        print('Actuator movement succeeded; final orientation is {}'.format(
              actuator.position))
        a.set_succeeded(result)
    else:
        print('Actuator movement failed; final orientation is {}'.format(
              actuator.position))
        a.set_preempted(result)


if __name__ == '__main__':
    actuator = FakeActuator()
    # Initialize the node
    rospy.init_node('fake')
    # Topic for the volume
    t = rospy.Subscriber('fake/volume', Float32, volume_callback)
    # Service for the light
    s = rospy.Service('fake/light', Light, light_callback)
    # Action for the position
    a = actionlib.SimpleActionServer('fake/position', RotationAction,
                                     execute_cb=rotation_callback,
                                     auto_start=False)
    a.start()
    # Start everything
    rospy.spin()
