import numpy as np
import pandas as pd

def find_missing_locations(data):
    missing_indices = np.isnan(data.astype(float))
    missing_locations = np.where(missing_indices)[0]
    return missing_locations

def find_non_numeric_locations(data):
    non_numeric_indices = np.isinf(data.astype(float))
    non_numeric_locations = np.where(non_numeric_indices)[0]
    return non_numeric_locations

# CSVファイルのパス
csv_path = r"C:\Users\newri\Desktop\vs code\kyoutei ver2\output_csv_all\Kout_ALL.csv"

# CSVファイルをDataFrameとして読み込む
df = pd.read_csv(csv_path, low_memory=False)

# 欠損値と非数値の場所を特定するために、DataFrameをNumPy配列に変換する
data = df.to_numpy()

missing_locations = find_missing_locations(data)
non_numeric_locations = find_non_numeric_locations(data)

print("欠損値の場所:", missing_locations)
print("非数値の場所:", non_numeric_locations)
