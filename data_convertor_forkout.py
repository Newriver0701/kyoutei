import pandas as pd

def convert_data_types(csv_file):
    # CSVファイルを読み込む
    df = pd.read_csv(csv_file)
    
    # データ型を変換する
    df["Date"] = pd.to_datetime(df["Date"])
    df["Round"] = df["Round"].astype(int)
    df["会場"] = df["会場"].astype(str)
    df["試合タイプ"] = df["試合タイプ"].astype(str)
    df["天候"] = df["天候"].astype(str)
    df["風向"] = df["風向"].astype(str)
    df["風速"] = df["風速"].astype(int)
    df["波高"] = df["波高"].astype(int)
    df["選手登番_1"] = df["選手登番_1"].astype(int)
    df["選手登番_2"] = df["選手登番_2"].astype(str)
    df["選手登番_3"] = df["選手登番_3"].astype(str)
    df["選手登番_4"] = df["選手登番_4"].astype(str)
    df["選手登番_5"] = df["選手登番_5"].astype(str)
    df["選手登番_6"] = df["選手登番_6"].astype(str)
    df["選手名_1"] = df["選手名_1"].astype(str)
    df["選手名_2"] = df["選手名_2"].astype(str)
    df["選手名_3"] = df["選手名_3"].astype(str)
    df["選手名_4"] = df["選手名_4"].astype(str)
    df["選手名_5"] = df["選手名_5"].astype(str)
    df["選手名_6"] = df["選手名_6"].astype(str)
    df["展示タイム_1"] = df["展示タイム_1"].astype(float)
    df["展示タイム_2"] = df["展示タイム_2"].astype(float)
    df["展示タイム_3"] = df["展示タイム_3"].astype(float)
    df["展示タイム_4"] = df["展示タイム_4"].astype(float)
    df["展示タイム_5"] = df["展示タイム_5"].astype(float)
    df["展示タイム_6"] = df["展示タイム_6"].astype(float)
    df["スタートタイム_1"] = df["スタートタイム_1"].astype(float)
    df["スタートタイム_2"] = df["スタートタイム_2"].astype(float)
    df["スタートタイム_3"] = df["スタートタイム_3"].astype(float)
    df["スタートタイム_4"] = df["スタートタイム_4"].astype(float)
    df["スタートタイム_5"] = df["スタートタイム_5"].astype(float)
    df["スタートタイム_6"] = df["スタートタイム_6"].astype(float)
    df["進入順位_1"] = df["進入順位_1"].astype(float)
    df["進入順位_2"] = df["進入順位_2"].astype(float)
    df["進入順位_3"] = df["進入順位_3"].astype(float)
    df["進入順位_4"] = df["進入順位_4"].astype(float)
    df["進入順位_5"] = df["進入順位_5"].astype(float)
    df["進入順位_6"] = df["進入順位_6"].astype(float)
    
    # 変換後のデータ型を表示する
    print("変換後のデータ型:")
    print(df.dtypes)

# メイン関数
def main():
    csv_file = "C:\\Users\\newri\\Desktop\\vs code\\kyoutei ver2\\output_csv_all\\Kout_ALL.csv"  # CSVファイルのパスを指定してください
    convert_data_types(csv_file)

if __name__ == "__main__":
    main()
