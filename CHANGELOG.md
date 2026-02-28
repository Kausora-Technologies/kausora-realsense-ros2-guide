# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.0] — 2026-02-28

### Added

- Launch files for D415, D435, D435i, D455, L515, T265, and multi-camera setups
- Per-camera YAML parameter config files
- Pre-configured RViz2 display layouts with `launch_rviz:=true` argument
- Docker production image (`Dockerfile`) and developer image (`Dockerfile.dev`)
- Docker Compose setup with USB passthrough and X11 support
- `scripts/verify_setup.py` — checks librealsense SDK, connected cameras, and ROS2 environment
- `scripts/install_sdk.sh` — installs librealsense2 SDK on Ubuntu 24.04
- `scripts/install_ros2_deps.sh` — installs ROS2 Jazzy realsense packages
- Seven step-by-step documentation guides (prerequisites through troubleshooting)
- GitHub Actions CI: separate Build, Lint, and Docker workflows
