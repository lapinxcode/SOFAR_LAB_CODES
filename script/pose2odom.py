#!/usr/bin/env python3

# colcon build --symlink-install so u dont have to build it every time u change the code
# ~/ros2$ chmod +x pose2odom.py to make it executable
# ~/ros2$ source install/setup.bash

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
import numpy as np

from turtlesim.msg import Pose

class Pose2Odometry(Node):

    def __init__(self):
        super().__init__('pose2odom')
        
        self.my_subscription = self.create_subscription( # subscribes to Pose node
            Pose,
            '/turtle1/pose',
            self.odometry_callback,10)
        self.my_subscription  # prevent unused variable warning
       
        self.my_publisher = self.create_publisher(Odometry, 'odometry', 10)
        
    def odometry_callback(self, in_msg): # returns odometry??
        odom = Odometry()
        odom.header.stamp = self.get_clock().now().to_msg() 
        odom.header.frame_id = "/odom"

        # set the position
        odom.pose.pose.position.x = in_msg.x
        odom.pose.pose.position.y = in_msg.y
        l = np.sqrt(in_msg.linear_velocity**2 + in_msg.angular_velocity**2)
        
        odom.pose.pose.orientation.w = in_msg.linear_velocity/l
        odom.pose.pose.orientation.x = 0.0
        odom.pose.pose.orientation.y = 0.0
        odom.pose.pose.orientation.z = in_msg.angular_velocity/l
        
                
        self.my_publisher.publish(odom)

            
            
def main(args=None):
    rclpy.init(args=args)

    pose_odom_node = Pose2Odometry()

    rclpy.spin(pose_odom_node)

    pose_odom_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
