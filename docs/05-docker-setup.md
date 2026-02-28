# Docker Setup

Run RealSense cameras in Docker containers.

---

## Prerequisites

- Docker Engine 24+
- Docker Compose v2

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# Log out and back in

# Verify
docker --version
docker compose version
```

---

## Configuration

Copy the environment template:

```bash
cp docker/.env.example docker/.env
```

Edit `docker/.env`:

```bash
# Set your camera model
CAMERA_MODEL=d435

# Set serial number if using multiple cameras
# Find it with: rs-enumerate-devices | grep Serial
CAMERA_SERIAL=

# ROS Domain ID (match your network)
ROS_DOMAIN_ID=0
```

---

## Build Images

All `docker compose` commands must be run from the `docker/` directory (where `docker-compose.yml` lives):

```bash
cd docker

# Build production image
docker compose build realsense

# Build development image
docker compose build dev
```

---

## Run

### Production (camera node only)

```bash
# From the docker/ directory:
docker compose up realsense

# Override camera model at runtime
CAMERA_MODEL=d455 docker compose up realsense

# Run in background
docker compose up -d realsense
```

### Development (interactive shell)

```bash
# From the docker/ directory:
docker compose up dev

# Or attach to a running dev container
docker exec -it kausora_realsense_dev bash
```

---

## USB Access

RealSense cameras require USB passthrough. The compose file handles this:

```yaml
privileged: true
devices:
  - /dev/bus/usb:/dev/bus/usb
```

> **Important:** `privileged: true` is required for USB device access inside Docker.

Verify the camera is visible inside the container:

```bash
docker exec kausora_realsense rs-enumerate-devices
```

---

## Verify Topics from Host

With `network_mode: host`, ROS2 topics are visible on the host:

```bash
# On host machine (with ROS2 sourced)
source /opt/ros/jazzy/setup.bash
ros2 topic list
```

---

## X11 Forwarding (Visualization)

To use RViz2 or image_view from inside Docker:

```bash
# On host, allow X11 connections
xhost +local:docker

# Launch dev container (DISPLAY is set in compose)
docker compose up dev

# Inside container
rviz2
```

---

## Troubleshooting

### Camera not found inside container
```bash
# Check USB passthrough
docker exec kausora_realsense lsusb | grep Intel

# Ensure container has privileged access
docker inspect kausora_realsense | grep Privileged
```

### ROS2 topics not visible on host
```bash
# Verify network_mode is host
docker inspect kausora_realsense | grep NetworkMode
# Should output: "host"

# Check ROS_DOMAIN_ID matches
echo $ROS_DOMAIN_ID
```

---

## Next Steps

- [Camera Configs →](./06-camera-configs.md)
- [Troubleshooting →](./07-troubleshooting.md)
