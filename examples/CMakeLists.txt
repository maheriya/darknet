#
#
#
file(GLOB EXAMPLES     "*.c")

 


foreach (example_src ${EXAMPLES})
    get_filename_component(example_name ${example_src} NAME_WE)

    #cuda_add_executable(${example_name} ${example_src})
    add_executable(${example_name} ${example_src})
    set_property(TARGET ${example_name} PROPERTY CUDA_SEPARABLE_COMPILATION ON)
    target_link_libraries(${example_name} PRIVATE ${LIBNAME})

 
    install(TARGETS ${example_name}
        # IMPORTANT: Add the ${example_name} executable to the "export-set"
        EXPORT DarknetTargets
        RUNTIME DESTINATION "${INSTALL_BIN_DIR}" COMPONENT bin)
endforeach()

