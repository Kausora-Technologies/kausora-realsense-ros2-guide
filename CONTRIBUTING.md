# Contributing to kausora-realsense-ros2-guide

Thank you for your interest in contributing. This project is maintained by [Kausora Technologies](https://kausora.com).

## How to Contribute

### Reporting Issues

- Search [existing issues](https://github.com/Kausora-Technologies/kausora-realsense-ros2-guide/issues) before opening a new one.
- Include your OS version, ROS2 distro, librealsense version, and camera model.
- Attach the output of `python3 scripts/verify_setup.py` where relevant.

### Submitting Pull Requests

1. Fork the repository and create a branch from `main`.
2. Keep changes focused — one fix or feature per PR.
3. Test your changes on a real RealSense camera where possible.
4. Ensure CI passes: `colcon build` must succeed and `flake8 scripts/` must produce no errors.
5. Update docs if your change affects behaviour or configuration.
6. Open a PR against `main` with a clear description of what changed and why.

### Development Setup

```bash
git clone https://github.com/Kausora-Technologies/kausora-realsense-ros2-guide.git
cd kausora-realsense-ros2-guide
source /opt/ros/jazzy/setup.bash
mkdir -p ~/kausora_ws/src
ln -s "$(pwd)" ~/kausora_ws/src/kausora_realsense_ros2
cd ~/kausora_ws
colcon build --packages-select kausora_realsense_ros2
source install/setup.bash
```

### Lint

```bash
pip3 install flake8
flake8 scripts/ --max-line-length=120
```

## Scope

This repository covers:

- Launch files and YAML configs for D415, D435, D435i, D455, L515, and T265
- RViz2 display layouts
- Docker production and dev images
- Installation scripts and setup verification
- Step-by-step documentation

Out of scope: librealsense SDK internals, ROS2 core changes, camera firmware.

## Code Style

- Python: PEP 8, max line length 120, enforced by flake8.
- Launch files: follow the existing pattern (ROS2 Python launch API).
- YAML: 2-space indentation.
- Markdown: sentence-case headings, fenced code blocks with language tags.

## License

By contributing you agree that your contributions will be licensed under the [Apache License 2.0](LICENSE).
