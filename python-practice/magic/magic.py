"""
    This python file contains all sorts of python magic methods.
    Refer to https://realpython.com/python-magic-methods/
"""

"""
    demo1:
    __init__魔法方法，初始化对象实例
"""
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

point = Point(23, 34)
print(point.x)
print(point.y)

"""
    demo2:
    __magic__魔法方法，实例化对象，先于__init__执行
    下面示例演示__new__的应用场景，在不可变对象的创建中，只能在构建阶段确定值。
    计算重载，__add__
"""
class Storage(float):
    def __new__(cls, value, unit):
        instance = super().__new__(cls, value)
        instance.unit = unit
        return instance
    
    def __add__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError(
                "unsupported operand for +: "
                f"'{type(self).__name__}' and '{type(other).__name__}'"
            )
        if not self.unit == other.unit:
            raise TypeError(
                f"incompatible units: '{self.unit}' and '{other.unit}'"
            )

        return type(self)(super().__add__(other), self.unit)

disk = Storage(1024, "GB")
disk_2 = Storage(1000, "GB")
print(disk+disk_2)
# print(disk+100)

print(disk)

print(disk.unit)

"""
    demo3:
    用户友好print：__str()__
    开发者友好print：__repr()__，要求无歧义，甚至开发者可以根据这个string重新创建对象
"""
class Person:
    def __init__(self, age, name):
        self.age =age
        self.name = name
    
    def __str__(self):
        return f"I'm {self.name}, and I'm {self.age} years old."

    def __repr__(self):
        return f"{type(self).__name__}(name='{self.name}', age={self.age})"
    
jane = Person("Jane Doe", 25)
print(jane)
print(str(jane))
print(repr(jane))

"""
    demo4:
    Arithmetic operators
"""
class Distance:  
    _multiples = {       # 一个字典
        "mm": 0.001,
        "cm": 0.01,
        "m": 1,
        "km": 1000,
    }

    def __init__(self, value, unit="m"):
        self.value = value
        self.unit = unit

    def _to_meter(self):
        return self.value * type(self)._multiples[self.unit]
    
    def _compute(self, other, operator):     # 使用eval()函数动态计算
        operation = eval(f"{self._to_meter()} {operator} {other._to_meter()}")    # 计算结果result
        cls = type(self)
        return cls(operation / cls._multiples[self.unit], self.unit)

    def __add__(self, other):
        return self._compute(other, "+")

    def __sub__(self, other):
        return self._compute(other, "-")

distance_1 = Distance(300, "km")
distance_2 = Distance(150, "m")
distance_3 = distance_1 + distance_2
distance_4 = distance_1 - distance_2

print(distance_3.value, distance_3.unit)
print(distance_4.value, distance_4.unit)    

"""
    demo5:
    探索demo4中为啥需要type？
"""
class Length:
    _multiples = {"m": 1, "cm": 0.01}

    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

    def to_meter(self):
        return self.value * type(self)._multiples[self.unit]
    
    def to_meter_wrong(self):
        return self.value * self._multiples[self.unit]


class LengthInMM(Length):
    _multiples = {"mm": 0.001}

a = LengthInMM(100, "mm")
print(type(a))                # <class '__main__.LengthInMM'>
print(a.to_meter())           # 0.1 （用子类的 _multiples）
print(a.to_meter_wrong())     # KeyError: 'mm' （用父类的 _multiples）

"""
    demo6:
    self是左边的operand还是右边的operand
"""
class Number:
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        print("__add__ called")
        if isinstance(other, Number):
            return Number(self.value + other.value)
        elif isinstance(other, int | float):
            return Number(self.value + other)
        else:
            raise TypeError("unsupported operand type for +")

    def __radd__(self, other):
        print("__radd__ called")
        return self.__add__(other)
 
"""
    demo7:
    membership 操作
"""
class Stack:
    def __init__(self, items):
        self.items = list(items) if items is not None else []
    
    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop() 

    # 判断item是否在stack中
    def __contains__(self, item):
        # 更加简洁的实现方式：
        # return item in self.items
        for _item in self.items:
            if item == _item:
                return True 
        return False
    
stacks = Stack([2, 3, 5, 9, 7])
print(2 in stacks)
print(10 in stacks)
print(10 not in stacks)

"""
    类属性获取操作
"""

"""
    Python has two methods to handle attribute access. 
    The .__getattribute__() method runs on every attribute access, 
    while the .__getattr__() method only runs if the target attribute doesn’t exist in the current object.
"""
import math

class Circle:
    def __init__(self, radius):
        self.radius = radius

    def __getattribute__(self, name):
        print(f"__getattribute__ called for {name}")
        return super().__getattribute__(name)

    def __getattr__(self, name):
        print(f"__getattr__ called for {name}")
        if name == "diameter":
            return self.radius * 2
        return super().__getattr__(name)
    
circle = Circle(10)

# 1. __getattribute__ failed to find diameter
# 2. __getattr__ find it
# 3. self.radius * 2 call __getattribute__，and find it
print(circle.diameter)
print(circle.radius)







