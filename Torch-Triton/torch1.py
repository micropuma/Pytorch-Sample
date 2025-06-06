import torch
import torch.library

# ======================================== Simplest version of custom operator ========================================
# Define a custom "square" operation
mylib = torch.library.Library("mylib", "DEF")

# Define the operation signature
mylib.define("square(Tensor x) -> Tensor")

# Implement the operation for CPU
@torch.library.impl(mylib, "square", "CPU")
def square_cpu(x):
    return x * x

# Now use it like any PyTorch op
x = torch.tensor([1., 2., 3.])
print(torch.ops.mylib.square(x))  # tensor([1., 4., 9.])

# ======================================== Custom operation with auto grad support ========================================
mylib.define("log1p(Tensor x) -> Tensor")

# Forward implementation
@torch.library.impl(mylib, "log1p", "CPU")
def log1p_forward(x):
    return (x+1).log()

# Backward implementation
@torch.library.impl(mylib, "log1p_backward", "AutogradCPU")
def log1p_backward(ctx, grad_output):
    x, _ = ctx.saved_tensors
    return grad_output / (x + 1)

# ======================================== GPU acceleration version ========================================
mylib.define("fast_gelu(Tensor x) -> Tensor")

@torch.library.impl(mylib, "fast_gelu", "CUDA")
def fast_gelu_cuda(x):
    # Custom CUDA kernel implementation
    return x * torch.sigmoid(1.702 * x)