#include <pybind11/pybind11.h>
#include "mlir/Pass/PassManager.h"
#include "PrintOpPass.h"  // 包含 Pass 头文件

namespace py = pybind11;

void registerPasses(py::module &m) {
  m.def("register_print_op_pass", [](mlir::PassManager &pm) {
    pm.addPass(createPrintOpPass());  // 将 Pass 添加到 PassManager
  });
}

PYBIND11_MODULE(_mlir_ext, m) {
  m.doc() = "Minimal MLIR Pass Bindings";
  registerPasses(m);
}