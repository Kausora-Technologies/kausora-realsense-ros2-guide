from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('camera_name', default_value='d435'),
        DeclareLaunchArgument('camera_namespace', default_value='camera'),
        DeclareLaunchArgument('serial_no', default_value=''),
        DeclareLaunchArgument('enable_pointcloud', default_value='false'),
        DeclareLaunchArgument('align_depth.enable', default_value='false'),
        DeclareLaunchArgument('initial_reset', default_value='false',
                              description='Hardware reset on node startup (use to recover from USB errors)'),
        DeclareLaunchArgument(
            'launch_rviz', default_value='false',
            description='Launch RViz2 with pre-configured display layout'),

        Node(
            package='realsense2_camera',
            executable='realsense2_camera_node',
            name=LaunchConfiguration('camera_name'),
            namespace=LaunchConfiguration('camera_namespace'),
            parameters=[{
                'camera_name': LaunchConfiguration('camera_name'),
                'camera_namespace': LaunchConfiguration('camera_namespace'),
                'serial_no': LaunchConfiguration('serial_no'),
                # Color stream
                'enable_color': True,
                'color_width': 848,
                'color_height': 480,
                'color_fps': 30.0,
                # Depth stream
                'enable_depth': True,
                'depth_width': 848,
                'depth_height': 480,
                'depth_fps': 30.0,
                # Infrared
                'enable_infra1': False,
                'enable_infra2': False,
                # Pointcloud
                'pointcloud.enable': LaunchConfiguration('enable_pointcloud'),
                'align_depth.enable': LaunchConfiguration('align_depth.enable'),
                'initial_reset': LaunchConfiguration('initial_reset'),
            }],
            output='screen',
            emulate_tty=True,
        ),

        Node(
            condition=IfCondition(LaunchConfiguration('launch_rviz')),
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', PathJoinSubstitution([
                FindPackageShare('kausora_realsense_ros2'), 'rviz', 'd435.rviz'
            ])],
            output='screen',
        ),
    ])
