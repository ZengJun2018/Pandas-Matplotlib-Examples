import numpy as np

dt = np.dtype([('age', np.int8)])
print(dt)
a = np.array([(10,), (20,), (30,)], dtype=dt)
print(a, a.dtype)
print(a['age'])

# 定义一个结构化数据类型student
student = np.dtype([('name', 'S20'), ('age', 'i1'), ('marks', 'f4')])
# S20 表示20字节的字符串类型
# i1 表示有符号的8位（1个字节）的整型
# f4 表示标准的单精度浮点数，与C的float兼容
print(student)
a = np.array([('abc', 21, 50),('xyz', 18, 75)], dtype = student) 
print(a)
print(a.dtype)
print(len(a))