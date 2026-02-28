from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('camera_name', default_value='t265'),
        DeclareLaunchArgument('camera_namespace', default_value='camera'),
        DeclareLaunchArgument('serial_no', default_value=''),
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
                # T265 is a tracking camera — no standard depth/color
                'enable_color': False,
                'enable_depth': False,
                # Fisheye cameras (pose tracking uses stereo fisheye)
                'enable_fisheye1': True,
                'enable_fisheye2': True,
                # Pose stream
                'enable_pose': True,
                # IMU
                'enable_gyro': True,
                'enable_accel': True,
                'unite_imu_method': 'linear_interpolation',
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
                FindPackageShare('kausora_realsense_ros2'), 'rviz', 't265.rviz'
            ])],
            output='screen',
        ),
    ])
