import torch

a = torch.tensor([1,2,3], dtype=torch.uint8)
a - 3

torch.ops.aten.allclose.default.tags

import torch

a = torch.randn(15, device='meta')

try:
  torch.vdot(a, a)
except RuntimeError as msg:
  print(msg)

# Example 1: Extending support for an existing C++ library
from torch.library import Library, impl

# Create a library to extend an existing C++ library (in this case aten).
# All functions registered through this library would be registered
# in the aten library for the Meta dispatch key
meta_lib = Library("aten", "IMPL", "Meta")

# Register a function for torch.vdot
# This will be called when vdot is called on a Meta Tensor
@impl(meta_lib, 'vdot')
def meta_vdot(self, other):
    assert self.dim() == 1 and other.dim() == 1
    assert self.dtype == other.dtype
    assert self.numel() == other.numel()
    return self.new_empty(())

# Test the new meta support
torch.vdot(a, a)

import torch.fx
class MyModuleOld(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.param = torch.nn.Parameter(torch.rand(3, 4))
        self.linear = torch.nn.Linear(4, 5)

    def forward(self, x):
        out = self.linear(x + self.linear.weight)
        return torch.topk(torch.sum(out.relu(), dim=-1), 3)

m = MyModuleOld()
gm = torch.fx.symbolic_trace(m)
# sum and topk separately show up in the trace
print(gm.code)