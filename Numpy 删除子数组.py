import numpy as np

a = np.arange(12).reshape(3, 4)
print(f'第一个数组:\n{a}')
print('\n')
print('未传递A参数，则删除前数组将先展开：')
print(np.delete(a, 5))  # 删除了展开后下标为5的元素
print('\n')
print('可使用负数下标：')
print(np.delete(a, -1))  # 可使用负数下标
print('\n')
print('删除第2列：')
print(np.delete(a, 1, axis=1))  # 删除第2列
print('\n')
print('删除第1行：')
print(np.delete(a, 0, axis=0))  # 删除第1行
print('\n')
print('===============================================')
a = np.array([i for i in range(1, 11)]).reshape(5,2)
slice0 = np.s_[::2]  # 切片对象
print('删除切片包含的各索引对应元素：')
print(np.delete(a, slice0))
slice1 = np.s_[:2]
print('删除切片对应的行：')
print(np.delete(a, slice1, axis=0))
