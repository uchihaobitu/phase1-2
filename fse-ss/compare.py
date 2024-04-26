import pandas as pd
import os

def compare_csv_columns(directory):
    for root, dirs, files in os.walk(directory):
        compare_file_path = os.path.join(root, "compare_data.csv")
        norm_file_path = os.path.join(root, "norm_data.csv")

        # 确保两个文件都存在
        if "compare_data.csv" in files and "norm_data.csv" in files:
            compare_data = pd.read_csv(compare_file_path)
            norm_data = pd.read_csv(norm_file_path)

            # 检查列数是否一致
            compare_columns_count = len(compare_data.columns)
            print(compare_columns_count)
            norm_columns_count = len(norm_data.columns)
            print(norm_columns_count)
            if compare_columns_count != norm_columns_count:
                print(f"Column number mismatch in {root}")
                print(f"  Compare data columns count: {compare_columns_count}")
                print(f"  Norm data columns count: {norm_columns_count}")
                continue  # 继续下一个循环迭代

            # 检查列名是否完全一致
            if not all(compare_data.columns == norm_data.columns):
                print(f"Column name mismatch in {root}")
                print(f"  Compare data columns: {compare_data.columns.tolist()}")
                print(f"  Norm data columns: {norm_data.columns.tolist()}")

# 替换路径为你的实际目录
compare_csv_columns('F:/Axiaolunwen/datasets/fse-ss/fse-ss')
