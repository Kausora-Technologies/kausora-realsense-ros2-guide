# RealSense ROS2 Setup

Set up and verify the `realsense2_camera` ROS2 wrapper.

---

## Install RealSense ROS2 Packages

### Automated

```bash
chmod +x scripts/install_ros2_deps.sh
./scripts/install_ros2_deps.sh
```

### Manual

```bash
sudo apt-get update
sudo apt-get install -y \
    ros-jazzy-realsense2-camera \
    ros-jazzy-realsense2-description \
    ros-jazzy-rviz2
```

---

## Build the Kausora Package

```bash
cd ~/kausora_ws

# Install package dependencies
rosdep install --from-paths src --ignore-src -r -y

# Build
colcon build --packages-select kausora_realsense_ros2 \
    --cmake-args -DCMAKE_BUILD_TYPE=Release

# Source the workspace
source install/setup.bash
```

---

## Launch a Camera

Connect your RealSense camera, then launch the appropriate file:

```bash
# D435
ros2 launch kausora_realsense_ros2 d435.launch.py

# D435i with IMU
ros2 launch kausora_realsense_ros2 d435i.launch.py

# D455 (long range)
ros2 launch kausora_realsense_ros2 d455.launch.py

# L515 (LiDAR)
ros2 launch kausora_realsense_ros2 l515.launch.py

# T265 (tracking)
ros2 launch kausora_realsense_ros2 t265.launch.py

# Specify serial number (for multi-camera setups)
ros2 launch kausora_realsense_ros2 d435.launch.py serial_no:=123456789012
```

---

## Verify Topics

With the node running, check active topics:

```bash
ros2 topic list
```

Expected topics for a D435 (`/camera/d435/`):

```
/camera/d435/color/image_raw
/camera/d435/color/camera_info
/camera/d435/depth/image_rect_raw
/camera/d435/depth/camera_info
/camera/d435/extrinsics/depth_to_color
```

Additional topics for D435i (IMU):

```
/camera/d435i/imu
/camera/d435i/gyro/sample
/camera/d435i/accel/sample
```

T265 topics:

```
/camera/t265/odom/sample
/camera/t265/fisheye1/image_raw
/camera/t265/fisheye2/image_raw
/camera/t265/imu
```

---

## View in RViz2

Each launch file includes a `launch_rviz` argument that opens RViz2 with a
pre-configured display layout — no manual setup required.

```bash
# Launch camera + RViz2 together
ros2 launch kausora_realsense_ros2 d435.launch.py launch_rviz:=true

# Works for all supported cameras
ros2 launch kausora_realsense_ros2 d415.launch.py launch_rviz:=true
ros2 launch kausora_realsense_ros2 d435i.launch.py launch_rviz:=true
ros2 launch kausora_realsense_ros2 d455.launch.py launch_rviz:=true
ros2 launch kausora_realsense_ros2 l515.launch.py launch_rviz:=true
ros2 launch kausora_realsense_ros2 t265.launch.py launch_rviz:=true
```

Pre-configured displays per camera:

| Camera | Fixed Frame | Displays |
|--------|-------------|----------|
| D415 / D435 / D455 / L515 | `camera_link` | Grid, TF, Color Image, Depth Image, PointCloud2 (disabled) |
| D435i | `camera_link` | Grid, TF, Color Image, Depth Image, PointCloud2 (disabled), IMU |
| T265 | `t265_pose_frame` | Grid, TF, Odometry, Fisheye 1, Fisheye 2 |

The `launch_rviz` argument defaults to `false`, so existing launch commands are
unaffected.

---

## View Camera Image (Quick)

```bash
# View color stream
ros2 run image_view image_view --ros-args -r image:=/camera/d435/color/image_raw

# View depth stream
ros2 run image_view image_view --ros-args -r image:=/camera/d435/depth/image_rect_raw
```

---

## Run Verification Script

```bash
python3 scripts/verify_setup.py
```

---

## Next Steps

- [Docker Setup →](./05-docker-setup.md)
- [Camera Configs →](./06-camera-configs.md)
