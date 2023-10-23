import pandas as pd

def convert_data_types(csv_file):
    # CSVファイルを読み込む
    df = pd.read_csv(csv_file)
    
    # データ型を変換する
    convert_dict = {
        "Date": "int64",
        "Round": "int64",
        "会場": "object",
        "選手登番_1": "int64",
        "選手登番_2": "int64",
        "選手登番_3": "int64",
        "選手登番_4": "int64",
        "選手登番_5": "int64",
        "選手登番_6": "int64",
        "選手名_1": "object",
        "選手名_2": "object",
        "選手名_3": "object",
        "選手名_4": "object",
        "選手名_5": "object",
        "選手名_6": "object",
        "年齢_1": "int64",
        "年齢_2": "int64",
        "年齢_3": "int64",
        "年齢_4": "int64",
        "年齢_5": "int64",
        "年齢_6": "int64",
        "支部_1": "object",
        "支部_2": "object",
        "支部_3": "object",
        "支部_4": "object",
        "支部_5": "object",
        "支部_6": "object",
        "体重_1": "int64",
        "体重_2": "int64",
        "体重_3": "int64",
        "体重_4": "int64",
        "体重_5": "int64",
        "体重_6": "int64",
        "級別_1": "object",
        "級別_2": "object",
        "級別_3": "object",
        "級別_4": "object",
        "級別_5": "object",
        "級別_6": "object",
        "全国勝率_1": "float64",
        "全国勝率_2": "float64",
        "全国勝率_3": "float64",
        "全国勝率_4": "float64",
        "全国勝率_5": "float64",
        "全国勝率_6": "float64",
        "全国2連率_1": "float64",
        "全国2連率_2": "float64",
        "全国2連率_3": "float64",
        "全国2連率_4": "float64",
        "全国2連率_5": "float64",
        "全国2連率_6": "float64",
        "当地勝率_1": "float64",
        "当地勝率_2": "float64",
        "当地勝率_3": "float64",
        "当地勝率_4": "float64",
        "当地勝率_5": "float64",
        "当地勝率_6": "float64",
        "当地2連率_1": "float64",
        "当地2連率_2": "float64",
        "当地2連率_3": "float64",
        "当地2連率_4": "float64",
        "当地2連率_5": "float64",
        "当地2連率_6": "float64",
        "モーター2連率_1": "float64",
        "モーター2連率_2": "float64",
        "モーター2連率_3": "float64",
        "モーター2連率_4": "float64",
        "モーター2連率_5": "float64",
        "モーター2連率_6": "float64",
        "ボート2連率_1": "float64",
        "ボート2連率_2": "float64",
        "ボート2連率_3": "float64",
        "ボート2連率_4": "float64",
        "ボート2連率_5": "float64",
        "ボート2連率_6": "float64",
        "結果_1着": "int64",
        "結果_2着": "int64",
        "結果_3着": "int64",
        "決まり手": "object",
        "払戻金": "int64"
    }
    
    df = df.astype(convert_dict)
    
    # 変換後のデータ型を表示する
    print("変換後のデータ型:")
    print(df.dtypes)

# メイン関数
def main():
    csv_file = r"C:\Users\newri\Desktop\vs code\kyoutei ver2\output_csv_all\Bout_ALL.csv"  # CSVファイルのパスを指定してください
    convert_data_types(csv_file)

if __name__ == "__main__":
    main()
