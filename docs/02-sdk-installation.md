# librealsense SDK Installation

Install the Intel RealSense SDK 2.0 on Ubuntu 24.04.

---

## Automated Installation (Recommended)

Use the provided script to install and configure the SDK automatically:

```bash
chmod +x scripts/install_sdk.sh
./scripts/install_sdk.sh
```

The script:
1. Verifies Ubuntu 24.04
2. Adds the Intel RealSense apt repository
3. Installs `librealsense2`, `librealsense2-utils`, `librealsense2-dev`, and udev rules

---

## Manual Installation

If you prefer to install manually:

### Step 1 — Add the Intel RealSense Repository

```bash
sudo apt-get update
sudo apt-get install -y curl gnupg2 ca-certificates

# Add signing key
sudo mkdir -p /etc/apt/keyrings
curl -sSf https://librealsense.intel.com/Debian/librealsense.pgp \
    | sudo tee /etc/apt/keyrings/librealsense.pgp > /dev/null

# Add repository
echo "deb [signed-by=/etc/apt/keyrings/librealsense.pgp] \
https://librealsense.intel.com/Debian/apt-repo $(lsb_release -cs) main" \
    | sudo tee /etc/apt/sources.list.d/librealsense.list > /dev/null

sudo apt-get update
```

### Step 2 — Install Packages

```bash
# Core SDK
sudo apt-get install -y librealsense2

# Command-line tools (rs-enumerate-devices, realsense-viewer, etc.)
sudo apt-get install -y librealsense2-utils

# Development headers (required if building C++ applications)
sudo apt-get install -y librealsense2-dev

# udev rules (enables non-root USB access)
sudo apt-get install -y librealsense2-udev-rules
```

---

## Verify Installation

```bash
# List connected cameras
rs-enumerate-devices

# Check installed version
dpkg -l librealsense2

# Open the graphical viewer (requires display)
realsense-viewer
```

Expected output from `rs-enumerate-devices` with a D435 connected:

```
Device info:
    Name                          :     Intel RealSense D435
    Serial Number                 :     123456789012
    Firmware Version              :     05.16.00.01
    ...
```

---

## Troubleshooting

### "USB 2.0 detected" warning
Connect the camera to a USB 3.0 (blue) port.

### "LIBUSB_ERROR_ACCESS" or permission denied
```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
# Reconnect the camera
```

### Kernel module conflicts (DKMS)
```bash
sudo apt-get install -y librealsense2-dkms
sudo dkms autoinstall
```

---

## Next Steps

- [ROS2 Installation →](./03-ros2-installation.md)
