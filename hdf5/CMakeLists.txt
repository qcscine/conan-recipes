cmake_minimum_required(VERSION 3.6)
project(cmake_wrapper)

include(${CMAKE_CURRENT_BINARY_DIR}/../conanbuildinfo.cmake)
conan_basic_setup()

enable_testing()
add_subdirectory(${CMAKE_CURRENT_BINARY_DIR}/../source_subfolder)
