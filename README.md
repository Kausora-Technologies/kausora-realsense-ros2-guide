# Kausora RealSense ROS2 Guide

[![Build](https://github.com/Kausora-Technologies/kausora-realsense-ros2-guide/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/Kausora-Technologies/kausora-realsense-ros2-guide/actions/workflows/build.yml)
[![Lint](https://github.com/Kausora-Technologies/kausora-realsense-ros2-guide/actions/workflows/lint.yml/badge.svg?branch=main)](https://github.com/Kausora-Technologies/kausora-realsense-ros2-guide/actions/workflows/lint.yml)
[![Docker](https://github.com/Kausora-Technologies/kausora-realsense-ros2-guide/actions/workflows/docker.yml/badge.svg?branch=main)](https://github.com/Kausora-Technologies/kausora-realsense-ros2-guide/actions/workflows/docker.yml)

**Intel RealSense + ROS2 Jazzy — Complete Integration Package**

Provided by [Kausora Technologies](https://kausora.com)

---

This repository provides a production-ready ROS2 Jazzy package with pre-configured launch files, YAML parameter configs, Docker support, and step-by-step documentation for integrating Intel RealSense cameras into your ROS2 robotics stack.

## Supported Cameras

| Camera | Depth | Color | IMU | Fisheye | Notes |
|--------|-------|-------|-----|---------|-------|
| **D415** | Yes | Yes | No | No | Wide-angle, indoor 3D reconstruction |
| **D435** | Yes | Yes | No | No | Global shutter, fast-moving objects |
| **D435i** | Yes | Yes | Yes | No | D435 + BMI055 IMU for SLAM/VIO |
| **D455** | Yes | Yes | Yes | No | Long-range (up to 6m), outdoor use; BMI085 IMU |
| **L515** | Yes (LiDAR) | Yes | No | No | High-accuracy indoor LiDAR depth |
| **T265** | No | No | Yes | Yes | 6-DoF VIO tracking, pose estimation |

---

## Quick Start

### Option A — Docker (Recommended)

No host installation required beyond Docker.

```bash
# 1. Clone the repository
git clone https://github.com/Kausora-Technologies/kausora-realsense-ros2-guide.git
cd kausora-realsense-ros2-guide

# 2. Configure environment
cp docker/.env.example docker/.env
# Edit docker/.env: set CAMERA_MODEL and optionally CAMERA_SERIAL

# 3. Build and run (compose file lives in docker/)
cd docker
docker compose build realsense
docker compose up realsense
```

Topics will be available on the host via `network_mode: host`.

### Option B — Native Installation

```bash
# 1. Install librealsense2 SDK
chmod +x scripts/install_sdk.sh
./scripts/install_sdk.sh

# 2. Install ROS2 Jazzy realsense packages
chmod +x scripts/install_ros2_deps.sh
./scripts/install_ros2_deps.sh

# 3. Build this package
cd ~/kausora_ws
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --packages-select kausora_realsense_ros2
source install/setup.bash

# 4. Launch your camera
ros2 launch kausora_realsense_ros2 d435.launch.py
```

### Verify Setup

```bash
python3 scripts/verify_setup.py
```

---

## Launch Files

| Launch File | Camera | Command |
|-------------|--------|---------|
| `d415.launch.py` | D415 | `ros2 launch kausora_realsense_ros2 d415.launch.py` |
| `d435.launch.py` | D435 | `ros2 launch kausora_realsense_ros2 d435.launch.py` |
| `d435i.launch.py` | D435i | `ros2 launch kausora_realsense_ros2 d435i.launch.py` |
| `d455.launch.py` | D455 | `ros2 launch kausora_realsense_ros2 d455.launch.py` |
| `l515.launch.py` | L515 | `ros2 launch kausora_realsense_ros2 l515.launch.py` |
| `t265.launch.py` | T265 | `ros2 launch kausora_realsense_ros2 t265.launch.py` |
| `multi_camera.launch.py` | Any × 2 | `ros2 launch kausora_realsense_ros2 multi_camera.launch.py` |

### Common Launch Arguments

```bash
# Launch camera + RViz2 with pre-configured displays (one command)
ros2 launch kausora_realsense_ros2 d435.launch.py launch_rviz:=true

# Specify camera serial number
ros2 launch kausora_realsense_ros2 d435.launch.py serial_no:=123456789012

# Enable pointcloud
ros2 launch kausora_realsense_ros2 d435.launch.py enable_pointcloud:=true

# Align depth to color
ros2 launch kausora_realsense_ros2 d435.launch.py align_depth.enable:=true

# Multi-camera with specific serials
ros2 launch kausora_realsense_ros2 multi_camera.launch.py \
    camera1_serial:=111111111 \
    camera2_serial:=222222222
```

---

## Key Topics

### Depth Cameras (D415 / D435 / D435i / D455 / L515)

```
/camera/<name>/color/image_raw          sensor_msgs/Image
/camera/<name>/color/camera_info        sensor_msgs/CameraInfo
/camera/<name>/depth/image_rect_raw     sensor_msgs/Image
/camera/<name>/depth/camera_info        sensor_msgs/CameraInfo
/camera/<name>/depth/color/points       sensor_msgs/PointCloud2  (if enabled)
```

### IMU (D435i / D455)

```
/camera/d435i/imu                       sensor_msgs/Imu  (fused, if unite_imu_method set)
/camera/d435i/gyro/sample               sensor_msgs/Imu
/camera/d435i/accel/sample              sensor_msgs/Imu

/camera/d455/gyro/sample                sensor_msgs/Imu  (if enable_gyro: true)
/camera/d455/accel/sample               sensor_msgs/Imu  (if enable_accel: true)
```

### Tracking (T265)

```
/camera/t265/odom/sample                nav_msgs/Odometry
/camera/t265/fisheye1/image_raw         sensor_msgs/Image
/camera/t265/fisheye2/image_raw         sensor_msgs/Image
/camera/t265/imu                        sensor_msgs/Imu
```

---

## Documentation

| Guide | Description |
|-------|-------------|
| [01 — Prerequisites](docs/01-prerequisites.md) | Hardware, OS, and USB requirements |
| [02 — SDK Installation](docs/02-sdk-installation.md) | Install librealsense2 on Ubuntu 24.04 |
| [03 — ROS2 Installation](docs/03-ros2-installation.md) | Install ROS2 Jazzy |
| [04 — RealSense ROS2 Setup](docs/04-realsense-ros2-setup.md) | Build and verify the ROS2 wrapper |
| [05 — Docker Setup](docs/05-docker-setup.md) | Docker workflow guide |
| [06 — Camera Configs](docs/06-camera-configs.md) | Per-camera parameter reference |
| [07 — Troubleshooting](docs/07-troubleshooting.md) | Common errors and fixes |

---

## Repository Structure

```
kausora-realsense-ros2-guide/
├── package.xml                 # ROS2 package metadata
├── CMakeLists.txt              # ament_cmake build config
├── launch/                     # Per-camera launch files
├── config/                     # Per-camera YAML parameter files
├── rviz/                       # Pre-configured RViz2 display layouts
├── docker/                     # Dockerfile, Compose, .env template
├── scripts/                    # Install and verification scripts
├── docs/                       # Step-by-step documentation
└── .github/workflows/          # CI workflow (GitHub Actions)
```

---

## Requirements

- **OS:** Ubuntu 24.04 LTS
- **ROS2:** Jazzy Jalisco
- **librealsense:** >= 2.56.1
- **realsense-ros:** ros-jazzy-realsense2-camera (v4.56.1+)
- **USB:** 3.0+ (3.2 recommended for L515)

---

## Support

- **Documentation:** See the `docs/` directory
- **Issues:** [GitHub Issues](https://github.com/Kausora-Technologies/kausora-realsense-ros2-guide/issues)
- **Email:** support@kausora.com
- **Website:** [kausora.com](https://kausora.com)

---

## License

Apache License 2.0 — see [LICENSE](LICENSE) for details.

© 2024 Kausora Technologies
