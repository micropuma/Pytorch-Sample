import itertools
import torch
import time
import triton
import random
from dly_gems import *

# 10次预热，1000次重复
# 计算平均时间
def run_bench(op, *args, warmups=10, repetitions=1000, **kwargs):
    for i in range(warmups):
        ref_out = op(*args, **kwargs)
    start = time.time()
    for i in range(repetitions):
        ref_out = op(*args, **kwargs)
    torch.cuda.synchronize()
    end = time.time()
    ms = (end - start) * 1000
    return ms


class Benchmark:
    def __init__(self, op_name):
        self.op_name = op_name

    def provider_ops(self, gem=None, torch=None):
        assert gem is not None
        assert torch is not None
        self.provider_ops = {"gem": gem, "torch": torch}

    def bench_params(self, **params):
        self.bench_params = params

    def arg_names(self, *arg_names):
        self.x_names = arg_names

    def arg_vals(self, arg_vals):
        self.x_vals = arg_vals

    def extra_args(self, **args):
        self.extra_args = args

    # 核心装饰器
    def perf(self, fn):
        line_names, line_vals = zip(*self.provider_ops.items())
        bench_param_names, bench_param_vals = zip(*self.bench_params.items())
        benchmarks = (
            triton.testing.Benchmark(
                x_names=self.x_names,
                x_vals=self.x_vals,
                line_arg="op",
                line_names=list(line_names),
                line_vals=list(line_vals),
                styles=[("red", "-"), ("green", "-")],
                ylabel="ms",
                plot_name="test_performance_{}_{}".format(
                    self.op_name, "_".join(str(e) for e in bench_param_set)
                ),
                args={
                    **self.extra_args,
                    **dict(zip(bench_param_names, bench_param_set)),
                },
            )
            for bench_param_set in itertools.product(*bench_param_vals)
        )
        return triton.testing.perf_report(benchmarks)(fn)


f16_f32_bf = (torch.float16, torch.float32, torch.bfloat16)
sizes = [i * 64 for i in range(1, 20)]
mnk_sizes = list(zip(sizes, sizes, sizes))

add_bench = Benchmark("add")
add_bench.bench_params(dtype=f16_f32_bf)
add_bench.provider_ops(gem=add, torch=torch.add)
add_bench.arg_names("N")
add_bench.arg_vals(sizes)
add_bench.extra_args(M=1024)

@add_bench.perf
def bench_add(op, M, N, dtype):
    inp1 = torch.randn((M, N), dtype=dtype, device="cuda")
    inp2 = torch.randn((M, N), dtype=dtype, device="cuda")
    alpha = random.random()
    ms = run_bench(op, inp1, inp2, alpha=alpha)
    return ms


@add_bench.perf
def bench_add_scalar(op, M, N, dtype):
    inp1 = torch.randn((M, N), dtype=dtype, device="cuda")
    inp2 = random.random()
    alpha = random.random()
    ms = run_bench(op, inp1, inp2, alpha=alpha)
    return ms

bench_add.run(print_data=True)
bench_add_scalar.run(print_data=True)
