import pandas as pd

input_file = r'C:\Users\newri\Desktop\vs code\kyoutei ver2\output_csv_all\Bout_ALL.csv'
output_file = input_file

# CSVファイルを読み込む
df = pd.read_csv(input_file)

# 重複行を削除する
df = df.drop_duplicates(subset=['Date', 'Round', '会場'], keep=False)

# roundと会場が同じものが2つ以上ある場合、それらを削除する
df = df.groupby(['Date', 'Round', '会場']).filter(lambda x: len(x) == 1)

# 空のデータ行を削除する
df = df.dropna(how='any')

# 元のファイルを上書きする
df.to_csv(output_file, index=False)
