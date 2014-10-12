if(EXISTS "/etc/debian_version")
  set(SETUPTOOLS_ARG_EXTRA "--install-layout=deb")
else()
  set(SETUPTOOLS_ARG_EXTRA "")
endif()
add_custom_target(compile_openrtm_aist_python ALL
  COMMAND python setup.py build
  COMMAND python setup.py install --prefix=${CMAKE_INSTALL_PREFIX} ${SETUPTOOLS_ARG_EXTRA}
  WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})

install(FILES package.xml DESTINATION share/openrtm_aist_python/)
