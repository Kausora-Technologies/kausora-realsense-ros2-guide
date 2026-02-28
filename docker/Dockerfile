# Kausora Technologies — RealSense ROS2 Production Image
# Base: ROS2 Jazzy on Ubuntu 24.04
# Includes: librealsense2 SDK + realsense-ros2 wrapper

FROM ros:jazzy-ros-base

LABEL maintainer="contact@kausora.com"
LABEL description="Intel RealSense + ROS2 Jazzy production image"
LABEL version="1.0.0"

# Avoid interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=jazzy

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    lsb-release \
    ca-certificates \
    udev \
    libusb-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Add Intel RealSense apt repository
RUN mkdir -p /etc/apt/keyrings && \
    curl -sSf https://librealsense.intel.com/Debian/librealsense.pgp \
        | tee /etc/apt/keyrings/librealsense.pgp > /dev/null && \
    echo "deb [signed-by=/etc/apt/keyrings/librealsense.pgp] https://librealsense.intel.com/Debian/apt-repo $(lsb_release -cs) main" \
        | tee /etc/apt/sources.list.d/librealsense.list

# Install librealsense2 SDK and ROS2 realsense package
RUN apt-get update && apt-get install -y --no-install-recommends \
    librealsense2 \
    librealsense2-utils \
    ros-jazzy-realsense2-camera \
    ros-jazzy-realsense2-description \
    && rm -rf /var/lib/apt/lists/*

# Set up workspace
ENV COLCON_WS=/opt/kausora_ws
WORKDIR ${COLCON_WS}

# Copy the kausora_realsense_ros2 package
COPY . src/kausora_realsense_ros2/

# Build the workspace
RUN . /opt/ros/jazzy/setup.sh && \
    colcon build \
        --packages-select kausora_realsense_ros2 \
        --cmake-args -DCMAKE_BUILD_TYPE=Release && \
    rm -rf build/ log/

# Source ROS2 and workspace on container start
RUN echo "source /opt/ros/jazzy/setup.bash" >> /root/.bashrc && \
    echo "source ${COLCON_WS}/install/setup.bash" >> /root/.bashrc

# Add udev rules for RealSense cameras
RUN mkdir -p /etc/udev/rules.d/ && \
    curl -sSf https://raw.githubusercontent.com/IntelRealSense/librealsense/master/config/99-realsense-libusb.rules \
        -o /etc/udev/rules.d/99-realsense-libusb.rules 2>/dev/null || true

# Default command: open bash with ROS2 sourced
CMD ["/bin/bash", "-c", \
    "source /opt/ros/jazzy/setup.bash && \
     source ${COLCON_WS}/install/setup.bash && \
     exec bash"]
