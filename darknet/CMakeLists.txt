#
#
#
file(GLOB SRC      "*.c")
file(GLOB CUDASRC  "*.cu")
file(GLOB GHEADERS "${PROJECT_SOURCE_DIR}/include/*.h")
file(GLOB HEADERS  "*.h")

CUDA_ADD_LIBRARY(${PROJECT_NAME} SHARED ${SRC} ${CUDASRC} ${GHEADERS})
 
# Request that the library be built with -std=c++11 as a public compile feature.
# As a result anything that links to this library will also build with -std=c++11
target_compile_features(${PROJECT_NAME} PUBLIC cxx_std_11)

# Explicitly state that all CUDA files in this library to be built with -dc as the
# member functions could be called by other libraries and executables
set_target_properties(${PROJECT_NAME} PROPERTIES CUDA_SEPARABLE_COMPILATION ON)
set_target_properties(${PROJECT_NAME} PROPERTIES PUBLIC_HEADER "${GHEADERS}")
set_target_properties(${PROJECT_NAME} PROPERTIES SOVERSION 2)

install(TARGETS ${PROJECT_NAME}
  # IMPORTANT: Add the library to the "export-set"
  EXPORT DarknetTargets
  RUNTIME DESTINATION "${INSTALL_BIN_DIR}" COMPONENT bin
  LIBRARY DESTINATION "${INSTALL_LIB_DIR}" COMPONENT shlib
  PUBLIC_HEADER DESTINATION "${INSTALL_INCLUDE_DIR}/${PROJECT_NAME}" COMPONENT dev)

