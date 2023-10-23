import pandas as pd
import glob

# 番組表データを1つに結合
df_concat_B = pd.DataFrame()
file_list_B = glob.glob('./output_csv_all/Bout_*.csv')
for filepath_ in file_list_B:
    print(filepath_)
    try:
        df = pd.read_csv(filepath_)
        if not df.empty:
            df_concat_B = pd.concat([df_concat_B, df], axis=0)
    except pd.errors.EmptyDataError:
        print(f"No data in file: {filepath_}")

df_concat_B.to_csv('./output_csv_all/Bout_ALL.csv', index=None)


# レース結果データを1つに結合
df_concat_K = pd.DataFrame()
file_list_K = glob.glob('./output_csv_all/Kout_*.csv')
for filepath_ in file_list_K:
    print(filepath_)
    try:
        df = pd.read_csv(filepath_)
        if not df.empty:
            df_concat_K = pd.concat([df_concat_K, df], axis=0)
    except pd.errors.EmptyDataError:
        print(f"No data in file: {filepath_}")

df_concat_K.to_csv('./output_csv_all/Kout_ALL.csv', index=None)
