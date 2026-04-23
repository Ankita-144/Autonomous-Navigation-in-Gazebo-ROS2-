import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import time


class DecisionNode(Node):
    def __init__(self):
        super().__init__('decision_node')

        self.create_subscription(Int32, '/aruco_id', self.aruco_callback, 10)
        self.create_subscription(LaserScan, '/r1_mini/lidar', self.lidar_callback, 10)

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.latest_marker = None
        self.last_marker_time = time.time()

    # ========================
    # ARUCO CALLBACK
    # ========================
    def aruco_callback(self, msg):
        self.latest_marker = msg.data
        self.last_marker_time = time.time()

    # ========================
    # MAIN LOOP (LIDAR + ARUCO)
    # ========================
    def lidar_callback(self, msg):
        cmd = Twist()

        # PRIORITY: ARUCO (2 sec override)
        if time.time() - self.last_marker_time < 2.0:
            self.handle_marker(cmd)
        else:
            self.lidar_navigation(msg, cmd)

        self.cmd_pub.publish(cmd)

    # ========================
    # ARUCO CONTROL
    # ========================
    def handle_marker(self, cmd):
        if self.latest_marker == 0:
            # LEFT
            cmd.linear.x = 0.1
            cmd.angular.z = 0.3

        elif self.latest_marker == 1:
            # RIGHT
            cmd.linear.x = 0.1
            cmd.angular.z = -0.3

        elif self.latest_marker == 2:
            # FORWARD
            cmd.linear.x = 0.15
            cmd.angular.z = 0.0

        elif self.latest_marker == 3:
            # STOP
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0

        self.get_logger().info(f"Marker: {self.latest_marker}")

    # ========================
    # LIDAR NAVIGATION
    # ========================
    def lidar_navigation(self, msg, cmd):
        ranges = msg.ranges

        # Clean invalid values
        ranges = [r if r > 0.0 else 10.0 for r in ranges]

        front = min(ranges[0:10] + ranges[-10:])
        left = min(ranges[80:100])
        right = min(ranges[260:280])

        # OBSTACLE AHEAD
        if front < 0.6:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.3

        # TOO CLOSE LEFT → move right
        elif left < 0.4:
            cmd.linear.x = 0.1
            cmd.angular.z = -0.2

        # TOO CLOSE RIGHT → move left
        elif right < 0.4:
            cmd.linear.x = 0.1
            cmd.angular.z = 0.2

        # CLEAR PATH
        else:
            cmd.linear.x = 0.15
            cmd.angular.z = 0.0


def main(args=None):
    rclpy.init(args=args)
    node = DecisionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()