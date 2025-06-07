import torch
from .add import add
from .abs import abs

# 定义aten library，其中aten已有，IMPL表示operator覆盖实现
aten_lib = torch.library.Library("aten", "IMPL")

# enable用于注册自定义的operator操作，目前是add操作
def enable(lib=aten_lib):
    # 典型的注册操作，包含：操作名，操作函数实现和dispatch key
    # dispatch key可以参考http://blog.ezyang.com/2020/09/lets-talk-about-the-pytorch-dispatcher/
    lib.impl("add.Tensor", add, "CUDA")
    lib.impl("abs", abs, "CUDA")

# 定义一个类，支持use_gems作为上下文管理器
class use_gems:
    def __init__(self):
        self.lib = torch.library.Library("aten", "IMPL")

    def __enter__(self):
        enable(self.lib)

    # 注意，exit需要四个参数
    # 执行类型（捕获异常），执行值，执行回调函数
    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.lib