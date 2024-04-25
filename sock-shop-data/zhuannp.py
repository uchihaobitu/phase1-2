import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler


def process_csv_file(csv_file):
    # 读取CSV文件
    df = pd.read_csv(csv_file)

    # 移除第一行第一列
    df = df.iloc[1:, 1:]

    # # 初始化RobustScaler
    # scaler = RobustScaler()
    #
    # # 进行归一化
    # normalized_data = scaler.fit_transform(df)
    for col in df.columns:
        df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

    df.fillna(0, inplace=True)
    # 获取文件名（不含扩展名）
    file_name = os.path.splitext(csv_file)[0]

    # 保存为.npy文件
    npy_file = file_name + ".npy"
    np.save(npy_file, df)

    return npy_file


def process_directory(directory):
    # 遍历目录下的所有文件和子目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith("normal.csv"):
                csv_file = os.path.join(root, file)
                npy_file = process_csv_file(csv_file)
                print(f"Processed: {csv_file} -> {npy_file}")


# 指定sock-shop-data的路径
directory_path = "."

# 处理指定目录下的所有CSV文件
process_directory(directory_path)
