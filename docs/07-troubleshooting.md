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
# Check node logs for errors
ros2 launch kausora_realsense_ros2 d435.launch.py 2>&1 | head -50

# Verify camera is detected before launching ROS2
rs-enumerate-devices

# Try with explicit serial number
ros2 launch kausora_realsense_ros2 d435.launch.py \
    serial_no:=$(rs-enumerate-devices | grep Serial | awk '{print $NF}')
```

### "No devices found" in ROS2 node

**Symptom:** `[realsense2_camera_node]: No device found.`

**Solutions:**
- Camera is not connected or not detected (see camera detection above)
- Wrong serial number specified in launch args
- Camera is in use by another process:
  ```bash
  # Find and kill processes using the camera
  fuser /dev/bus/usb/*/*
  ```

### TF transform errors

**Symptom:** `Could not find transform from X to Y`

```bash
# Check active TF frames
ros2 run tf2_tools view_frames

# Check specific transform
ros2 run tf2_ros tf2_echo camera_link camera_color_optical_frame
```

Ensure `publish_tf: true` in your config and that `camera_name` matches the frame prefix.

---

## IMU Issues (D435i / T265)

### IMU data not published

**Symptom:** `/imu` topic missing.

**Check `d435i_config.yaml`:**
```yaml
enable_gyro: true
enable_accel: true
unite_imu_method: "linear_interpolation"  # Must not be empty string for /imu topic
```

### IMU noise / drift

- Ensure camera is stationary for ~1 second after launch for IMU initialization
- Verify `unite_imu_method` is `linear_interpolation` for fused IMU data

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
   dpkg -l librealsense2
   uname -r
   ```

3. Contact Kausora support: **support@kausora.com**
4. File an issue in the repository with the above information.
