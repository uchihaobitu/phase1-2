import pandas as pd
import numpy as np
import os

def drop_constant(df: pd.DataFrame):
    return df.loc[:, (df != df.iloc[0]).any()]

def convert_mem_mb(df: pd.DataFrame):
    def update_mem(x):
        if not x.name.endswith("_mem"):
            return x
        x /= 1e6
        return x
    return df.apply(update_mem)

def preprocess(data):
    # data = drop_constant(data)
    data = convert_mem_mb(data)
    return data


def min_max_scale(data):
    for c in data.columns[1:]:  # 跳过第一列
        min_val = np.min(data[c])
        max_val = np.max(data[c])
        if max_val != min_val:  # 防止除以零的情况
            data[c] = (data[c] - min_val) / (max_val - min_val)
        else:
            data[c] = 0  # 如果最大值和最小值相等，整列应设置为0（或其他适当的默认值）
    return data


def process_files(directory):
    for root, dirs, files in os.walk(directory):
        if "simple_data.csv" in files and "inject_time.txt" in files:
            csv_path = os.path.join(root, "simple_data.csv")
            txt_path = os.path.join(root, "inject_time.txt")

            data = pd.read_csv(csv_path)
            with open(txt_path, 'r') as f:
                inject_time = float(f.read().strip())

            # Filter data based on time
            data = data[data['time'] < inject_time]

            # Replace infinities
            data.replace([np.inf, -np.inf], np.nan, inplace=True)

            # Handle na
            data.ffill(inplace=True)
            data.fillna(0, inplace=True)

            if data.isnull().values.any():
                print(f"File has NaN values: {csv_path}")
            if data.isin([np.inf, -np.inf]).values.any():
                print(f"File has infinity values: {csv_path}")



            # Remove columns ending with 'latency-50'
            data = data.loc[:, ~data.columns.str.endswith("latency-50")]

            # Rename columns ending with '_latency-90'
            data = data.rename(columns={c: c.replace("_latency-90", "_latency") for c in data.columns if c.endswith("_latency-90")})

            # Further preprocessing
            data = preprocess(data)

            data = min_max_scale(data)
            # Save the processed data
            data.to_csv(os.path.join(root, "norm_data.csv"), index=False)
            np_data = data.iloc[1:, 1:].to_numpy()  # 从第二行和第二列开始
            np.save(os.path.join(root, "norm_data.npy"), np_data)


# Replace 'path_to_your_directory' with the path to your directory containing the files
process_files('F:/Axiaolunwen/datasets/fse-ss/fse-ss')
