from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

setup(
    name='my_kernel',
    ext_modules=[
        CUDAExtension(                    # 定义CUDA扩展，包名叫my_kernel
            name='my_kernel',
            sources=['kernel.cu', 'binding.cpp'],
        ),
    ],
    cmdclass={
        'build_ext': BuildExtension       # pytorch提供的构建扩展
    }
)
