import pytest
import torch
import dly_gems

# shape, alpha, dtype排列组合，共4x4x3=48种情况
@pytest.mark.parametrize(
    "shape",
    [(1024, 1024), (16, 1024, 256), (16, 128, 64, 64), (20, 320, 15)],
)
@pytest.mark.parametrize("alpha", [0, 1, 4, -9])
@pytest.mark.parametrize("dtype", [torch.float16, torch.float32, torch.bfloat16])
def test_accuracy_add(shape, alpha, dtype):
    inp1 = torch.randn(shape, dtype=dtype, device="cuda")
    inp2 = torch.randn(shape, dtype=dtype, device="cuda")

    ref_out = torch.add(inp1, inp2, alpha=alpha)
    with dly_gems.use_gems():
        # 重点是如何做torch.add的替换的
        res_out = torch.add(inp1, inp2, alpha=alpha)

    maxdiff = torch.max(torch.abs(ref_out - res_out))
    assert torch.allclose(
        ref_out, res_out, atol=1e-3, rtol=1e-3
    ), f"max diff: {maxdiff}"

# shape, alpha, dtype排列组合，共4x4x3=48种情况
@pytest.mark.parametrize(
    "shape",
    [(1024, 1024), (16, 1024, 256), (16, 128, 64, 64), (20, 320, 15)],
)
@pytest.mark.parametrize("dtype", [torch.float16, torch.float32, torch.bfloat16])
def test_accuracy_abs(shape, dtype):
    inp1 = torch.randn(shape, dtype=dtype, device="cuda")

    ref_out = torch.abs(inp1)
    with dly_gems.use_gems():
        # 重点是如何做torch.add的替换的
        res_out = torch.abs(inp1) 
    maxdiff = torch.max(torch.abs(ref_out - res_out))
    assert torch.allclose(
        ref_out, res_out, atol=1e-3, rtol=1e-3
    ), f"max diff: {maxdiff}"
