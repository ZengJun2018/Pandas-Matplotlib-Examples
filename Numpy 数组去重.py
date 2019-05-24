import numpy as np

a = np.array([5, 2, 6, 2, 7, 5, 6, 8, 2, 9])
print('第一个数组：')
print(a)
print('\n')
print('第一个数组去重后得到的新数组：')
u = np.unique(a)
print(u)
print('\n')
u, indices = np.unique(a, return_index=True)  # 返回新数组和列表
print('新的数组元素在旧数组中的下标：')
print(indices)
print('\n')
u, indices = np.unique(a, return_inverse=True)
print('原数组元素在新数组中的下标：')
print(indices)
print('可使用下标重构原数组：')
print(u[indices])  # 利用整数数组索引（花式索引）方法
print('\n')
print('返回重复元素的出现次数：')
u, indices = np.unique(a, return_counts=True)
print(indices)
