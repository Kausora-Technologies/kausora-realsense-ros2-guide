# Troubleshooting

Common errors and solutions for RealSense + ROS2 Jazzy integration.

---

## Camera Detection Issues

### Camera not detected by `rs-enumerate-devices`

**Symptom:** Command returns nothing or hangs.

**Solutions:**
```bash
# 1. Check USB connection
lsusb | grep -i intel

# 2. Try a different USB port (ensure USB 3.0)
# 3. Reload udev rules
sudo udevadm control --reload-rules
sudo udevadm trigger
# Then unplug and replug the camera

# 4. Check dmesg for errors
dmesg | tail -30 | grep -i usb
```

### LIBUSB_ERROR_ACCESS

**Symptom:** `Failed to get device list. (LIBUSB_ERROR_ACCESS)`

**Solution:**
```bash
# Install udev rules
sudo apt-get install -y librealsense2-udev-rules
sudo udevadm control --reload-rules
sudo udevadm trigger

# Add user to plugdev group
sudo usermod -aG plugdev $USER
# Log out and back in
```

---

## ROS2 Node Issues

### Node starts but no topics published

**Symptom:** Node launches but `ros2 topic list` shows no camera topics.

**Solutions:**
```bash
# Launch in foreground — errors appear immediately in the terminal
ros2 launch kausora_realsense_ros2 d435.launch.py

# In a second terminal, inspect logs
ros2 run rqt_console rqt_console
# Or tail the latest launch log directly:
tail -f ~/.ros/log/$(ls -t ~/.ros/log | head -1)/launch.log

# Verify camera is detected before launching ROS2
rs-enumerate-devices

# Try with explicit serial number (single camera attached)
ros2 launch kausora_realsense_ros2 d435.launch.py \
    serial_no:=$(rs-enumerate-devices | grep Serial | head -1 | awk '{print $NF}')
```

### "No devices found" in ROS2 node

**Symptom:** `[realsense2_camera_node]: No device found.`

**Solutions:**
- Camera is not connected or not detected (see camera detection above)
- Wrong serial number specified in launch args
- Camera is in use by another process:
  ```bash
  # Find processes using the RealSense library
  ps aux | grep -E 'realsense|rs-' | grep -v grep

  # Find any process with librealsense open
  lsof | grep librealsense
  ```

### TF transform errors

**Symptom:** `Could not find transform from X to Y`

```bash
# Check active TF frames
ros2 run tf2_tools view_frames

# Check a specific transform — frame names are prefixed by camera_name.
# With the default camera_name=d435:
ros2 run tf2_ros tf2_echo camera_d435_link camera_d435_color_optical_frame

# Substitute your camera model, e.g. for d455:
ros2 run tf2_ros tf2_echo camera_d455_link camera_d455_color_optical_frame
```

Ensure `publish_tf: true` in your config and that `camera_name` matches the frame prefix.

---

## IMU Issues (D435i / D455 / T265)

### IMU data not published

**Symptom:** `/camera/<name>/imu` topic missing (e.g. `/camera/d435i/imu` or `/camera/d455/imu`).

**Check the relevant config file (`d435i_config.yaml` or `d455_config.yaml`):**
```yaml
enable_gyro: true
enable_accel: true
unite_imu_method: "linear_interpolation"  # Must not be empty string for fused /imu topic
```

Without `unite_imu_method` set you get `/gyro/sample` and `/accel/sample` individually but no fused `/imu` topic.

