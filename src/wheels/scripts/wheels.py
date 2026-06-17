#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist

class LidarControlNode(Node):
    def __init__(self):
        super().__init__('lidar_subscriber_node')
        
        # 1. Subscriber to receive counter data from 'counter_topic'
        self.subscription = self.create_subscription(
            Int32,
            'counter_topic',
            self.counter_callback,
            10)
            
        # 2. Publisher to send movement commands
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        
        self.get_logger().info('Lidar Subscriber Node started. Waiting for counter data...')

    def counter_callback(self, msg):
        counter_value = msg.data
        
        # Create the Twist message (velocity command)
        cmd = Twist()

        # LOGIC:
        # If counter value is 3 or less -> STOP (0.0)
        # If counter value is greater than 3 -> MOVE (0.5)
        if counter_value <= 3:
            cmd.linear.x = 0.0
            self.get_logger().info(f'Counter: {counter_value} -> COMMAND: STOP')
        else:
            cmd.linear.x = 0.5  # Constant forward speed
            self.get_logger().info(f'Counter: {counter_value} -> COMMAND: MOVE')

        # Publish the command to the robot
        self.publisher_.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = LidarControlNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down...')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
