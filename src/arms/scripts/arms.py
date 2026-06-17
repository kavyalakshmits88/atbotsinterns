#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

class ArmControlNode(Node):
    def __init__(self):
        super().__init__('arm_control_node')

        # 1. Subscriber to receive counter data from 'counter_topic'
        self.subscription = self.create_subscription(
            Int32,
            'counter_topic',
            self.counter_callback,
            10)

        # 2. Publisher to send arm joint commands
        self.publisher_ = self.create_publisher(
            JointTrajectory,
            '/arm_controller/joint_trajectory',
            10)

        # Define joint names (modify to match your robot's URDF)
        self.joint_names = [
            'joint_1',  # Base rotation
            'joint_2',  # Shoulder
            'joint_3',  # Elbow
            'joint_4',  # Wrist 1
            'joint_5',  # Wrist 2
            'joint_6'   # Wrist 3 (End effector)
        ]

        self.get_logger().info('Arm Control Node started. Waiting for counter data...')

    def counter_callback(self, msg):
        counter_value = msg.data

        # Create JointTrajectory message
        traj = JointTrajectory()
        traj.joint_names = self.joint_names

        point = JointTrajectoryPoint()

        # -----------------------------------------------
        # ARM MOVEMENT LOGIC based on counter value (0-10)
        # -----------------------------------------------

        if counter_value == 0:
            # HOME position — all joints at 0
            point.positions = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            self.get_logger().info(f'Counter: {counter_value} -> ARM: HOME position')

        elif counter_value == 1:
            # Raise shoulder slightly
            point.positions = [0.0, 0.3, 0.0, 0.0, 0.0, 0.0]
            self.get_logger().info(f'Counter: {counter_value} -> ARM: Raise shoulder')

        elif counter_value == 2:
            # Bend elbow
            point.positions = [0.0, 0.3, 0.5, 0.0, 0.0, 0.0]
            self.get_logger().info(f'Counter: {counter_value} -> ARM: Bend elbow')

        elif counter_value == 3:
            # Rotate base left
            point.positions = [0.5, 0.3, 0.5, 0.0, 0.0, 0.0]
            self.get_logger().info(f'Counter: {counter_value} -> ARM: Rotate base left')

        elif counter_value == 4:
            # Extend arm forward (reach position)
            point.positions = [0.5, 0.6, 0.8, 0.0, 0.0, 0.0]
            self.get_logger().info(f'Counter: {counter_value} -> ARM: Extend arm forward')

        elif counter_value == 5:
            # Tilt wrist down
            point.positions = [0.5, 0.6, 0.8, -0.5, 0.0, 0.0]
            self.get_logger().info(f'Counter: {counter_value} -> ARM: Tilt wrist down')

        elif counter_value == 6:
            # Rotate wrist
            point.positions = [0.5, 0.6, 0.8, -0.5, 0.3, 0.0]
            self.get_logger().info(f'Counter: {counter_value} -> ARM: Rotate wrist')

        elif counter_value == 7:
            # GRAB position — close end effector / lower arm
            point.positions = [0.5, 0.6, 0.8, -0.5, 0.3, 0.5]
            self.get_logger().info(f'Counter: {counter_value} -> ARM: GRAB position')

        elif counter_value == 8:
            # LIFT — raise shoulder while holding
            point.positions = [0.5, 0.9, 0.6, -0.3, 0.3, 0.5]
            self.get_logger().info(f'Counter: {counter_value} -> ARM: LIFT object')

        elif counter_value == 9:
            # CARRY — rotate base to target location
            point.positions = [-0.5, 0.9, 0.6, -0.3, 0.3, 0.5]
            self.get_logger().info(f'Counter: {counter_value} -> ARM: CARRY to target')

        elif counter_value == 10:
            # PLACE — lower arm and release
            point.positions = [-0.5, 0.4, 0.5, -0.2, 0.0, 0.0]
            self.get_logger().info(f'Counter: {counter_value} -> ARM: PLACE object')

        else:
            # Fallback — return to HOME
            point.positions = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            self.get_logger().info(f'Counter: {counter_value} -> ARM: Unknown, return HOME')

        # Zero velocities and accelerations
        point.velocities = [0.0] * len(self.joint_names)
        point.accelerations = [0.0] * len(self.joint_names)

        # Time to reach this position (1 second)
        point.time_from_start = Duration(sec=1, nanosec=0)

        traj.points = [point]

        # Publish the trajectory command
        self.publisher_.publish(traj)


def main(args=None):
    rclpy.init(args=args)
    node = ArmControlNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down...')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