> **T265:** The T265 IMU is always active — it cannot be disabled. If its IMU topic
> (`/camera/t265/imu`) is missing, the issue is with the node itself, not a config flag.
> See [T265 Tracking Issues](#t265-tracking-issues) below.

### IMU noise / drift

- Ensure camera is stationary for 2–3 seconds after launch for IMU initialization
- Verify `unite_imu_method` is `linear_interpolation` for fused IMU data

---

## T265 Tracking Issues

### Pose / odometry not publishing

**Symptom:** `/camera/t265/odom/sample` topic exists but no messages arrive,
or node logs `TRACKING_STATE = FAILED`.

```bash
# Check tracking state in node output
ros2 launch kausora_realsense_ros2 t265.launch.py

# In a second terminal, verify pose messages are arriving
ros2 topic hz /camera/t265/odom/sample
```

**Common causes:**
- Insufficient visual texture — T265 needs visible scene features to track.
  Move to a well-lit area with distinct surface patterns.
- Firmware mismatch — update via `rs-fw-update`:
  ```bash
  rs-fw-update -l           # list available firmware
  rs-fw-update -n <serial>  # update to latest
  ```
- Fast motion causing tracking loss — slow down and move camera back to a
  previously seen area to re-localise.

### Fisheye images dark or distorted

```bash
# Verify streams are enabled
ros2 topic hz /camera/t265/fisheye1/image_raw
ros2 topic hz /camera/t265/fisheye2/image_raw

# T265 fisheye cameras have a fixed exposure — low light will produce dark images.
# This is a hardware limitation; use a well-lit environment.
```

---

## Multi-Camera Issues

### One camera works but the other is ignored

**Symptom:** Only one camera publishes topics; the second is silent.

Both `realsense2_camera` nodes need unique `camera_name` values **and** explicit
serial numbers. Without serial numbers, both nodes may try to open the same device:

```bash
# Always specify both serial numbers for multi-camera setups
ros2 launch kausora_realsense_ros2 multi_camera.launch.py \
    camera1_serial:=111111111111 \
    camera2_serial:=222222222222

# Find serials with:
rs-enumerate-devices | grep Serial
```

### Topics from both cameras look identical

**Symptom:** `ros2 topic list` shows duplicate topics or only one set of topics.

Check that `camera1_name` and `camera2_name` are distinct — they default to
`camera1` and `camera2` but must be set explicitly if you override them:

```bash
ros2 launch kausora_realsense_ros2 multi_camera.launch.py \
    camera1_name:=front \
    camera2_name:=rear \
    camera1_serial:=111111111111 \
    camera2_serial:=222222222222
```

Topics will then be `/camera/front/...` and `/camera/rear/...`.

### USB bandwidth saturation

**Symptom:** Both cameras connect but frames drop or one stops streaming.

Two D435 / D455 cameras at 1280×720@30 can saturate a single USB 3.0 controller.

```bash
# Reduce resolution and frame rate in the config files:
# config/d435_config.yaml:
#   color_width: 848
#   color_height: 480
#   color_fps: 15.0
#   depth_width: 848
#   depth_height: 480
#   depth_fps: 15.0

# Check which USB root hub each camera is on:
lsusb -t | grep -A3 "Intel"
# Ideally each camera should be on a different root hub.
```

---

## Docker Issues

### Camera not visible inside Docker container

```bash
# Verify USB passthrough
docker exec kausora_realsense lsusb | grep Intel

# If not visible, check compose file has:
# privileged: true
# devices:
#   - /dev/bus/usb:/dev/bus/usb
```

### Container starts but camera node crashes

```bash
# Check container logs
docker compose logs realsense

# Common cause: USB rules not applied in container
# Solution: Run in privileged mode (already configured in compose)
```

### ROS2 topics not visible from host

```bash
# Verify network_mode: host is set
docker inspect kausora_realsense | grep -A2 NetworkMode

# Check ROS_DOMAIN_ID matches on host and container
docker exec kausora_realsense printenv ROS_DOMAIN_ID
echo $ROS_DOMAIN_ID
```

---

## Build Issues

### `colcon build` fails with missing dependencies

```bash
# Install missing deps
rosdep install --from-paths src --ignore-src -r -y

# Retry build
colcon build --packages-select kausora_realsense_ros2
```

### `package 'realsense2_camera' not found`

```bash
# Install the package
sudo apt-get install -y ros-jazzy-realsense2-camera

# Or run the install script
./scripts/install_ros2_deps.sh
```

---

## Performance Issues

### High CPU usage

```bash
# Reduce frame rate or resolution in config
# e.g. config/d435_config.yaml:
#   color_fps: 15.0
#   depth_fps: 15.0

# Disable unused streams
#   enable_infra1: false
#   enable_infra2: false
```

### Dropped frames / stuttering

- Ensure USB 3.0 connection (not a hub)
- Reduce resolution or frame rate
- Check CPU load: `htop`
- Use a powered USB hub if using multiple cameras

---

## Getting Help

If you can't resolve an issue:

1. Run the verification script and include output:
   ```bash
   python3 scripts/verify_setup.py
   ```

2. Collect system info:
   ```bash
   rs-enumerate-devices
   ros2 --version
   dpkg -l 'librealsense2*'
   uname -r
   ```

3. Contact Kausora support: **contact@kausora.com**
4. File an issue in the repository with the above information.
