cd build

cmake .. -DCMAKE_BUILD_TYPE=Release \
         -DMLIR_DIR=/home/douliyang/local/LLVM/lib/cmake/mlir \
         -Dpybind11_DIR=/mnt/home/douliyang/mlsys/Pytorch-Sample/PyBind/.venv/lib/python3.11/site-packages/pybind11/share/cmake/pybind11
make -j $(nproc)
