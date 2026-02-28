#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Kausora Technologies
# Kausora Technologies — librealsense2 SDK Installer
# Targets: Ubuntu 24.04 LTS (Noble Numbat) with ROS2 Jazzy
# librealsense version: >= 2.56.1

set -euo pipefail

LIBREALSENSE_MIN_VERSION="2.56.1"

# ─── Colors ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info()    { echo -e "${GREEN}[INFO]${NC} $*"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $*"; }

# ─── Check Ubuntu version ────────────────────────────────────────────────────
check_ubuntu_version() {
    if ! command -v lsb_release &>/dev/null; then
        log_error "lsb_release not found. This script requires Ubuntu 24.04."
        exit 1
    fi

    local distro version
    distro=$(lsb_release -is)
    version=$(lsb_release -rs)

    if [[ "$distro" != "Ubuntu" ]]; then
        log_error "This script requires Ubuntu. Detected: $distro"
        exit 1
    fi

    if [[ "$version" != "24.04" ]]; then
        log_warn "This script targets Ubuntu 24.04. Detected: $version"
        log_warn "Proceeding anyway — results may vary."
    else
        log_info "Ubuntu $version detected. Supported."
    fi
}

# ─── Add Intel RealSense apt repository ──────────────────────────────────────
add_realsense_repo() {
    log_info "Adding Intel RealSense apt repository..."

    sudo apt-get update -q
    sudo apt-get install -y --no-install-recommends curl gnupg2 ca-certificates

    sudo mkdir -p /etc/apt/keyrings
    curl -sSf https://librealsense.intel.com/Debian/librealsense.pgp \
        | sudo tee /etc/apt/keyrings/librealsense.pgp > /dev/null

    local codename
    codename=$(lsb_release -cs)

    echo "deb [signed-by=/etc/apt/keyrings/librealsense.pgp] \
https://librealsense.intel.com/Debian/apt-repo ${codename} main" \
        | sudo tee /etc/apt/sources.list.d/librealsense.list > /dev/null

    sudo apt-get update -q
    log_info "RealSense repository added."
}

# ─── Install librealsense packages ───────────────────────────────────────────
install_librealsense() {
    log_info "Installing librealsense2 packages..."

    sudo apt-get install -y \
        librealsense2 \
        librealsense2-utils \
        librealsense2-dev \
        librealsense2-udev-rules

    log_info "librealsense2 installed."
}

# ─── Verify installation ─────────────────────────────────────────────────────
verify_installation() {
    log_info "Verifying librealsense2 installation..."

    if ! command -v realsense-viewer &>/dev/null && ! command -v rs-enumerate-devices &>/dev/null; then
        log_error "Verification failed: librealsense2 tools not found in PATH."
        exit 1
    fi

    local installed_version
    installed_version=$(dpkg -l librealsense2 2>/dev/null | grep '^ii' | awk '{print $3}' | cut -d'-' -f1)

    if [[ -n "$installed_version" ]]; then
        log_info "Installed librealsense2 version: $installed_version"
    fi

    log_info "Installation verified successfully."
}

# ─── Main ─────────────────────────────────────────────────────────────────────
main() {
    echo "=============================================="
    echo " Kausora — librealsense2 SDK Installer"
    echo " Target: Ubuntu 24.04 + librealsense >= ${LIBREALSENSE_MIN_VERSION}"
    echo "=============================================="
    echo

    check_ubuntu_version
    add_realsense_repo
    install_librealsense
    verify_installation

    echo
    log_info "SDK installation complete!"
    log_info "Connect your RealSense camera and run: rs-enumerate-devices"
    log_info "For ROS2 packages, run: ./scripts/install_ros2_deps.sh"
}

main "$@"
