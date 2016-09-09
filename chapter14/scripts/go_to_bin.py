#!/usr/bin/env python

import sys

import rospy

import actionlib
from geometry_msgs.msg import Quaternion
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler
from std_srvs.srv import Empty
from look_at_bin import look_at_bin


if __name__ == '__main__':
    rospy.init_node('go_to_bin')
    rospy.wait_for_service('/move_base/clear_costmaps')
    rospy.ServiceProxy('/move_base/clear_costmaps', Empty)()
    args = rospy.myargv(argv=sys.argv)
    if len(args) != 2:
        print('Usage: go_to_bin.py BIN_NUMBER')
        sys.exit(1)
    bin_number = int(args[1])
    move_base = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    move_base.wait_for_server()
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.pose.position.x = 0.5 * (bin_number % 6) - 1.5
    goal.target_pose.pose.position.y = 1.1 * (bin_number / 6) - 0.55
    if bin_number >= 6:
        yaw = 1.57
    else:
        yaw = -1.57
    orient = Quaternion(*quaternion_from_euler(0, 0, yaw))
    goal.target_pose.pose.orientation = orient
    move_base.send_goal(goal)
    move_base.wait_for_result()
    look_at_bin()
