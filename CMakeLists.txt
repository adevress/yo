project(yo)
cmake_minimum_required(VERSION 3.0)

enable_testing()

set(YO_VERSION_MAJOR "0")
set(YO_VERSION_MINOR "1")


add_definitions( -DYO_VERSION_MAJOR=\"${YO_VERSION_MAJOR}\" -DYO_VERSION_MINOR=\"${YO_VERSION_MINOR}\")


list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/CMake
      ${PROJECT_SOURCE_DIR}/CMake/portability
      ${PROJECT_SOURCE_DIR}/CMake/packages
      ${PROJECT_SOURCE_DIR}/CMake/config)


include(DefineInstallationPaths)
include(ReleaseDebugAutoFlags)
include(DetectCXX11Support)

find_package(Threads)



set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")


set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${CMAKE_CXX_VECTORIZE}")

#set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address -fsanitize=undefined -fsanitize=object-size")

include_directories( ${CMAKE_CURRENT_SOURCE_DIR}/include/  )
include_directories( ${CMAKE_CURRENT_SOURCE_DIR}/deps/digestpp/  )
include_directories( ${CMAKE_CURRENT_SOURCE_DIR}/deps/hadoken/include  )

include_directories(SYSTEM ${BOOST_INCLUDE_DIR} )

#
# libyo library
#
set(libyo_src "${CMAKE_CURRENT_SOURCE_DIR}/src/yo.cpp")

add_library(libyo ${libyo_src} ${YO_HEADERS_1} ${YO_HEADERS_2})
target_link_libraries(libyo ${CMAKE_THREAD_LIBS_INIT})
install(TARGETS libyo DESTINATION ${LIB_INSTALL_DIR}/)


# yocp tool
set(yocp_src "${CMAKE_CURRENT_SOURCE_DIR}/src/yocp.cpp")

add_executable(yocp ${yocp_src} ${YO_HEADERS_1} ${YO_HEADERS_2})
target_link_libraries(yocp ${CMAKE_THREAD_LIBS_INIT} libyo)


install(TARGETS yocp DESTINATION ${BIN_INSTALL_DIR}/)


