import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration


class JointPublisher(Node):

    def __init__(self):
        super().__init__('joint_publisher')

        # Topic = controller name from the YAML + /joint_trajectory
        self.publisher_ = self.create_publisher(
            JointTrajectory, '/joint_trajectory_controller/joint_trajectory', 10)

        # Same joints, same names, as in the YAML
        self.joints = [
            'body_to_shoulder_right',
            'body_to_shoulder_left',
            'shoulder_to_arm_upper_right',
            'shoulder_to_arm_upper_left',
            'arm_upper_to_lower_right',
            'arm_upper_to_lower_left',
        ]

        # Target angles (radians), one value per joint, in the order above
        self.poses = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],      # arms hanging down
            [-1.0, -1.0, 0.5, 0.5, 1.2, 1.2],    # arms forward, slightly out, elbows bent
        ]
        self.index = 0

        self.timer = self.create_timer(3.0, self.timer_callback)  # every 3 s

    def timer_callback(self):
        msg = JointTrajectory()
        msg.joint_names = self.joints

        point = JointTrajectoryPoint()
        point.positions = self.poses[self.index]
        point.time_from_start = Duration(sec=2)   # reach this pose within 2 s

        msg.points = [point]
        self.publisher_.publish(msg)
        self.get_logger().info(f'Sent pose {self.index}: {point.positions}')

        self.index = (self.index + 1) % len(self.poses)  # alternate 0, 1, 0, 1...


def main(args=None):
    rclpy.init(args=args)
    node = JointPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()