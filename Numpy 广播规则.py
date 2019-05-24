import numpy as np

# 广播 (Broadcast) 是 numpy 对不同形状 (shape) 的数组进行数值计算的方式
# 对数组的算术运算通常在相应的元素上进行。

# a.shape==b.shape，则为对应位置的元素进行计算
a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])
c = a*b
print(c)

# 形状不同时，将自动触发广播机制
a = np.array([[0, 0, 0], [10, 10, 10], [20, 20, 20], [30, 30, 30]])
b = np.array([1, 2, 3])
print(a + b)
