#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import PoseStamped, Twist
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster
#from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3 # two "Poses" are outputting error
import numpy as np

class MyNodePy(Node):

    def __init__(self):
        super().__init__('control')

        self.pose_sub = self.create_subscription( # subscribes to Pose node
            Pose,
            '/turtle1/pose',
            self.pose_callback,10)
        self.pose_sub  # prevent unused variable warning

        self.goal_sub = self.create_subscription( # subscribes to Goal Pose node
            PoseStamped,
            '/goal_pose',
            self.goal_callback,10)
        self.goal_sub  # prevent unused variable warning

        self.declare_parameter('v',0.0)
        self.declare_parameter('dt',.1)
       
        self.my_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
    def pose_callback(self, in_msg):
        v = self.get_parameter('v').get_parameter_value().double_value
        dt = self.get_parameter('dt').get_parameter_value().double_value

        # set the orienation
        theta = in_msg.theta

        x_pred_f = 0
        y_pred_f = 0
        for w in range(-np.pi,np.pi):
            x_pred = in_msg.x + v*dt*np.cos(theta+(w/2)*dt)
            y_pred = in_msg.y + v*dt*np.sin(theta+(w/2)*dt)

            x_pred_f = min(x_pred_f, x_pred)
            y_pred_f = min(y_pred_f, y_pred)
        
        twist = Twist()
        
        twist.linear.x = 2.0

        self.my_publisher.publish(twist)
                
    def goal_callback(self, in_msg): # just save the goal values for the pose
        # for debugging, use get_logger().info('msg')
        self.px = in_msg.pose.position.x        
        self.py = in_msg.pose.position.x 

        self.qz = in_msg.pose.orientation.z
        self.qw = in_msg.pose.orientation.w

            
            
def main(args=None):
    rclpy.init(args=args)
    my_node_py = MyNodePy()
    rclpy.spin(my_node_py)
    simulation.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
