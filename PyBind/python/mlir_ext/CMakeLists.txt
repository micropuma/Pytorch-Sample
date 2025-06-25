add_library(_mlir_ext SHARED bindings.cpp)
target_link_libraries(_mlir_ext PUBLIC Passes pybind11::module MLIRPass)
set_target_properties(_mlir_ext PROPERTIES PREFIX "" SUFFIX ".so")