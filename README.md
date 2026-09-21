# `var_e9t`

ROS 2 Python package for the AJR small assignment.

[![ROS 2 Humble](https://img.shields.io/badge/ROS_2-Humble-34aec5)](https://docs.ros.org/en/humble/)

## Build

It is assumed that the workspace is `~/ros2_ws/`.

```bash
cd ~/ros2_ws/src
git clone https://github.com/PeterxVarga/var_e9t.git
cd ~/ros2_ws
colcon build --packages-select var_e9t --symlink-install
source install/setup.bash
```
