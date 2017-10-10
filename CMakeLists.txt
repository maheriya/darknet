cmake_minimum_required(VERSION 3.9 FATAL_ERROR)
project(darknet LANGUAGES C CXX CUDA)

## Version and paths
set(DARKNET_MAJOR_VERSION 2)
set(DARKNET_MINOR_VERSION 0)
set(DARKNET_PATCH_VERSION 1)
set(DARKNET_VERSION ${DARKNET_MAJOR_VERSION}.${DARKNET_MINOR_VERSION}.${DARKNET_PATCH_VERSION})


## Global configuration of features
set (EN_OPENCV 1)
set (EN_OPENMP 1)
 
# Offer the user the choice of overriding the installation directories
set(INSTALL_LIB_DIR     lib     CACHE PATH "Installation directory for libraries")
set(INSTALL_BIN_DIR     bin     CACHE PATH "Installation directory for executables")
set(INSTALL_INCLUDE_DIR include CACHE PATH "Installation directory for header files")
set(DEF_INSTALL_CMAKE_DIR lib/CMake/Darknet)
set(INSTALL_CMAKE_DIR ${DEF_INSTALL_CMAKE_DIR} CACHE PATH "Installation directory for CMake files")
 
# Make relative paths absolute (needed later on)
foreach(p LIB BIN INCLUDE CMAKE)
  set(var INSTALL_${p}_DIR)
  if(NOT IS_ABSOLUTE "${${var}}")
    set(${var} "${CMAKE_INSTALL_PREFIX}/${${var}}")
  endif()
endforeach()

## CUDA Stuff
set(CMAKE_CUDA_FLAGS "${CMAKE_CUDA_FLAGS} -gencode arch=compute_61,code=sm_61")
set(COMMON  "${COMMON} -DGPU -I/usr/local/cuda/include")
set(CFLAGS  "${CFLAGS} -DGPU")
##set(LDFLAGS "${LDFLAGS} -L/usr/local/cuda/lib64 -lcuda -lcudart -lcublas -lcurand -lstdc++")
if (EN_CUDNN)
  message("==== CUDNN is enabled")
  set(COMMON  "${COMMON} -DCUDNN")
  set(CFLAGS  "${CFLAGS} -DCUDNN")
  set(LDFLAGS "${LDFLAGS} -lcudnn")
endif()

 
if (EN_OPENCV)
 # Find OpenCV
 find_package( OpenCV 2.4 REQUIRED ) # not requiring EXACT sub-version
 include_directories (${OpenCV_INCLUDE_DIRS})
 set(OPENCV_LIBS ${OpenCV_LIBS})
 set(COMMON "${COMMON} -DOPENCV")
 set(CFLAGS "${CFLAGS} -DOPENCV")
endif()


if (EN_OPENMP)
  set(CFLAGS "${CFLAGS} -fopenmp" )
endif()

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${CFLAGS} -std=c++11" )
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${COMMON} ${CFLAGS}" )
set(CMAKE_CUDA_FLAGS "${CMAKE_CUDA_FLAGS} ${COMMON} --compiler-options '${CFLAGS}'")
message("CMAKE_CUDA_FLAGS = ${CMAKE_CUDA_FLAGS}")

# set up include-directories
include_directories(include src "${PROJECT_BINARY_DIR}")
 
#Set CXX standard
##--ADD_DEFINITIONS(
##--      -std=c++11
##--)

set(LIBNAME ${PROJECT_NAME})
# Add sub-directories
add_subdirectory(${PROJECT_NAME})
add_subdirectory(examples)

## Generate and install CMake Config files for use by other CMake builds
include(cmake/GenConfig.cmake)

