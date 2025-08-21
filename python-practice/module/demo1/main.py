# main.py

from mymodule import *

print(public_func())     # ✅ 能用

# print(another_func())  # ❌ NameError: not defined
# print(_private_func()) # ❌ NameError: not defined

import mymodule
print(mymodule.another_func())  # ✅ 通过模块访问仍然能用
print(mymodule._private_func()) # ✅ 虽然不推荐，但依然能用
