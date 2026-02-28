#!/usr/bin/env python3
"""
Kausora Technologies — RealSense + ROS2 Setup Verifier

Checks:
  1. librealsense2 Python bindings version
  2. Connected RealSense cameras
  3. ROS2 realsense2_camera package availability
"""

import sys
import subprocess


def check_librealsense() -> bool:
    """Check librealsense2 SDK installation and version."""
    print("\n── librealsense2 SDK ──────────────────────────────")
    try:
        import pyrealsense2 as rs  # type: ignore
        try:
            version = ".".join(str(v) for v in rs.core.version)
        except AttributeError:
            version = rs.__version__ if hasattr(rs, '__version__') else "unknown"
        print(f"  [OK] pyrealsense2 version: {version}")

        # Check minimum version
        try:
            version_parts = [int(v) for v in version.split(".")]
            min_version = [2, 56, 1]
            if version_parts >= min_version:
                print(f"  [OK] Version >= 2.56.1 requirement met.")
            else:
                print(f"  [WARN] Version {version} is below recommended 2.56.1")
        except ValueError:
            print(f"  [INFO] Could not parse version string: {version}")

        return True
    except ImportError:
        print("  [WARN] pyrealsense2 Python bindings not installed.")
        print("         Install: pip3 install pyrealsense2")
        print("         (SDK may still work via C++ libraries)")

        # Try system-level check via rs-enumerate-devices
        try:
            result = subprocess.run(
                ["dpkg", "-l", "librealsense2"],
                capture_output=True, text=True, timeout=5
            )
            if "ii  librealsense2" in result.stdout:
                version_line = [l for l in result.stdout.splitlines() if "ii  librealsense2 " in l]
                if version_line:
                    version = version_line[0].split()[2]
                    print(f"  [OK] librealsense2 system package: {version}")
                    return True
        except (subprocess.SubprocessError, FileNotFoundError):
            pass

        print("  [FAIL] librealsense2 not found. Run: ./scripts/install_sdk.sh")
        return False


def list_cameras() -> int:
    """List connected RealSense cameras."""
    print("\n── Connected Cameras ──────────────────────────────")
    camera_count = 0

    try:
        import pyrealsense2 as rs  # type: ignore
        ctx = rs.context()
        devices = ctx.query_devices()
        camera_count = len(devices)

        if camera_count == 0:
            print("  [WARN] No RealSense cameras detected.")
            print("         Ensure camera is connected via USB 3.0+")
        else:
            for i, dev in enumerate(devices):
                name = dev.get_info(rs.camera_info.name)
                serial = dev.get_info(rs.camera_info.serial_number)
                firmware = dev.get_info(rs.camera_info.firmware_version)
                usb = dev.get_info(rs.camera_info.usb_type_descriptor)
                print(f"  Camera {i + 1}: {name}")
                print(f"    Serial:   {serial}")
                print(f"    Firmware: {firmware}")
                print(f"    USB:      {usb}")

    except ImportError:
        # Try rs-enumerate-devices as fallback
        try:
            result = subprocess.run(
                ["rs-enumerate-devices"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0 and result.stdout.strip():
                print(result.stdout)
                # Count devices roughly
                camera_count = result.stdout.count("Serial Number")
            else:
                print("  [WARN] rs-enumerate-devices found no cameras.")
        except FileNotFoundError:
            print("  [SKIP] rs-enumerate-devices not available.")
        except subprocess.TimeoutExpired:
            print("  [WARN] Camera enumeration timed out.")

    return camera_count


def check_ros2() -> bool:
    """Check ROS2 Jazzy installation and realsense2_camera package."""
    print("\n── ROS2 Environment ───────────────────────────────")

    # Check ROS2 is available
    try:
        result = subprocess.run(
            ["ros2", "pkg", "list"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0:
            print("  [FAIL] ros2 command failed. Is ROS2 sourced?")
            print("         Run: source /opt/ros/jazzy/setup.bash")
            return False
    except FileNotFoundError:
        print("  [FAIL] ros2 not found in PATH.")
        print("         Run: source /opt/ros/jazzy/setup.bash")
        return False
    except subprocess.TimeoutExpired:
        print("  [FAIL] ros2 pkg list timed out.")
        return False

    packages = result.stdout.splitlines()

    # Check realsense2_camera
    if "realsense2_camera" in packages:
        print("  [OK] realsense2_camera package found.")
    else:
        print("  [FAIL] realsense2_camera not found.")
        print("         Run: ./scripts/install_ros2_deps.sh")
        return False

    # Check realsense2_description
    if "realsense2_description" in packages:
        print("  [OK] realsense2_description package found.")
    else:
        print("  [WARN] realsense2_description not found (optional).")

    # Check kausora package
    if "kausora_realsense_ros2" in packages:
        print("  [OK] kausora_realsense_ros2 package found.")
    else:
        print("  [WARN] kausora_realsense_ros2 not in ROS2 package list.")
        print("         Build the workspace: colcon build --packages-select kausora_realsense_ros2")

    return True


def print_summary(sdk_ok: bool, camera_count: int, ros2_ok: bool) -> None:
    """Print verification summary."""
    print("\n" + "=" * 52)
    print(" SUMMARY")
    print("=" * 52)
    sdk_str = "OK" if sdk_ok else "FAIL"
    cam_str = f"{camera_count} found" if camera_count > 0 else "none"
    ros2_str = "OK" if ros2_ok else "FAIL"

    print(f"  librealsense2 SDK : {sdk_str}")
    print(f"  Cameras connected : {cam_str}")
    print(f"  ROS2 + realsense  : {ros2_str}")

    all_ok = sdk_ok and ros2_ok
    if all_ok and camera_count > 0:
        print("\n  System ready! Launch a camera with:")
        print("    ros2 launch kausora_realsense_ros2 d435.launch.py")
    elif all_ok:
        print("\n  SDK and ROS2 ready. Connect a RealSense camera to get started.")
    else:
        print("\n  Issues detected. See output above for details.")
        print("  Documentation: docs/07-troubleshooting.md")


def main() -> None:
    print("=" * 52)
    print(" Kausora — RealSense + ROS2 Setup Verifier")
    print("=" * 52)

    sdk_ok = check_librealsense()
    camera_count = list_cameras()
    ros2_ok = check_ros2()
    print_summary(sdk_ok, camera_count, ros2_ok)

    if not (sdk_ok and ros2_ok):
        sys.exit(1)


if __name__ == "__main__":
    main()
