# Prerequisites

This guide covers hardware, software, and USB requirements for using Intel RealSense cameras with ROS2 Jazzy.

---

## Hardware Requirements

### Host Machine

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | Intel Core i5 (6th gen) / AMD Ryzen 5 | Intel Core i7+ / AMD Ryzen 7+ |
| RAM | 8 GB | 16 GB+ |
| Storage | 20 GB free | 40 GB+ SSD |
| USB | USB 3.0 (one port) | USB 3.1 Gen 1+ |

> **Note:** USB 2.0 will work for some cameras at reduced resolution and frame rate, but USB 3.0 is strongly recommended for full capability.

### Supported Camera Models

| Camera | Type | USB | Depth | Color | IMU | Fisheye |
|--------|------|-----|-------|-------|-----|---------|
| D415 | Stereo Active | 3.0 | Yes | Yes | No | No |
| D435 | Stereo Global | 3.0 | Yes | Yes | No | No |
| D435i | Stereo + IMU | 3.0 | Yes | Yes | Yes | No |
| D455 | Long-range Stereo | 3.0 | Yes | Yes | No | No |
| L515 | LiDAR | 3.2 | Yes | Yes | No | No |
| T265 | Tracking (VIO) | 2.0+ | No | No | Yes | Yes |

---

## Operating System

- **Required:** Ubuntu 24.04 LTS (Noble Numbat)
- **ROS2 Distribution:** Jazzy Jalisco

Ubuntu 24.04 is required for ROS2 Jazzy. Other distributions are not supported by these scripts.

```bash
lsb_release -a
# Should output: Ubuntu 24.04
```

---

## USB Requirements

RealSense cameras require proper USB access permissions.

### Verify USB 3.0 detection

After connecting your camera:

```bash
lsusb | grep -i intel
# Example output: Bus 002 Device 003: ID 8086:0b3a Intel Corp. Intel(R) RealSense(TM) Depth Camera 435i
```

The bus number (`002` = USB 3.x, `001` = USB 2.x) indicates which USB version is in use.

### udev Rules

The librealsense SDK installer automatically installs udev rules. If you encounter permission errors:

```bash
# Check if rules are installed
ls /etc/udev/rules.d/ | grep realsense

# Reload rules manually if needed
sudo udevadm control --reload-rules
sudo udevadm trigger

# Then reconnect the camera
```

### Running Without sudo

After installing udev rules, add your user to the `plugdev` group:

```bash
sudo usermod -aG plugdev $USER
# Log out and back in for the group change to take effect
```

---

## Network Requirements (Docker)

When running in Docker with `network_mode: host`:
- Ensure `ROS_DOMAIN_ID` is set consistently across your network
- No additional firewall rules needed for localhost-only use

---

## Next Steps

- [SDK Installation →](./02-sdk-installation.md)
