import numpy as np

# 对换数组的维度
a = np.arange(12).reshape(3, 4)
print(f'原数组: \n {a}')
b = np.transpose(a)  # 返回视图，类似np.ndarray.T
print(f'np.transpose(a)翻转后的数组视图: \n {b}')
c = a.T
print(f'利用np.ndarray.T翻转: \n {c}')