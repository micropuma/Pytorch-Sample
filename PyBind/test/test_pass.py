import mlir.ir
from mlir_ext import register_print_op_pass

with mlir.ir.Context() as ctx:
    module = mlir.ir.Module.parse("""
    func.func @main() {
        %0 = arith.constant 1 : i32
        %1 = arith.addi %0, %0 : i32
        return
    }
    """)
    pm = mlir.passmanager.PassManager.parse("builtin.module")
    register_print_op_pass(pm)
    pm.run(module)