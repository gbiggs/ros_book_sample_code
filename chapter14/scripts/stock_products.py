#!/usr/bin/env python

import rospy
import tf

from gazebo_msgs.srv import DeleteModel, SpawnModel
from geometry_msgs.msg import Point, Pose, Quaternion


if __name__ == '__main__':
    rospy.init_node("stock_products")
    rospy.wait_for_service("gazebo/delete_model")
    rospy.wait_for_service("gazebo/spawn_sdf_model")
    delete_model = rospy.ServiceProxy("gazebo/delete_model", DeleteModel)
    s = rospy.ServiceProxy("gazebo/spawn_sdf_model", SpawnModel)
    orient = Quaternion(*tf.transformations.quaternion_from_euler(0, 0, 0))
    with open("models/product_0/model.sdf", "r") as f:
        product_xml = f.read()
    for product_num in xrange(0, 12):
        item_name = "product_{0}_0".format(product_num)
        delete_model(item_name)
    for product_num in xrange(0, 12):
        bin_y = 2.8 * (product_num / 6) - 1.4
        bin_x = 0.5 * (product_num % 6) - 1.5
        item_name = "product_{0}_0".format(product_num)
        item_pose = Pose(Point(x=bin_x, y=bin_y, z=2), orient)
        s(item_name, product_xml, "", item_pose, "world")
