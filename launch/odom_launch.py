from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # turtlesim pkg
        Node(
            package='turtlesim',
            #namespace='turtlesim1', -> doesnt work
            executable='turtlesim_node',
            name='sim',
            remappings = [('/turtle1/color_sensor', 'color')],
            parameters = [{'background_r': 50},
                            {'background_g': 100},
                            {'background_b': 69}
                        ]
        ),    

        # conversion node (pkg created in lab)

        # Turtle 1
        Node(
            name = 'odom_1',
            package='sofar_lab',
            executable='../script/pose2odom.py'
        ),

        # Turtle 2
        # sometimes I need to run colcon build --symlink-install to make it work

        Node(
            name = 'odom_2',
            package='sofar_lab',
            executable='../script/pose2odom.py',
            remappings = [('/turtle1/pose', '/turtle2/pose'),
                          ('/odometry', '/odometry2')]

        ),

        # rviz config
        Node( # by default it opens the last rviz config
              # change this to open the right config file 
            package='rviz2',
            namespace='',
            executable='rviz2',
            name='rviz2',
        ),

        Node( 
            package = "tf2_ros", 
            executable = "static_transform_publisher",
            arguments = ["5.5", "5.5", "0", "0", "0", "0", "odom", "map"]) # maybe quaternion
    
    ])

# tf2 - ros2 run tf2_ros static_transform_publisher 5.5 5.5 0 0 0 0 foo bar