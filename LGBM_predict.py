import pandas as pd
import pickle
import itertools
import os
import sys
pd.set_option('display.max_rows', 500)
import warnings
warnings.filterwarnings('ignore')

date = str(sys.argv[1])
place = str(sys.argv[2])
rno = str(sys.argv[3])


place_mapper = {
    '桐生' :1, '戸田': 2, '江戸川': 3, '平和島': 4, '多摩川':5,
    '浜名湖': 6, '蒲郡': 7, '常滑': 8, '津': 9, '三国': 10,
    'びわこ': 11, '住之江': 12, '尼崎': 13, '鳴門': 14, '丸亀':15,
    '児島': 16, '宮島': 17, '徳山': 18, '下関': 19, '若松': 20,
    '芦屋': 21, '福岡': 22, '唐津': 23, '大村':24
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
           'ボート2連率_1', 'ボート2連率_2', 'ボート2連率_3', 'ボート2連率_4', 'ボート2連率_5', 'ボート2連率_6',
]

class_mapping = {'B2':0,'B1':1,'A2':2,'A1':3}

def predict_worker(filepath):
    print(date, place, rno)

    # データセットを読み込む
    df = pd.read_csv(filepath)

    X_chokuzen = df[columns]
    place_categories = list(place_mapper)
    X_chokuzen['会場'] = pd.Categorical(X_chokuzen['会場'], categories=place_categories)
    X_chokuzen[place_categories] = pd.get_dummies(X_chokuzen['会場'])

    for q in range(1, 6+1):
        X_chokuzen['級別_'+str(q)] = X_chokuzen['級別_'+str(q)].map(class_mapping)

    
    X_chokuzen = X_chokuzen.drop(['会場', 'Round'], axis=1)
    print(X_chokuzen)


    # モデルの読み出し
    model1 = pickle.load(open('./models/trained_model_2023-10-21_1chaku.pkl', "rb"))
    model2 = pickle.load(open('./models/trained_model_2023-10-21_2chaku.pkl', "rb"))
    model3 = pickle.load(open('./models/trained_model_2023-10-21_3chaku.pkl', "rb"))


    # テストデータを予測する
    y_pred1 = model1.predict(X_chokuzen.values, num_iteration=model1.best_iteration)[0].tolist()
    y_pred2 = model2.predict(X_chokuzen.values, num_iteration=model2.best_iteration)[0].tolist()
    y_pred3 = model3.predict(X_chokuzen.values, num_iteration=model3.best_iteration)[0].tolist()

    print('y_pred = ')
    print(y_pred1)
    print(y_pred2)
    print(y_pred3)

    proba1 = pd.DataFrame(y_pred1, columns=['予想確率_1着'])
    proba2 = pd.DataFrame(y_pred2, columns=['予想確率_2着'])
    proba3 = pd.DataFrame(y_pred3, columns=['予想確率_3着'])
    proba_1to3 = pd.concat([proba1, proba2, proba3], axis=1)

    l = [1, 2, 3, 4, 5, 6]
    #l.remove(rm_boat)
    p = itertools.permutations(l, 3)
    proba_list = []
    p_list = []
    for v in p:
        No = str(v[0])  + '-' + str(v[1])  + '-' + str(v[2]) 
        _1chaku = int(v[0]) -1
        _2chaku = int(v[1]) -1
        _3chaku = int(v[2]) -1
        proba_3rentan = proba1['予想確率_1着'][_1chaku] * proba2['予想確率_2着'][_2chaku] * proba3['予想確率_3着'][_3chaku]
        #print(v, proba_3rentan)
        proba_list.append(proba_3rentan)
        p_list.append(No)

    print(p_list)

    _3rentan = pd.DataFrame(p_list, columns=['3連単'])
    proba = pd.DataFrame(proba_list, columns=['予想確率'])

    predict_df = pd.concat([_3rentan, proba], axis=1)

    proba_std = (proba - proba.mean()) / proba.std()
    predict_df['標準化値'] = proba_std
    predict_df['min-max処理値'] = (proba_std - proba_std.min()) / (proba_std.max() - proba_std.min())

    sorted_predict_df = predict_df.sort_values('min-max処理値', ascending=False)
    sorted_predict_df = sorted_predict_df.reset_index(drop=True)
    _sum= sorted_predict_df['min-max処理値'].sum()
    sorted_predict_df['予想確率[%]'] = sorted_predict_df['min-max処理値'] / _sum
    sorted_predict_df = sorted_predict_df.sort_values('予想確率[%]', ascending=False)
    sorted_predict_df = sorted_predict_df.reset_index(drop=True)

    print('{}, {}, R{}'.format(date, place, rno))
    print(proba_1to3)
    print()

    out_filedirs = f'./output/{date}_{place}'
    os.makedirs(out_filedirs, exist_ok=True)

    print(sorted_predict_df)
    sorted_predict_df.to_csv(f'{out_filedirs}/predict_{place}_R{str(rno).zfill(2)}.csv', index=None)


def main():
    filepath = f'./input/chokuzen/chokuzen_{place}_Race_{str(rno).zfill(2)}.csv'
    predict_worker(filepath)


if __name__ == '__main__':
    main()