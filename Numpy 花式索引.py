import numpy as np

x = np.arange(32).reshape((8,4))
print(x)
print('\n')
print('利用整数数组选取指定的行：')
print(x[[4, 2, 1, 7]])
print('\n')
print('可使用倒序索引数组:')
print(x[[-4, -2, -1, -7]])
print('\n')
print('使用多个索引数组：')
slice0 = np.ix_([1, 5, 7, 2], [0, 3, 1, 2])
#print(type(slice0))
print(slice0)
# 生成数组元素在原数组的索引：
# 行向量[1, 5, 7, 2]与列向量[0, 3, 1, 2]的乘积
print(x[slice0])
