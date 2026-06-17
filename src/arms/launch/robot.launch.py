#!/usr/bin/env python3
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([

        # Node 1: The Counter Publisher (publishes 0 to 10 in a loop)
        Node(
            package='lidar',
            executable='lidar.py',
            name='counter_publisher_node',
            output='screen'
        ),

        # Node 2: The Wheel/Movement Controller (STOP if counter <= 3, MOVE if > 3)
        Node(
            package='wheels',
            executable='wheels.py',
            name='lidar_control_node',
            output='screen'
        ),

        # Node 3: The Arm Controller (controls 6 joints based on counter 0-10)
        Node(
            package='arms',
            executable='arms.py',
            name='arm_control_node',
            output='screen',
            remappings=[
                # Remap arm trajectory to the correct controller topic
                ('/arm_controller/joint_trajectory', '/arm_controller/joint_trajectory')
            ]
        )

    ])
