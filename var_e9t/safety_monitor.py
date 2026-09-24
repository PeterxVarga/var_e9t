"""Monitor LiDAR sectors and publish a simple safety status."""

import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String


class SafetyMonitor(Node):
    """Classify the nearest valid LiDAR measurement by sector."""

    STOP_DISTANCE = 1.0
    WARNING_DISTANCE = 2.0

    def __init__(self):
        """Initialize the subscriber and status publisher."""
        super().__init__('safety_monitor')
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10,
        )
        self.publisher = self.create_publisher(String, 'safety_status', 10)

    @staticmethod
    def sector_for_angle(angle):
        """Return the sector name for an angle in radians."""
        degrees = math.degrees(angle)

        if -45.0 <= degrees < 45.0:
            return 'FRONT'
        if 45.0 <= degrees < 135.0:
            return 'LEFT'
        if -135.0 <= degrees < -45.0:
            return 'RIGHT'
        return 'REAR'

    def classify_distance(self, distance):
        """Return the safety state for the nearest distance."""
        if distance < self.STOP_DISTANCE:
            return 'STOP'
        if distance < self.WARNING_DISTANCE:
            return 'WARNING'
        return 'SAFE'

    def scan_callback(self, msg):
        """Process a LaserScan and publish the nearest obstacle status."""
        nearest = {
            'FRONT': math.inf,
            'LEFT': math.inf,
            'RIGHT': math.inf,
            'REAR': math.inf,
        }

        for index, distance in enumerate(msg.ranges):
            if not math.isfinite(distance):
                continue
            if distance < msg.range_min or distance > msg.range_max:
                continue

            angle = msg.angle_min + index * msg.angle_increment
            sector = self.sector_for_angle(angle)
            nearest[sector] = min(nearest[sector], distance)

        sector, distance = min(
            nearest.items(),
            key=lambda item: item[1],
        )

        status = String()
        if math.isinf(distance):
            status.data = 'SAFE | NO OBSTACLE'
        else:
            state = self.classify_distance(distance)
            status.data = f'{state} | {sector} | {distance:.2f} m'

        self.publisher.publish(status)


def main(args=None):
    """Run the safety monitor node."""
    rclpy.init(args=args)
    node = SafetyMonitor()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
