import matplotlib.pyplot as plt
import numpy as np


a = [ i**2 for i in range(100)]
fig = plt.figure()

plt.style.use('ggplot')  # 使用样式
print(plt.style.available)

plt.tight_layout() # 设定紧凑显示

ax1 = fig.add_subplot(1,1,1)
ax1.set_title('My test matplot plot')
# --------------------------------------------------------------------
ax1.plot(np.arange(0,10,0.1), a, label = 'n**2') # lable为图例参数
ax1.set_xticks(np.arange(0,10,1))  # 设定x轴刻度，刻度的数值范围应与x轴取值范围对应
ax1.set_xlim([0, 5])  # 设定x轴数值范围
# x轴刻度个数与标签个数对应
ax1.set_xticklabels(['zero','one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eigth', 'nine', 'ten'])
ax1.set_xlabel('Stages')
# --------------------------------------------------------------------
ax1.plot([i for i in range(100)], label = 'n')

# --------------------------------------------------------------------
# 最简单的添加图例的方式，是在添加subplot时传入label参数
ax1.legend(loc='best') # 创建图例并将其放入‘最佳’位置
# print(help(ax1.legend))
# --------------------------------------------------------------------
# --------------------------------------------------------------------
plt.savefig('figpath.png', dpi=400, bbox_inches='tight', edgeclor = 'k')
# fname: 含有文件路径的字符串或python的文件型对象；图像格式由指定的推展名推断得出，如pdf，png，svg等
# dpi：图像分辨率，即每英寸点数，默认为100
# bbox_inches：图标需要保存的部分，‘tight'表示剪除周围空白部分
# format：显式设置文件格式('png', 'pdf','svg', 'ps', 'eps'...)
# facecolor/edgecolor: 图像的背景色， 默认为'w'（白色）
# --------------------------------------------------------------------
plt.show()