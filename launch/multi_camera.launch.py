from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """Launch multiple RealSense cameras with separate namespaces.

    Topics are published under /<namespace>/<name>/... (e.g. /camera/camera1/color/image_raw).
    Override serial numbers via launch arguments:
        ros2 launch kausora_realsense_ros2 multi_camera.launch.py \\
            camera1_serial:=111111111111 camera2_serial:=222222222222
    """
    return LaunchDescription([
        # Camera 1 arguments
        DeclareLaunchArgument('camera1_name', default_value='camera1',
                              description='Name (topic prefix) for camera 1'),
        DeclareLaunchArgument('camera1_serial', default_value='',
                              description='Serial number for camera 1 (empty = first available)'),
        DeclareLaunchArgument('camera1_namespace', default_value='camera',
                              description='ROS namespace for camera 1'),

        # Camera 2 arguments
        DeclareLaunchArgument('camera2_name', default_value='camera2',
                              description='Name (topic prefix) for camera 2'),
        DeclareLaunchArgument('camera2_serial', default_value='',
                              description='Serial number for camera 2 (empty = second available)'),
        DeclareLaunchArgument('camera2_namespace', default_value='camera',
                              description='ROS namespace for camera 2'),

        # Shared arguments
        DeclareLaunchArgument('enable_pointcloud', default_value='false'),

        # Camera 1 — topics: /<camera1_namespace>/<camera1_name>/...
        Node(
            package='realsense2_camera',
            executable='realsense2_camera_node',
            name=LaunchConfiguration('camera1_name'),
            parameters=[{
                'camera_name': LaunchConfiguration('camera1_name'),
                'camera_namespace': LaunchConfiguration('camera1_namespace'),
                'serial_no': LaunchConfiguration('camera1_serial'),
                'enable_color': True,
                'color_width': 848,
                'color_height': 480,
                'color_fps': 30.0,
                'enable_depth': True,
                'depth_width': 848,
                'depth_height': 480,
                'depth_fps': 30.0,
                'pointcloud.enable': LaunchConfiguration('enable_pointcloud'),
            }],
            output='screen',
            emulate_tty=True,
        ),

        # Camera 2 — topics: /<camera2_namespace>/<camera2_name>/...
        Node(
            package='realsense2_camera',
            executable='realsense2_camera_node',
            name=LaunchConfiguration('camera2_name'),
            parameters=[{
                'camera_name': LaunchConfiguration('camera2_name'),
                'camera_namespace': LaunchConfiguration('camera2_namespace'),
                'serial_no': LaunchConfiguration('camera2_serial'),
                'enable_color': True,
                'color_width': 848,
                'color_height': 480,
                'color_fps': 30.0,
                'enable_depth': True,
                'depth_width': 848,
                'depth_height': 480,
                'depth_fps': 30.0,
                'pointcloud.enable': LaunchConfiguration('enable_pointcloud'),
            }],
            output='screen',
            emulate_tty=True,
        ),
    ])
