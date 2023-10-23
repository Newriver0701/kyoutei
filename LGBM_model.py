import os
import lightgbm as lgb
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import pickle
import datetime

place_mapper = {
    '桐生' :1, '戸田': 2, '江戸川': 3, '平和島': 4, '多摩川':5,
    '浜名湖': 6, '蒲郡': 7, '常滑': 8, '津': 9, '三国': 10,
    '琵琶湖': 11, '住之江': 12, '尼崎': 13, '鳴門': 14, '丸亀':15,
    '児島': 16, '宮島': 17, '徳山': 18, '下関': 19, '若松': 20,
    '芦屋': 21, '福岡': 22, '唐津': 23, '大村':24
}

class_mapping = {
    'B2':0,'B1':1,'A2':2,'A1':3
}

columns = [
    'Round', 
    '会場', 
    '年齢_1', '年齢_2', '年齢_3', '年齢_4', '年齢_5', '年齢_6', 
    '体重_1', '体重_2', '体重_3', '体重_4', '体重_5', '体重_6', 
    '級別_1', '級別_2', '級別_3', '級別_4', '級別_5', '級別_6', 
    '全国勝率_1', '全国勝率_2', '全国勝率_3', '全国勝率_4', '全国勝率_5', '全国勝率_6',
    '全国2連率_1', '全国2連率_2', '全国2連率_3', '全国2連率_4', '全国2連率_5', '全国2連率_6', 
    '当地勝率_1', '当地勝率_2', '当地勝率_3', '当地勝率_4', '当地勝率_5', '当地勝率_6',
    '当地2連率_1', '当地2連率_2', '当地2連率_3', '当地2連率_4', '当地2連率_5', '当地2連率_6', 
    'モーター2連率_1', 'モーター2連率_2', 'モーター2連率_3', 'モーター2連率_4', 'モーター2連率_5', 'モーター2連率_6', 
    'ボート2連率_1', 'ボート2連率_2', 'ボート2連率_3', 'ボート2連率_4', 'ボート2連率_5', 'ボート2連率_6'
]

# 分類したいクラス数
num_class = 6

def create_additional_features(df):
    # 追加の特徴量を作成する関数
    # 例えば、特徴量Aと特徴量Bの組み合わせから新しい特徴量Cを作成する場合は、以下のように記述します
    df['特徴量C'] = df['特徴量A'] + df['特徴量B']
    # 必要な特徴量を作成してください
    return df

def feature_selection(X, Y):
    # 特徴量選択を行う関数
    # 相関分析や特徴量の重要度ランキングなどの手法を使用して、予測タスクに最も関連性の高い特徴量を選択します
    # 必要な特徴量の選択を行ってください
    return X_selected, Y

def main():
    date = str(datetime.datetime.today()).split(' ')[0]
    print(date)
    df_B = pd.read_csv('./output_csv_all/Bout_ALL.csv').query('決まり手 != "恵まれ"')
    df_K = pd.read_csv('./output_csv_all/Kout_ALL.csv') 

    df = pd.merge(df_B, df_K, how='inner', on=['Date', '会場', 'Round'])

    df.to_csv('./output_csv_all/out_merge.csv')
    print(df)   

    X = df[columns].reset_index(drop=True)
    
    # Check if all unique values in '会場' column are present in place_mapper
    missing_values = set(X['会場'].unique()) - set(place_mapper.keys())
    if missing_values:
        raise ValueError(f"Missing values in place_mapper: {missing_values}")
    
    X[list(place_mapper.keys())] = pd.get_dummies(X['会場'])
    
    # 追加の特徴量の作成
    X = create_additional_features(X)

    for q in range(1, 6+1):
        X['級別_'+str(q)] = X['級別_'+str(q)].map(class_mapping)

    X = X.drop(['会場', 'Round'], axis=1)
    print(X)

    for chaku in range(1, 3+1):
        Y = df[f'結果_{chaku}着']
        Y = Y.reset_index(drop=True)       
        Y = Y - 1

        # Load the pre-trained model if it exists
        filename = f'./models/trained_model_2023-10-21_{chaku}chaku.pkl'
        if os.path.exists(filename):
            model = pickle.load(open(filename, 'rb'))
        else:
            model = None

        # 訓練データとテストデータに分割する
        X_train, X_test, y_train, y_test = train_test_split(X.values, Y.values, test_size=0.20, shuffle=True, random_state=42)
        print("X_train = ", X_train)
        print("Y_train = ", y_train)

        # データセットを生成する
        lgb_train = lgb.Dataset(X_train, y_train)
        lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train)

        # LightGBM のハイパーパラメータ
        lgbm_params = {
            'task': 'train',
            # 多値分類問題
            'objective': 'multiclass',
            # クラス数は 1~6 
            'num_class': num_class,
            'metric': {'multi_error'},
            'early_stopping_rounds': 50,
            'boosting_type': 'dart',
            'learning_rate': 0.10,
            'verbose':-1,
            'seed': 42,
            'num_threads': 8
        }
        
        # 上記のパラメータでモデルを学習する
        model = lgb.train(lgbm_params, lgb_train,
                        valid_sets=(lgb_train, lgb_eval),
                        valid_names=["Train", "Test"],
                        num_boost_round=500,
                        verbose_eval=1,
                        init_model=model  # Initialize the model with the pre-trained model
                )

        os.makedirs('./models', exist_ok=True)
        filename = f'./models/trained_model_{date}_{chaku}chaku.pkl'
        
        pickle.dump(model, open(filename, 'wb'))

        # テストデータを予測する
        y_pred = model.predict(X_test, num_iteration=model.best_iteration)
        # 最尤と判断したクラスの値にする
        y_pred_max = np.argmax(y_pred, axis=1)  

        np.set_printoptions(threshold=np.inf)
        np.set_printoptions(precision=3)
        np.set_printoptions(suppress=True)
        print("y_predict = ")
        print(y_pred)
        print()
        y_pred_max = np.argmax(y_pred, axis=1)
        print(y_pred_max)
        
        pd.set_option('display.max_rows', 200)
        importance = pd.DataFrame(model.feature_importance(), index=X.columns, columns=['importance'])
        print(importance)
        print()

if __name__ == '__main__':
    main()
