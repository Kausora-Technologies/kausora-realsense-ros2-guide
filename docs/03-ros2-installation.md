# ROS2 Jazzy Installation

Install ROS2 Jazzy Jalisco on Ubuntu 24.04 LTS.

---

## Installation

### Step 1 — Set Locale

```bash
locale  # Check current locale

sudo apt-get update && sudo apt-get install -y locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

### Step 2 — Add ROS2 Repository

```bash
sudo apt-get install -y software-properties-common
sudo add-apt-repository universe

sudo apt-get update && sudo apt-get install -y curl
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
    -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
    | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

### Step 3 — Install ROS2 Jazzy

```bash
sudo apt-get update
sudo apt-get upgrade -y

# Desktop install (includes RViz, rqt — recommended for development)
sudo apt-get install -y ros-jazzy-desktop

# Or base install (headless — for production/Docker)
# sudo apt-get install -y ros-jazzy-ros-base
```

### Step 4 — Install Development Tools

```bash
sudo apt-get install -y \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-argcomplete

# Initialize rosdep
sudo rosdep init
rosdep update
```

### Step 5 — Source ROS2

```bash
# Add to ~/.bashrc for automatic sourcing
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

## Verify Installation

```bash
# Check ROS2 version
ros2 --version

# Run the talker demo (in one terminal)
ros2 run demo_nodes_cpp talker

# Run the listener demo (in another terminal)
ros2 run demo_nodes_cpp listener
```

---

## Workspace Setup

Create a colcon workspace for Kausora packages:

```bash
mkdir -p ~/kausora_ws/src
cd ~/kausora_ws

# Clone or place the kausora_realsense_ros2 package
# (if not already done)
# git clone <repo-url> src/kausora-realsense-ros2-guide

# Source ROS2 (required before colcon — open a new shell or run this explicitly)
source /opt/ros/jazzy/setup.bash

# Install dependencies
rosdep install --from-paths src --ignore-src -r -y

# Build
colcon build --packages-select kausora_realsense_ros2 \
    --cmake-args -DCMAKE_BUILD_TYPE=Release

# Source the workspace
source install/setup.bash
```

---

## Next Steps

- [RealSense ROS2 Setup →](./04-realsense-ros2-setup.md)
