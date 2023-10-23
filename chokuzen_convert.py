import pandas as pd
import glob
import sys

place_mapper = {
    '桐生' :1, '戸田': 2, '江戸川': 3, '平和島': 4, '多摩川':5,
    '浜名湖': 6, '蒲郡': 7, '常滑': 8, '津': 9, '三国': 10,
    'びわこ': 11, '住之江': 12, '尼崎': 13, '鳴門': 14, '丸亀':15,
    '児島': 16, '宮島': 17, '徳山': 18, '下関': 19, '若松': 20,
    '芦屋': 21, '福岡': 22, '唐津': 23, '大村':24
}

columns = [
           'Date', 
           'Round', 
           '会場', 
           '選手登番_1', '選手登番_2', '選手登番_3', '選手登番_4', '選手登番_5', '選手登番_6',
           '選手名_1', '選手名_2', '選手名_3', '選手名_4', '選手名_5', '選手名_6', 
           '年齢_1', '年齢_2', '年齢_3', '年齢_4', '年齢_5', '年齢_6', 
           '支部_1', '支部_2', '支部_3', '支部_4', '支部_5', '支部_6', 
           '体重_1', '体重_2', '体重_3', '体重_4', '体重_5', '体重_6', 
           '級別_1', '級別_2', '級別_3', '級別_4', '級別_5', '級別_6', 
           '全国勝率_1', '全国勝率_2', '全国勝率_3', '全国勝率_4', '全国勝率_5', '全国勝率_6',
           '全国2連率_1', '全国2連率_2', '全国2連率_3', '全国2連率_4', '全国2連率_5', '全国2連率_6', 
           '当地勝率_1', '当地勝率_2', '当地勝率_3', '当地勝率_4', '当地勝率_5', '当地勝率_6',
           '当地2連率_1', '当地2連率_2', '当地2連率_3', '当地2連率_4', '当地2連率_5', '当地2連率_6', 
           'モーター2連率_1', 'モーター2連率_2', 'モーター2連率_3', 'モーター2連率_4', 'モーター2連率_5', 'モーター2連率_6', 
           'ボート2連率_1', 'ボート2連率_2', 'ボート2連率_3', 'ボート2連率_4', 'ボート2連率_5', 'ボート2連率_6',

           '進入順位_1', '進入順位_2', '進入順位_3', '進入順位_4', '進入順位_5', '進入順位_6'
]

dic = {str(x):x for x in range(5)}

columns_rename = {}
for x in range(0, len(columns)):
    columns_rename.update({x: columns[x] })

print(columns_rename)



folder = './input/chokuzen'
filepath = sorted(glob.glob(folder + '/chokuzen_*.csv'))
print(filepath)

for filename in filepath:
    df = pd.read_csv(filename)
    for i in range(0, len(df), 6):
        df_output = pd.DataFrame()
        df_one_race = df[i:i+6].reset_index()
        print(df_one_race)

        date = pd.DataFrame([df_one_race['Date'][0]])
        race = pd.DataFrame([df_one_race['Round'][0]])
        place = pd.DataFrame([df_one_race['会場'][0]])
        for key, value in place_mapper.items():
            if str(key) == str(place.iat[0, 0]):
                placeNo = value
                print('placeNo = ', placeNo)
                print('place = ', place)
                break

        #print(date)
        #print(race)
        #print(place)
        df_output = pd.concat([df_output, date, race, place], axis=0)

        data_toban = df_one_race['選手登番']
        data_name = df_one_race['選手名']
        data_age = df_one_race['年齢'] #.rank()
        data_shibu = df_one_race['支部']
        data_weight = df_one_race['体重'] #.rank()
        
        data_kyubetsu = df_one_race['級別']
        data_zenkoku_shoritsu = df_one_race['全国勝率'] #.rank(ascending=False)
        data_zenkoku_2ren = df_one_race['全国２連率'] #.rank(ascending=False)
        data_touchi_shouritsu = df_one_race['当地勝率'] #.rank(ascending=False)
        data_touchi_2ren = df_one_race['当地２連率'] #.rank(ascending=False)
        data_motor_2ren = df_one_race['モーター２連率'] #.rank(ascending=False)
        data_boat_2ren = df_one_race['ボート２連率'] #.rank(ascending=False)


        df_output = pd.concat([df_output, data_toban, data_name, data_age, data_shibu, data_weight, data_kyubetsu,
                            data_zenkoku_shoritsu, data_zenkoku_2ren, 
                            data_touchi_shouritsu, data_touchi_2ren,
                            data_motor_2ren, data_boat_2ren], axis=0).T
        print(df_output)

        sh = df_output.shape
        df_output.columns = range(sh[1]) # 列名のインデックスを振り直し
        df_output_new = df_output.rename(columns=columns_rename)
    
    df_output_new.to_csv('./input/chokuzen/chokuzen_'+ str(place.iat[0, 0]) + '_Race_' + str(race.iat[0, 0]).zfill(2) +'.csv', index=None)

