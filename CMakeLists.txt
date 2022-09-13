cmake_minimum_required(VERSION 3.1.8)
set(CMAKE_VERBOSE_MAKEFILE off)
project(asio_http C CXX)


# default initialize the output paths
if( NOT  DEFINED  CMAKE_RUNTIME_OUTPUT_DIRECTORY )
    set( CMAKE_RUNTIME_OUTPUT_DIRECTORY  "${CMAKE_BINARY_DIR}/bin" )
endif()
if( NOT  DEFINED  CMAKE_LIBRARY_OUTPUT_DIRECTORY )
    set( CMAKE_LIBRARY_OUTPUT_DIRECTORY  "${CMAKE_BINARY_DIR}/lib" )
endif()
if( NOT  DEFINED  CMAKE_ARCHIVE_OUTPUT_DIRECTORY )
    set( CMAKE_ARCHIVE_OUTPUT_DIRECTORY  "${CMAKE_BINARY_DIR}/lib" )
endif()


include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()



set( CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
if (APPLE)
    set(CMAKE_INSTALL_RPATH "@loader_path/../lib") 
else()
    set(CMAKE_INSTALL_RPATH "$ORIGIN/../lib")
endif()



# disable link time optimization for all targets
set( INTERPROCEDURAL_OPTIMIZATION  OFF )

# export all symbols when compiling on windows
set( CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS  ON )


include_directories(SYSTEM
    deps/asio/asio/include
    include
)
include_directories(
    src
    include/http
)
add_definitions(-DASIO_STANDALONE -DRAPIDJSON_HAS_STDSTRING=1)
file(GLOB SOURCE_FILES src/*.cpp)
add_library(asio_http SHARED ${SOURCE_FILES})
find_package(Threads REQUIRED)
target_link_libraries(asio_http Threads::Threads)
if (CMAKE_COMPILER_IS_GNUCXX)
    set_target_properties(asio_http PROPERTIES COMPILE_FLAGS "--coverage")
    set_target_properties(asio_http PROPERTIES LINK_FLAGS "--coverage")
endif()
if (MSVC)
    add_compile_options(/EHsc)
endif()

set_property(TARGET asio_http PROPERTY CXX_STANDARD 11)
set_property(TARGET asio_http PROPERTY CXX_STANDARD_REQUIRED TRUE)


if(WIN32)
    install(TARGETS asio_http
        RUNTIME DESTINATION ${CMAKE_BINARY_DIR}/lib
    )
    install(DIRECTORY include/http DESTINATION ${CMAKE_BUILD_DIR}/include)
else()
    install(TARGETS asio_http
        LIBRARY DESTINATION ${CMAKE_BINARY_DIR}/lib
    )
    install(DIRECTORY include/http DESTINATION ${CMAKE_BUILD_DIR}/include)
endif()


if(true) # BUILD_EXAMPLE
    add_executable(example examples/main.cpp)
    target_link_libraries(example asio_http)
    if (CMAKE_COMPILER_IS_GNUCXX)
        set_target_properties(example PROPERTIES COMPILE_FLAGS "--coverage")
        set_target_properties(example PROPERTIES LINK_FLAGS "--coverage")
    endif()
    set_property(TARGET example PROPERTY CXX_STANDARD 11)
endif()