# Install DarknetConfig*.cmake files
# ===================================
# Add all targets to the build-tree export set
export(TARGETS ${PROJECT_NAME} FILE "${PROJECT_BINARY_DIR}/DarknetTargets.cmake")
 
# Export the package for use from the build-tree
# (this registers the build-tree with a global CMake-registry)
export(PACKAGE Darknet)
 
# Create the DarknetConfig.cmake and DarknetConfigVersion files
file(RELATIVE_PATH REL_INCLUDE_DIR "${INSTALL_CMAKE_DIR}" "${INSTALL_INCLUDE_DIR}")
# ... for the build tree
set(CONF_INCLUDE_DIRS include)
set(CONF_LIBNAME "${PROJECT_NAME}")
set(CONF_LIBRARY_DIRS lib)
configure_file(DarknetConfig.cmake.in "${PROJECT_BINARY_DIR}/DarknetConfig.cmake" @ONLY)
# ... for the install tree
set(CONF_INCLUDE_DIRS "${CMAKE_INSTALL_PREFIX}/${CONF_INCLUDE_DIRS}")
set(CONF_LIBRARY_DIRS "${CMAKE_INSTALL_PREFIX}/${CONF_LIBRARY_DIRS}")
configure_file(DarknetConfig.cmake.in "${PROJECT_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/DarknetConfig.cmake" @ONLY)
# ... for both
configure_file(DarknetConfigVersion.cmake.in "${PROJECT_BINARY_DIR}/DarknetConfigVersion.cmake" @ONLY)
 
# Install the DarknetConfig.cmake and DarknetConfigVersion.cmake
install(FILES
  "${PROJECT_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/DarknetConfig.cmake"
  "${PROJECT_BINARY_DIR}/DarknetConfigVersion.cmake"
  DESTINATION "${INSTALL_CMAKE_DIR}" COMPONENT dev)
 

# Install the export set for use with the install-tree
install(EXPORT DarknetTargets DESTINATION "${INSTALL_CMAKE_DIR}" COMPONENT dev)
