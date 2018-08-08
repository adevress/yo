project(yo)
cmake_minimum_required(VERSION 3.0)


option(YO_PYTHON_BINDINGS "Enable compilation of python bindings" ON)

set(PYTHON_VERSION "" CACHE STRING "Python version to use")

set(YO_VERSION_MAJOR "0")
set(YO_VERSION_MINOR "3")


add_definitions( -DYO_VERSION_MAJOR=\"${YO_VERSION_MAJOR}\" -DYO_VERSION_MINOR=\"${YO_VERSION_MINOR}\")


list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/CMake
      ${PROJECT_SOURCE_DIR}/CMake/portability
      ${PROJECT_SOURCE_DIR}/CMake/packages
      ${PROJECT_SOURCE_DIR}/CMake/config)

include(CTest)
include(GNUInstallDirs)
include(ReleaseDebugAutoFlags)
include(CompilerFlagsHelpers)
include(DetectCXX11Support)
include(FindPkgConfig)


find_package(Threads)
find_package(Boost 1.41 COMPONENTS system)




## use pkg-config, avoid all the stupidiocratic issues of FindPythonInterp / Libs
pkg_search_module(PYTHON REQUIRED python${PYTHON_VERSION})


if(NOT DEFINED CMAKE_INSTALL_PYTHON_SITE_PACKAGE)
    set(CMAKE_INSTALL_PYTHON_SITE_PACKAGE "${CMAKE_INSTALL_FULL_LIBDIR}/python${PYTHON_VERSION}/site-packages/")
endif()



set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")


set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${CMAKE_CXX_VECTORIZE}")

#set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address -fsanitize=undefined -fsanitize=object-size")

include_directories( ${CMAKE_CURRENT_SOURCE_DIR}/include/  )
include_directories( ${CMAKE_CURRENT_SOURCE_DIR}/deps/digestpp/  )
include_directories( ${CMAKE_CURRENT_SOURCE_DIR}/deps/pybind11/include  )
include_directories( ${CMAKE_CURRENT_SOURCE_DIR}/deps/hadoken/include  )

include_directories(SYSTEM ${Boost_INCLUDE_DIR} )

#
# libyo library
#
set(libyo_src "${CMAKE_CURRENT_SOURCE_DIR}/src/yo.cpp")

add_library(libyo STATIC ${libyo_src} ${YO_HEADERS_1} ${YO_HEADERS_2})
target_link_libraries(libyo ${CMAKE_THREAD_LIBS_INIT})
target_compile_options(libyo PUBLIC ${CMAKE_CXX_POSITION_INDEPENDANT})

set_target_properties(libyo PROPERTIES OUTPUT_NAME "yo")


install(TARGETS libyo DESTINATION ${CMAKE_INSTALL_FULL_LIBDIR}/)

#
# yocp tool
#
set(yocp_src "${CMAKE_CURRENT_SOURCE_DIR}/src/yocp.cpp")

add_executable(yocp ${yocp_src} ${YO_HEADERS_1} ${YO_HEADERS_2})
target_link_libraries(yocp ${CMAKE_THREAD_LIBS_INIT} libyo)


install(TARGETS yocp DESTINATION ${CMAKE_INSTALL_FULL_BINDIR}/)


#
# yo python module
#
set(pyyo_src "${CMAKE_CURRENT_SOURCE_DIR}/src/pyyo.cpp")
add_library(pyyo MODULE ${pyyo_src} ${YO_HEADERS_1} ${YO_HEADERS_2})
target_link_libraries(pyyo ${CMAKE_THREAD_LIBS_INIT} ${PYTHON_LIBRARIES}  libyo )
set_target_properties(pyyo PROPERTIES
    OUTPUT_NAME "_yo"
    PREFIX "")
target_include_directories(pyyo PRIVATE ${PYTHON_INCLUDE_DIRS})

FILE(GLOB PY_FILES "${CMAKE_CURRENT_SOURCE_DIR}/python/*.py")
FILE(GLOB PY_NUMPY_FILES "${CMAKE_CURRENT_SOURCE_DIR}/python/numpyio/*.py")
FILE(GLOB PY_PICKLE_FILES "${CMAKE_CURRENT_SOURCE_DIR}/python/pickleio/*.py")
FILE(GLOB PY_TEST_FILES "${CMAKE_CURRENT_SOURCE_DIR}/python/test/*.py")

install(TARGETS pyyo DESTINATION ${CMAKE_INSTALL_PYTHON_SITE_PACKAGE}/yo)
install(FILES ${PY_FILES} DESTINATION ${CMAKE_INSTALL_PYTHON_SITE_PACKAGE}/yo)
install(FILES ${PY_NUMPY_FILES} DESTINATION ${CMAKE_INSTALL_PYTHON_SITE_PACKAGE}/yo/numpyio)
install(FILES ${PY_PICKLE_FILES} DESTINATION ${CMAKE_INSTALL_PYTHON_SITE_PACKAGE}/yo/pickleio)
install(FILES ${PY_TEST_FILES} DESTINATION ${CMAKE_INSTALL_PYTHON_SITE_PACKAGE}/yo/test)

## install headers
install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/include/yo DESTINATION ${CMAKE_INSTALL_FULL_INCLUDEDIR})


## pkgconfig
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/yo.pc.in ${CMAKE_CURRENT_BINARY_DIR}/yo.pc @ONLY)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/yo.pc DESTINATION ${CMAKE_INSTALL_FULL_LIBDIR}/pkgconfig/)
