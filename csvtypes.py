import pandas as pd
import datetime

def check_data_types(csv_file):
    # CSVファイルを読み込む
    df = pd.read_csv(csv_file)
    
    # 各列のデータ型を調べる
    data_types = df.dtypes
    
    # 結果をCSVファイルに保存する
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    result_file = f"data_types_{timestamp}.csv"  # 結果を保存するCSVファイルの名前を生成します
    data_types.to_csv(result_file)
    
    print(f"Data types have been saved to {result_file}")

# メイン関数
def main():
    csv_file = r"C:\Users\newri\Desktop\vs code\kyoutei\output_csv_all\out_merge.csv"  # CSVファイルのパスを指定してください
    check_data_types(csv_file)

if __name__ == "__main__":
    main()
