import pandas as pd

def compare_data_types(csv_file1, csv_file2):
    # CSVファイルを読み込む
    df1 = pd.read_csv(csv_file1)
    df2 = pd.read_csv(csv_file2)
    
    # 各列のデータ型を調べる
    data_types1 = df1.dtypes
    data_types2 = df2.dtypes
    
    # データ型が異なる部分を判別する
    diff_columns = []
    for column in data_types1.index:
        if data_types1[column] != data_types2[column]:
            diff_columns.append(column)
    
    # 結果を表示する
    if len(diff_columns) > 0:
        print("データ型が異なる列:")
        for column in diff_columns:
            print(column)
    else:
        print("データ型はすべて一致しています。")

# メイン関数
def main():
    csv_file1 = "C:\\Users\\newri\\Desktop\\vs code\\kyoutei ver2\\output_csv_all\\Kout_ALL.csv"  # 1つ目のCSVファイルのパスを指定してください
    csv_file2 = r"C:\Users\newri\Desktop\vs code\kyoutei ver2\data\2014\Kout_ALL.csv"  # 2つ目のCSVファイルのパスを指定してください
    compare_data_types(csv_file1, csv_file2)

if __name__ == "__main__":
    main()
