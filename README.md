# phase1-2
shiyan

数据集主要用A1和A2，先用A2
首先解决train1阶段损失会出现负数的问题。
解读一下dataset.py的数据处理，他处理会构造一个nx的Graph外还会分训练集验证集和测试集，而且会把metric文件分time窗口，因为fault里面也有解读一下print一下看看
