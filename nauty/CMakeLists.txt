cmake_minimum_required(VERSION 3.6)
project(nauty VERSION 2.7)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

set(NAUTY_HEADERS
  ${CMAKE_CURRENT_BINARY_DIR}/sources/gtools.h
  ${CMAKE_CURRENT_BINARY_DIR}/sources/gutils.h
  ${CMAKE_CURRENT_BINARY_DIR}/sources/naugroup.h
  ${CMAKE_CURRENT_BINARY_DIR}/sources/naugstrings.h
  ${CMAKE_CURRENT_BINARY_DIR}/sources/naurng.h
  ${CMAKE_CURRENT_BINARY_DIR}/sources/nausparse.h
  ${CMAKE_CURRENT_BINARY_DIR}/sources/nautaux.h
  ${CMAKE_CURRENT_BINARY_DIR}/sources/nautinv.h
  ${CMAKE_CURRENT_BINARY_DIR}/sources/naututil.h
  ${CMAKE_CURRENT_BINARY_DIR}/sources/nauty.h
  ${CMAKE_CURRENT_BINARY_DIR}/sources/planarity.h
  ${CMAKE_CURRENT_BINARY_DIR}/sources/quarticirred28.h
  ${CMAKE_CURRENT_BINARY_DIR}/sources/rng.h
  ${CMAKE_CURRENT_BINARY_DIR}/sources/schreier.h
  ${CMAKE_CURRENT_BINARY_DIR}/sources/traces.h
)

set(NAUTY_SOURCES
  ${CMAKE_CURRENT_BINARY_DIR}/sources/gtnauty.c
  ${CMAKE_CURRENT_BINARY_DIR}/sources/gtools.c
  ${CMAKE_CURRENT_BINARY_DIR}/sources/gutil1.c
  ${CMAKE_CURRENT_BINARY_DIR}/sources/gutil2.c
  ${CMAKE_CURRENT_BINARY_DIR}/sources/naugraph.c
  ${CMAKE_CURRENT_BINARY_DIR}/sources/naugroup.c
  ${CMAKE_CURRENT_BINARY_DIR}/sources/naurng.c
  ${CMAKE_CURRENT_BINARY_DIR}/sources/nausparse.c
  ${CMAKE_CURRENT_BINARY_DIR}/sources/nautil.c
  ${CMAKE_CURRENT_BINARY_DIR}/sources/nautinv.c
  ${CMAKE_CURRENT_BINARY_DIR}/sources/naututil.c
  ${CMAKE_CURRENT_BINARY_DIR}/sources/nauty.c
  ${CMAKE_CURRENT_BINARY_DIR}/sources/schreier.c
  ${CMAKE_CURRENT_BINARY_DIR}/sources/traces.c
)

add_library(nauty ${NAUTY_HEADERS} ${NAUTY_SOURCES})
target_include_directories(nauty PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
  $<INSTALL_INTERFACE:$<INSTALL_PREFIX>/include>
)
install(
  DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/sources/
  DESTINATION include/nauty
  FILES_MATCHING PATTERN "*.h"
)

install(
  FILES ${CMAKE_CURRENT_BINARY_DIR}/sources/COPYRIGHT
  DESTINATION share/doc/nauty/licenses
)
install(TARGETS nauty EXPORT nautyTargets ARCHIVE DESTINATION lib)

include(CMakePackageConfigHelpers)
write_basic_package_version_file(
  "${CMAKE_CURRENT_BINARY_DIR}/nautyConfigVersion.cmake"
  VERSION ${nauty_VERSION}
  COMPATIBILITY AnyNewerVersion
)

configure_package_config_file(
  "config.cmake.in"
  "${CMAKE_CURRENT_BINARY_DIR}/nautyConfig.cmake"
  INSTALL_DESTINATION "lib/cmake/nauty"
)

install(
  FILES
    "${CMAKE_CURRENT_BINARY_DIR}/nautyConfigVersion.cmake"
    "${CMAKE_CURRENT_BINARY_DIR}/nautyConfig.cmake"
  DESTINATION "lib/cmake/nauty"
)

export(
  EXPORT nautyTargets
  FILE "${CMAKE_CURRENT_BINARY_DIR}/nautyTargets.cmake"
)

install(
  EXPORT nautyTargets
  FILE "nautyTargets.cmake"
  DESTINATION "lib/cmake/nauty"
)
