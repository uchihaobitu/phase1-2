import pandas as pd
import matplotlib.pyplot as plt

# 加载CSV文件
df = pd.read_csv('db_003.csv')

# 遍历每一列
for column in df.columns:
    plt.figure()  # 创建一个新的图形
    plt.plot(df[column])  # 绘制列数据
    plt.title(column)  # 设置图形的标题为列名
    plt.xlabel('Index')  # 设置x轴标签
    plt.ylabel('Value')  # 设置y轴标签
    plt.show()
    # plt.savefig(f"{column}.png")  # 保存图形为PNG文件
    plt.close()  # 关闭图形以释放内存
