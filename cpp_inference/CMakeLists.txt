cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(inference)

# Import torch and MonopodSDK
find_package(Torch REQUIRED)
find_package(MonopodSdk REQUIRED)

add_executable(exec-inference exec_inference.cpp)
target_link_libraries(exec-inference PUBLIC
    "${TORCH_LIBRARIES}" 
    MonopodSdk::MonopodSdk
)
set_property(TARGET exec-inference PROPERTY CXX_STANDARD 14)
