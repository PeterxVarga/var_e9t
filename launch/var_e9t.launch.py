"""Launch both nodes of the var_e9t package."""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """Start the LiDAR simulator and safety monitor."""
    return LaunchDescription([
        Node(
            package='var_e9t',
            executable='lidar_simulator',
            name='lidar_simulator',
            output='screen',
        ),
        Node(
            package='var_e9t',
            executable='safety_monitor',
            name='safety_monitor',
            output='screen',
        ),
    ])
