cmake_minimum_required( VERSION 2.8 )
project( UnitreeCameraSDK )

set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bins/)

find_package(OpenCV 4 REQUIRED)
if(OpenCV_FOUND)
    include_directories(${OpenCV_INCLUDE_DIR})
    message(STATUS "OpenCV ${OpenCV_VERSION} FOUND")
    message(STATUS ${OpenCV_LIBS})
    if(${OpenCV_VERSION_MAJOR} EQUAL 4)
        add_definitions(-DOPENCV_VERSION_4)
    elseif(${OpenCV_VERSION_MAJOR} LESS 4)
        add_definitions(-DOPENCV_VERSION_3)
    endif()
else()
    message(FATAL_ERROR "OpenCV Library Not Found")
endif()

if(CMAKE_HOST_SYSTEM_PROCESSOR MATCHES "x86_64")
set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib/amd64/)
link_directories(${PROJECT_SOURCE_DIR}/lib/amd64/)
else()
set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib/arm64/)
link_directories(${PROJECT_SOURCE_DIR}/lib/arm64/)
endif()

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -pthread")
include_directories(${PROJECT_SOURCE_DIR}/include)

set(SDKLIBS unitree_camera tstc_V4L2_xu_camera udev systemlog ${OpenCV_LIBS})

# add_subdirectory(${PROJECT_SOURCE_DIR}/examples)


# 以上是官方SDK内容
# 以下是ERNIE-Dog项目添加的部分

find_package(JPEG REQUIRED)
include_directories(${JPEG_INCLUDE_DIR})

include_directories(/home/unitree/PicSocket/install/include)
link_directories(/home/unitree/PicSocket/install/lib)

add_executable(ERNIE_Dog_nano1 ERNIE_Dog_nano1.cpp)
target_link_libraries(ERNIE_Dog_nano1 ${SDKLIBS} picsocket ${JPEG_LIBRARIES})
