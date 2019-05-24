# 修改数组形状

import numpy as np

# 重塑数组形状
a = np.arange(8)
print(f'原数组: \n {a}')
b = a.reshape([4, 2])
print(f'修改后的数组: \n {b}')
print('------------------------')

# 数组迭代器
a = np.arange(9).reshape(3, -1)  # 参数-1表示该值由数组本身推断，本例中实际为3
print(f'原数组: \n {a}')
print('对数组的行进行迭代:')
for row in a:
    print(row)
print('对数组元素进行迭代:')
for element in a.flat:
    print(element, end=' ')
print('------------------------')

# 数组的扁平化(flatten)或散开(ravel)
a = np.arange(8).reshape(2, 4)
print(f'原数组: \n {a}')
b = a.flatten()  # 返回新的数组
print(f'扁平化（flatten)后的数组: \n {b}')

c = a.ravel()  # 返回数组视图
print(f'散开（ravel)后的数组: \n {c}')
c[:] = 0
print(f'散开的数组置零后：\n {a}')

