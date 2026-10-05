import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')               # node name
        self.publisher_ = self.create_publisher(String, 'topic', 10)  # type, topic name, queue size
        self.timer = self.create_timer(0.5, self.timer_callback)      # call every 0.5 s
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1


def main(args=None):
    rclpy.init(args=args)
    node = MinimalPublisher()
    rclpy.spin(node)        # keep the node running
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()