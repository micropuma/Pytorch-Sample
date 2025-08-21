from collections import deque

def demo():
    print("==== Python 数据结构 Demo ====\n")

    # 1. 列表 list（有序，可变，允许重复）
    numbers = [1, 2, 3, 3]
    numbers.append(4)       # 添加
    numbers.remove(2)       # 删除
    print("list:", numbers)  # [1, 3, 3, 4]

    # 2. 元组 tuple（有序，不可变，允许重复）
    point = (10, 20)
    print("tuple:", point)  # (10, 20)
    # point[0] = 100  # ❌ 不允许修改

    # 3. 字典 dict（键值对，键唯一）
    student = {
        "id": 101,
        "name": "Alice",
        "score": 95
    }
    student["score"] = 98   # 修改值
    student["grade"] = "A"  # 添加键值
    print("dict:", student)

    # 4. 集合 set（无序，不重复）
    fruits = {"apple", "banana", "orange"}
    fruits.add("banana")  # 重复元素不会增加
    fruits.add("pear")
    print("set:", fruits)

    # 5. 字符串 str（不可变序列）
    text = "hello world"
    print("str:", text.upper(), "| contains 'world'?", "world" in text)

    # 6. 双端队列 deque（高效的两端操作）
    dq = deque([1, 2, 3])
    dq.appendleft(0)   # 左侧插入
    dq.append(4)       # 右侧插入
    dq.pop()           # 右侧删除
    dq.popleft()       # 左侧删除
    print("deque:", dq)

    # 7. 组合：常见用法 - 列表里放字典
    students = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ]
    print("list of dicts:", students)

if __name__ == "__main__":
    demo()
