#include "mlir/IR/MLIRContext.h"
#include "mlir/IR/Operation.h"
#include "mlir/IR/OwningOpRef.h"
#include "mlir/Parser/Parser.h"
#include "mlir/Support/FileUtilities.h"
#include "mlir/Support/LLVM.h"
#include "llvm/Support/SourceMgr.h"
#include "llvm/Support/ToolOutputFile.h"
#include "llvm/Support/raw_ostream.h"
#include <cstdlib>
#include <string>
#include <utility>

using namespace mlir;

namespace {
class PrintOpPass : public PassWrapper<PrintOpPass, OperationPass<ModuleOp>> {
public:
  void runOnOperation() override {
    ModuleOp module = getOperation();
    module.walk([&](Operation *op) {
      llvm::outs() << "Found operation: " << op->getName() << "\n";
    });
  }
};
} // namespace

std::unique_ptr<Pass> createPrintOpPass() {
  return std::make_unique<PrintOpPass>();
}