import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_msgs.msg import Int32
import cv2

class ArucoDetector(Node):
    def __init__(self):
        super().__init__('aruco_detector')

        self.bridge = CvBridge()

        self.subscription = self.create_subscription(
            Image,
            '/r1_mini/camera/image_raw',
            self.image_callback,
            10
        )

        self.publisher = self.create_publisher(Int32, '/aruco_id', 10)

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        parameters = cv2.aruco.DetectorParameters_create()

        corners, ids, _ = cv2.aruco.detectMarkers(frame, aruco_dict, parameters=parameters)

        if ids is not None:
            for marker_id in ids.flatten():
                msg_out = Int32()
                msg_out.data = int(marker_id)
                self.publisher.publish(msg_out)
                self.get_logger().info(f"Detected marker: {marker_id}")

        cv2.imshow("camera", frame)
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    node = ArucoDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()