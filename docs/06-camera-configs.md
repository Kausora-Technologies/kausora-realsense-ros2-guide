# Camera Configuration Reference

Parameter reference for each supported RealSense camera model.

---

## Using Config Files

Config files are located in `config/`. They are reference files documenting every tunable
parameter for each camera. Launch files use default parameters inline; pass a config file
directly to override them:

```bash
# Launch with built-in defaults (recommended)
ros2 launch kausora_realsense_ros2 d435.launch.py

# Override with a custom config file
ros2 run realsense2_camera realsense2_camera_node \
    --ros-args --params-file config/d435_config.yaml
```

---

## D415 — Wide-angle Stereo

**Use case:** Indoor 3D reconstruction, structured environments

| Parameter | Default | Notes |
|-----------|---------|-------|
| `color_width` | 1280 | Up to 1920 |
| `color_height` | 720 | Up to 1080 |
| `color_fps` | 30 | Up to 30 |
| `depth_width` | 1280 | Up to 1280 |
| `depth_height` | 720 | Up to 720 |
| `depth_fps` | 30 | Up to 90 (at lower res) |
| `enable_gyro` | false | Not available |
| `enable_accel` | false | Not available |

---

## D435 — Global Shutter Stereo

**Use case:** Dynamic scenes, robotic arms, fast-moving objects

| Parameter | Default | Notes |
|-----------|---------|-------|
| `color_width` | 848 | Up to 1920 |
| `color_height` | 480 | Up to 1080 |
| `color_fps` | 30 | Up to 30 |
| `depth_width` | 848 | Up to 1280 |
| `depth_height` | 480 | Up to 720 |
| `depth_fps` | 30 | Up to 90 |
| `enable_gyro` | false | Not available |
| `enable_accel` | false | Not available |

---

## D435i — Stereo + IMU

**Use case:** VIO, SLAM, autonomous robots

| Parameter | Default | Notes |
|-----------|---------|-------|
| `color_width` | 848 | Up to 1920 |
| `depth_width` | 848 | Up to 1280 |
| `enable_gyro` | true | 200 Hz |
| `enable_accel` | true | 63 Hz |
| `gyro_fps` | 200.0 | 200 or 400 Hz |
| `accel_fps` | 63.0 | 63 or 250 Hz |
| `unite_imu_method` | `linear_interpolation` | `""`, `copy`, `linear_interpolation` |

### IMU Topic
Published to `/camera/d435i/imu` (if `unite_imu_method` is set).
Raw streams: `/camera/d435i/gyro/sample`, `/camera/d435i/accel/sample`

---

## D455 — Long-range Stereo + IMU

**Use case:** Outdoor/long-range depth, vehicles, warehouses

| Parameter | Default | Notes |
|-----------|---------|-------|
| `color_width` | 1280 | Up to 1280 |
| `color_height` | 720 | Up to 800 |
| `color_fps` | 30 | Up to 30 |
| `depth_width` | 1280 | Up to 1280 |
| `depth_height` | 720 | Up to 720 |
| `depth_fps` | 30 | Up to 90 |
| `enable_gyro` | false | Available (BMI085) — enable for VIO/SLAM |
| `enable_accel` | false | Available (BMI085) — enable for VIO/SLAM |
| `gyro_fps` | 400.0 | 400 Hz |
| `accel_fps` | 250.0 | 250 Hz |
| `unite_imu_method` | `""` | `""`, `copy`, `linear_interpolation` |

**Range:** 0.6m – 6m (optimal), up to 20m (reduced accuracy)

---

## L515 — LiDAR Depth

**Use case:** High-accuracy indoor mapping, people tracking

| Parameter | Default | Notes |
|-----------|---------|-------|
| `color_width` | 1920 | |
| `color_height` | 1080 | |
| `color_fps` | 30 | |
| `depth_width` | 1024 | |
| `depth_height` | 768 | |
| `depth_fps` | 30 | Up to 30 |
| `enable_gyro` | false | Not available |
| `enable_accel` | false | Not available |

**Range:** 0.25m – 9m indoors

---

## T265 — Visual-Inertial Tracking

**Use case:** 6-DoF pose estimation, loop closure, mapping

| Parameter | Default | Notes |
|-----------|---------|-------|
| `enable_pose` | true | 200 Hz 6-DoF pose |
| `enable_fisheye1` | true | 848×800 @ 30fps |
| `enable_fisheye2` | true | 848×800 @ 30fps |
| `enable_gyro` | true | 200 Hz |
| `enable_accel` | true | 62.5 Hz |
| `unite_imu_method` | `linear_interpolation` | |
| `odom_frame_id` | `odom` | Odometry frame |

**Pose topic:** `/camera/t265/odom/sample` (type: `nav_msgs/Odometry`)

---

## Common Parameters (All Cameras)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `camera_name` | model-specific | Node and TF prefix (e.g. `d435`, `d435i`) |
| `camera_namespace` | `camera` | ROS namespace |
| `serial_no` | `""` | Camera serial (empty = first found) |
| `pointcloud.enable` | `false` | Publish PointCloud2 |
| `align_depth.enable` | `false` | Align depth to color frame |
| `clip_distance` | `-1.0` | Max depth distance in meters (-1.0 = disable) |
| `publish_tf` | `true` | Publish TF transforms |
| `initial_reset` | `false` | Hardware reset on startup |

---

## Next Steps

- [Troubleshooting →](./07-troubleshooting.md)
