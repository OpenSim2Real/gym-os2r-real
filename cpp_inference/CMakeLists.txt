# find_package(Torch REQUIRED)
find_package(MonopodSdk REQUIRED)

add_executable(exec-inference exec_inference.cpp)
target_link_libraries(exec-inference PUBLIC
    # "${TORCH_LIBRARIES}"
    MonopodSdk::MonopodSdk
)

# install(exec-inference)
