cmake_minimum_required(VERSION 3.15)
project(minimal_mlir_pass)

# 查找 MLIR 和 pybind11
find_package(MLIR REQUIRED)
find_package(pybind11 REQUIRED)

find_package(MLIR REQUIRED CONFIG)
message(STATUS "MLIR found: ${MLIR_DIR}")
message(STATUS "MLIR CMake directory: ${MLIR_CMAKE_DIR}")

find_package(LLVM REQUIRED CONFIG)
message(STATUS "LLVM found: ${LLVM_DIR}")
message(STATUS "LLVM CMake directory: ${LLVM_CMAKE_DIR}")

list(APPEND CMAKE_MODULE_PATH "${MLIR_CMAKE_DIR}")
list(APPEND CMAKE_MODULE_PATH "${LLVM_CMAKE_DIR}")

message(STATUS "CMAKE_MODULE_PATH: ${CMAKE_MODULE_PATH}")

include(TableGen)
include(AddLLVM)
include(AddMLIR)
include(HandleLLVMOptions)

include_directories(${LLVM_INCLUDE_DIRS} ${MLIR_INCLUDE_DIRS})

# 输出包含目录信息
message(STATUS "LLVM include directories: ${LLVM_INCLUDE_DIRS}")
message(STATUS "MLIR include directories: ${MLIR_INCLUDE_DIRS}")

# 添加 Pass 库
add_subdirectory(passes)

# 添加 Python 绑定
add_subdirectory(python/mlir_ext)

# 测试
enable_testing()
add_test(NAME test_pass COMMAND python ${PROJECT_SOURCE_DIR}/test/test_pass.py)