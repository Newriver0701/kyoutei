import pandas as pd

input_file = r'C:\Users\newri\Desktop\vs code\kyoutei ver2\output_csv_all\Bout_ALL.csv'
output_file = r'C:\Users\newri\Desktop\vs code\kyoutei ver2\output_csv_all\Venue_Categories.csv'

# CSVファイルを読み込む
df = pd.read_csv(input_file)

# "会場"列の値を抽出し、重複を除いてカテゴリーに分ける
categories = df['会場'].unique()

# カテゴリーごとに出現する言葉を調べる
category_words = {}
for category in categories:
    category_df = df[df['会場'] == category]
    words = category_df['会場'].unique()
    category_words[category] = words

# 結果をCSVファイルとして出力する
result_df = pd.DataFrame(category_words.items(), columns=['カテゴリー', '出現する言葉'])
result_df.to_csv(output_file, index=False)
