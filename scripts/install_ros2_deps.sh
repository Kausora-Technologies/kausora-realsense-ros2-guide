#!/usr/bin/env bash
# Kausora Technologies — ROS2 RealSense Dependencies Installer
# Installs ros-jazzy-realsense2-camera and related packages

set -euo pipefail

ROS_DISTRO="${ROS_DISTRO:-jazzy}"

# ─── Colors ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC} $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }

# ─── Check ROS2 is installed ─────────────────────────────────────────────────
check_ros2() {
    if [[ ! -d "/opt/ros/${ROS_DISTRO}" ]]; then
        log_error "ROS2 ${ROS_DISTRO} not found at /opt/ros/${ROS_DISTRO}"
        log_error "Please install ROS2 Jazzy first: docs/03-ros2-installation.md"
        exit 1
    fi
    log_info "ROS2 ${ROS_DISTRO} found at /opt/ros/${ROS_DISTRO}"
}

# ─── Install ROS2 RealSense packages ─────────────────────────────────────────
install_ros2_realsense() {
    log_info "Installing ROS2 RealSense packages for ${ROS_DISTRO}..."

    sudo apt-get update -q
    sudo apt-get install -y \
        "ros-${ROS_DISTRO}-realsense2-camera" \
        "ros-${ROS_DISTRO}-realsense2-description" \
        "ros-${ROS_DISTRO}-rviz2"

    log_info "ROS2 RealSense packages installed."
}

# ─── Verify ROS2 packages ────────────────────────────────────────────────────
verify_ros2_packages() {
    log_info "Verifying ROS2 RealSense packages..."

    # Source ROS2
    # shellcheck source=/dev/null
    source "/opt/ros/${ROS_DISTRO}/setup.bash"

    if ros2 pkg list 2>/dev/null | grep -q "realsense2_camera"; then
        log_info "realsense2_camera package found in ROS2."
    else
        log_error "realsense2_camera not found in ROS2 package list."
        exit 1
    fi
}

# ─── Print usage info ────────────────────────────────────────────────────────
print_usage() {
    echo
    log_info "ROS2 RealSense setup complete!"
    echo
    echo "  Source ROS2:"
    echo "    source /opt/ros/${ROS_DISTRO}/setup.bash"
    echo
    echo "  Launch a camera (e.g. D435):"
    echo "    ros2 launch kausora_realsense_ros2 d435.launch.py"
    echo
    echo "  Or use the realsense wrapper directly:"
    echo "    ros2 launch realsense2_camera rs_launch.py"
    echo
    echo "  Run verification:"
    echo "    python3 scripts/verify_setup.py"
    echo
}

# ─── Main ─────────────────────────────────────────────────────────────────────
main() {
    echo "=============================================="
    echo " Kausora — ROS2 RealSense Dependencies"
    echo " ROS distribution: ${ROS_DISTRO}"
    echo "=============================================="
    echo

    check_ros2
    install_ros2_realsense
    verify_ros2_packages
    print_usage
}

main "$@"
