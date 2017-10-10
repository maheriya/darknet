# Setup compilation of the Darknet executable using the lib
#
file(GLOB SRC "*.c")

CUDA_ADD_EXECUTABLE(Darknet ${SRC})
target_link_libraries(Darknet
  ${PROJECT_NAME}
  ${OPENCV_LIBS}
  ${CUDA_LIBRARIES} ${CUDA_curand_LIBRARY} ${CUDA_CUBLAS_LIBRARIES}
  ${LIBFLAGS})

install(TARGETS Darknet
    # IMPORTANT: Add the Darknet executable to the "export-set"
    EXPORT DarknetTargets
    RUNTIME DESTINATION "${INSTALL_BIN_DIR}" COMPONENT bin)

