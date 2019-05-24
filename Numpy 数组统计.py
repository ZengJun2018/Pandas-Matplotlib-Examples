import numpy as np

a = np.array([[3, 7, 5], [8, 4, 3], [2, 4, 9]])
# 找出数组中的最大与最小值
print('我们的数组是：')
print(a)
print('\n')
print('调用 amin() 函数：')
print(np.amin(a, 1))
print('\n')
print('再次调用 amin() 函数：')
print(np.amin(a, 0))
print('\n')
print('调用 amax() 函数：')
print(np.amax(a))  # 默认将输入展开为1维
print('\n')
print('再次调用 amax() 函数：')
print(np.amax(a, axis=0))  # 在行的方向上找出最大值

# 找出最大元素与最小元素的差
print('调用 ptp() 函数：')
print(np.ptp(a))
print('\n')
print('沿轴 1 调用 ptp() 函数：')
print(np.ptp(a, axis=1))
print('\n')
print('沿轴 0 调用 ptp() 函数：')
print(np.ptp(a, axis=0))
print('--------------------------------')

# 求取百分位数
# 第p个百分位数是指，在样本中至少有p%的数据项小于或等于这个值
# 且至少有（100-p)%的数据项大于或等于这个值
a = np.array([[10, 7, 4], [3, 2, 1]])
print('我们的数组是：')
print(a)
print('调用 percentile() 函数：')
print(np.percentile(a, 50))  # 求取百分位数为50时对应的数据项
print('沿着轴0方向进行统计：')
print(np.percentile(a, 50, axis=0))
print('沿着轴1方向进行统计：')
print(np.percentile(a, 50, axis=1))
print(np.percentile(a, 50, axis=1, keepdims=True))

# 求取中位数
a = np.array([[30, 65, 70], [80, 95, 10], [50, 90, 60]])
print('我们的数组是：')
print(a)
print('\n')
print('调用 median() 函数：')
print(np.median(a))
print('\n')
print('沿轴 0 调用 median() 函数：')
print(np.median(a, axis=0))
print('\n')
print('沿轴 1 调用 median() 函数：')
print(np.median(a, axis=1))

# 求取算数平均值
a = np.array([[1, 2, 3], [3, 4, 5], [4, 5, 6]])
print('我们的数组是：')
print(a)
print('\n')
print('调用 mean() 函数：')
print(np.mean(a))
print('\n')
print('沿轴 0 调用 mean() 函数：')
print(np.mean(a, axis=0))
print('\n')
print('沿轴 1 调用 mean() 函数：')
print(np.mean(a, axis=1))

# 求取加权平均值
# 考虑数组 [1,2,3,4] 和相应的权重[4,3,2,1]
# 加权平均值 = (1*4+2*3+3*2+4*1)/(4+3+2+1)
a = np.array([1, 2, 3, 4])
print('我们的数组是：')
print(a)
print('\n')
print('调用 average() 函数：')
print(np.average(a))
print('\n')
wts = np.array([4, 3, 2, 1])
print('再次调用 average() 函数：')
print(np.average(a, weights=wts))
print('\n')
print('返回加权平均值及权重的和：')
print(np.average([1, 2, 3, 4], weights=[4, 3, 2, 1], returned=True))
# 求取多维数组的加权平均值
print('\n')
a = np.arange(6).reshape(3, 2)
print('我们的数组是：')
print(a)
print('\n')
print('沿着轴1求取加权平均值：')
wt = np.array([3, 5])
print(np.average(a, axis=1, weights=wt))
print('\n') 
print('修改后的数组：')
print(np.average(a, axis=1, weights=wt, returned=True))

# 求取标准差和方差
a = np.arange(20)
print('求标准差：')
print(np.std(a))  # 求取标准差
print('求方差：')
print(np.var(a))

print('------------------')
a = np.array([1,1,1,1,1,1,1,1,1,2,2,2,2,3,4,5,5,5])
print(a)
print(np.median(a))
print(np.percentile(a, 50))
print(np.mean(a))
