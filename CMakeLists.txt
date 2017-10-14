cmake_minimum_required(VERSION 3.9 FATAL_ERROR)
project(darknet LANGUAGES C CXX CUDA)

## Version
set(DARKNET_MAJOR_VERSION 2)
set(DARKNET_MINOR_VERSION 0)
set(DARKNET_PATCH_VERSION 0)
set(DARKNET_VERSION ${DARKNET_MAJOR_VERSION}.${DARKNET_MINOR_VERSION}.${DARKNET_PATCH_VERSION})
include(cmake/ConfDirs.cmake)


## Global configuration of features
set (EN_OPENCV ON)
set (EN_OPENMP ON)
set (EN_CUDNN  ON)
 
## C flags
set(CFLGS  "-Wall -Wno-unknown-pragmas -Wfatal-errors")

## CUDA (cmake 3.8 onwards CUDA is implicitly available; however, using find_package allows more flexibility)
find_package(CUDA 8.0 REQUIRED)
CUDA_SELECT_NVCC_ARCH_FLAGS(CUDA_NVCC_FLAGS 6.1 6.2)
#LIST(APPEND CUDA_NVCC_FLAGS ${ARCH_FLAGS})
set(CUDA_PROPAGATE_HOST_FLAGS ON)
set(CFLGS  "${CFLGS} -DDNETGPU")
if (EN_CUDNN)
  set(CFLGS  "${CFLGS} -DDNETCUDNN")
  set(LIBFLAGS "-L${CUDA_TOOLKIT_ROOT_DIR}/lib64 -lcudnn")
endif()

## OpenCV
if (EN_OPENCV)
 find_package(OpenCV 2.4 REQUIRED)
 include_directories (${OpenCV_INCLUDE_DIRS})
 set(OPENCV_LIBS ${OpenCV_LIBS})
 set(CFLGS "${CFLGS} -DOPENCV")
endif()

## OpenMP
if (EN_OPENMP)
  set(CFLGS "${CFLGS} -fopenmp" )
endif()

## Final C and CXX flags
set(CMAKE_CXX_FLAGS  "${CFLGS} -std=c++11" )
set(CMAKE_C_FLAGS    "${CFLGS}" )
##message("CUDA_TOOLKIT_ROOT_DIR: ${CUDA_TOOLKIT_ROOT_DIR}")
##message("CUDA_NVCC_FLAGS      : ${CUDA_NVCC_FLAGS}")
##message("CMAKE_C_FLAGS        : ${CMAKE_C_FLAGS}")
##message("CMAKE_CXX_FLAGS      : ${CMAKE_CXX_FLAGS}")

# set up include-directories
include_directories(include src "${PROJECT_BINARY_DIR}")
 
## Library name (used for building the lib and linking the examples)
# Add sub-directories
add_subdirectory(${PROJECT_NAME})
add_subdirectory(examples)

## Generate and install CMake Config files for use by other CMake builds
include(cmake/GenConfig.cmake)

