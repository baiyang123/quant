'''
20240705
quant
https://zhuanlan.zhihu.com/p/612092672
plot
https://blog.csdn.net/weixin_47989730/article/details/124356416
https://zhuanlan.zhihu.com/p/572193380
marker="o",markersize=1,markerfacecolor="red",markeredgewidth=1,markeredgecolor="grey"
fig.set_facecolor("red")
ax.set_facecolor("blue")
图Figure和轴Axis之间的区别
figure https://blog.csdn.net/m0_74195174/article/details/136038729
SciPy的统计模块：scipy.stats
'''

import matplotlib.pyplot as plt
import numpy as np

def two_p():
    # plot 1:
    xpoints = np.array([0, 6])
    ypoints = np.array([0, 100])

    plt.subplot(1, 2, 1)
    plt.plot(xpoints, ypoints)
    plt.title("plot 1")

    # plot 2:
    x = np.array([1, 2, 3, 4])
    y = np.array([1, 4, 9, 16])

    plt.subplot(1, 2, 2)
    plt.plot(x, y)
    plt.title("plot 2")

    plt.suptitle("W3Cschool subplot Test")
    plt.show()

def one_p():
    # print(np.linspace(0.5, 25, 10))
    fig, ax = plt.subplots()
    x = np.linspace(0, 2 * np.pi, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    ax.plot(x, y1, 'b-', linewidth=2, label='sine function', alpha=0.6)
    ax.plot(x, y2, 'b-', linewidth=2, label='sine function', alpha=0.6)
    ax.legend()  # 字体
    # 准备数据
    # 设置标题和坐标轴标签
    plt.title('example')
    plt.xlabel('x')
    plt.ylabel('y')

    # 显示图形
    plt.show()

def scatter():
    N = 50
    x = np.random.rand(N)
    y = np.random.rand(N)
    colors = np.random.rand(N)

    fig, ax = plt.subplots()
    ax.scatter(x, y, s=100, c=colors, alpha=0.5)
    # 注释
    ax.annotate("First point", xy=(x[0], y[0]), xycoords="data",
                xytext=(25, -25), textcoords="offset points",
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.6"))
    plt.show()

def bar():
    countries = ["CAN", "MEX", "USA"]
    populations = [36.7, 129.2, 325.700]
    land_area = [3.850, 0.761, 3.790]

    fig, ax = plt.subplots(2)

    ax[0].bar(countries, populations, align="center")
    ax[0].set_title("Populations (in millions)")

    ax[1].bar(countries, land_area, align="center")
    ax[1].set_title("Land area (in millions miles squared)")
    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    scatter()