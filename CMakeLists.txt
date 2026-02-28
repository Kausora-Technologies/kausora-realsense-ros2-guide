cmake_minimum_required(VERSION 3.8)
project(kausora_realsense_ros2)

# This is a launch-file-only package — no C++ compilation.
# Runtime dependencies (realsense2_camera, sensor_msgs, etc.) are declared
# in package.xml as exec_depend and do not need to be found at build time.
find_package(ament_cmake REQUIRED)

# Install launch files
install(
  DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch
)

# Install config files
install(
  DIRECTORY config/
  DESTINATION share/${PROJECT_NAME}/config
)

# Install RViz config files
install(
  DIRECTORY rviz/
  DESTINATION share/${PROJECT_NAME}/rviz
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
