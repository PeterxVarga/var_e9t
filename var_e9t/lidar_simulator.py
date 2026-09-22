"""Simulate a 360-degree LiDAR scan with one moving obstacle."""

import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class LidarSimulator(Node):
    """Publish simulated LaserScan messages."""

    NUM_BEAMS = 360
    RANGE_MIN = 0.1
    RANGE_MAX = 8.0
    PUBLISH_PERIOD = 0.2
    ANGULAR_SPEED = math.radians(15.0)
    OBSTACLE_HALF_WIDTH = 4

    def __init__(self):
        """Initialize the ROS 2 publisher and timer."""
        super().__init__('lidar_simulator')
        self.publisher = self.create_publisher(LaserScan, 'scan', 10)
        self.start_time = self.get_clock().now()
        self.timer = self.create_timer(
            self.PUBLISH_PERIOD,
            self.publish_scan,
        )

    def publish_scan(self):
        """Publish the current simulated scan."""
        now = self.get_clock().now()
        elapsed = (now - self.start_time).nanoseconds / 1e9

        angle_increment = 2.0 * math.pi / self.NUM_BEAMS
        obstacle_angle = (self.ANGULAR_SPEED * elapsed + math.pi) % (
            2.0 * math.pi
        ) - math.pi
        obstacle_distance = 2.05 + 1.45 * math.sin(0.7 * elapsed)

        ranges = [math.inf] * self.NUM_BEAMS
        center_index = round(
            (obstacle_angle + math.pi) / angle_increment
        ) % self.NUM_BEAMS

        for offset in range(
            -self.OBSTACLE_HALF_WIDTH,
            self.OBSTACLE_HALF_WIDTH + 1,
        ):
            beam_index = (center_index + offset) % self.NUM_BEAMS
            ranges[beam_index] = (
                obstacle_distance + 0.02 * abs(offset)
            )

        scan = LaserScan()
        scan.header.stamp = now.to_msg()
        scan.header.frame_id = 'laser'
        scan.angle_min = -math.pi
        scan.angle_increment = angle_increment
        scan.angle_max = scan.angle_min + (
            self.NUM_BEAMS - 1
        ) * angle_increment
        scan.time_increment = 0.0
        scan.scan_time = self.PUBLISH_PERIOD
        scan.range_min = self.RANGE_MIN
        scan.range_max = self.RANGE_MAX
        scan.ranges = ranges

        self.publisher.publish(scan)


def main(args=None):
    """Run the LiDAR simulator node."""
    rclpy.init(args=args)
    node = LidarSimulator()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
