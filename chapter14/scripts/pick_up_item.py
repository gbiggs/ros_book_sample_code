#!/usr/bin/env python

import sys

import rospy

import tf
import actionlib
import moveit_commander
from control_msgs.msg import GripperCommandAction, GripperCommandGoal
from geometry_msgs.msg import Pose, Quaternion
from tf.transformations import quaternion_from_euler
from look_at_bin import look_at_bin
from std_srvs.srv import Empty
from moveit_python import PlanningSceneInterface


if __name__ == '__main__':
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('pick_up_item')
    args = rospy.myargv(argv=sys.argv)
    if len(args) != 2:
        print('usage: pick_up_item.py BIN_NUMBER')
        sys.exit(1)
    item_frame = 'item_{}'.format(args[1])

    print('Waiting for clear_octomap')
    rospy.wait_for_service('/clear_octomap')
    clear_octomap = rospy.ServiceProxy('/clear_octomap', Empty)
    print('Got clear_octomap')

    gripper = actionlib.SimpleActionClient('gripper_controller/gripper_action',
                                           GripperCommandAction)
    gripper.wait_for_server()

    arm = moveit_commander.MoveGroupCommander('arm')
    arm.allow_replanning(True)
    tf_listener = tf.TransformListener()
    rate = rospy.Rate(10)

    gripper_goal = GripperCommandGoal()
    gripper_goal.command.max_effort = 10.0

    scene = PlanningSceneInterface('base_link')

    p = Pose()
    p.position.x = 0.4 + 0.15
    p.position.y = -0.4
    p.position.z = 0.7 + 0.15
    p.orientation = Quaternion(*quaternion_from_euler(0, 1, 1))
    arm.set_pose_target(p)

    while True:
        if arm.go(True):
            break
        clear_octomap()
        scene.clear()

    look_at_bin()
    while not rospy.is_shutdown():
        rate.sleep()
        try:
            t = tf_listener.getLatestCommonTime('/base_link', item_frame)
            if (rospy.Time.now() - t).to_sec() > 0.2:
                rospy.sleep(0.1)
                continue

            item_translation, item_orientation = tf_listener.lookupTransform(
                '/base_link', item_frame, t)
        except (tf.Exception, tf.LookupException, tf.ConnectivityException,
                tf.ExtrapolationException):
            continue

        gripper_goal.command.position = 0.15
        gripper.send_goal(gripper_goal)
        gripper.wait_for_result(rospy.Duration(1.0))

        print('Item: ' + str(item_translation))
        scene.addCube('item', 0.05, item_translation[0], item_translation[1],
                      item_translation[2])

        p.position.x = item_translation[0] - 0.01 - 0.06
        p.position.y = item_translation[1]
        p.position.z = item_translation[2] + 0.04 + 0.14
        p.orientation = Quaternion(*quaternion_from_euler(0, 1.2, 0))
        arm.set_pose_target(p)
        arm.go(True)

        gripper_goal.command.position = 0
        gripper.send_goal(gripper_goal)
        gripper.wait_for_result(rospy.Duration(2.0))

        scene.removeAttachedObject('item')

        clear_octomap()

        p.position.x = 0.00
        p.position.y = -0.25
        p.position.z = 0.75 - 0.1
        p.orientation = Quaternion(*quaternion_from_euler(0, -1.5, -1.5))
        arm.set_pose_target(p)
        arm.go(True)
        break
