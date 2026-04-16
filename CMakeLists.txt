cmake_minimum_required(VERSION 3.5)
project(sofar_lab)

set(CMAKE_CXX_STANDARD 14)

find_package(ament_cmake_auto REQUIRED)
ament_auto_find_build_dependencies()
  
install(PROGRAMS script/pose2odom.py
  DESTINATION lib/${PROJECT_NAME})

ament_auto_package()
