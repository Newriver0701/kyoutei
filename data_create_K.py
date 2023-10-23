import re
import pandas as pd
import glob
import mojimoji
import os
import multiprocessing
import time

os.makedirs('./output_csv_all', exist_ok=True)

place_mapper = {
    '桐生': 1, '戸田': 2, '江戸川': 3, '平和島': 4, '多摩川': 5,
    '浜名湖': 6, '蒲郡': 7, '常滑': 8, '津': 9, '三国': 10,
    'びわこ': 11, '住之江': 12, '尼崎': 13, '鳴門': 14, '丸亀': 15,
    '児島': 16, '宮島': 17, '徳山': 18, '下関': 19, '若松': 20,
    '芦屋': 21, '福岡': 22, '唐津': 23, '大村': 24
}

columns = [
    'Date', 'Round', '会場',
    '試合タイプ', '天候', '風向', '風速', '波高',
    '選手登番_1', '選手登番_2', '選手登番_3', '選手登番_4', '選手登番_5', '選手登番_6',
    '選手名_1', '選手名_2', '選手名_3', '選手名_4', '選手名_5', '選手名_6',
    '展示タイム_1', '展示タイム_2', '展示タイム_3', '展示タイム_4', '展示タイム_5', '展示タイム_6',
    'スタートタイム_1', 'スタートタイム_2', 'スタートタイム_3', 'スタートタイム_4', 'スタートタイム_5', 'スタートタイム_6',
    '進入順位_1', '進入順位_2', '進入順位_3', '進入順位_4', '進入順位_5', '進入順位_6'
]

dic = {str(x): x for x in range(5)}

columns3_ = {}
for x in range(0, len(columns)):
    columns3_.update({x: columns[x]})


def worker_K(no, filepath):
    print(filepath)
    df_output_all = pd.DataFrame()
    for filename in filepath:
        df = pd.read_csv(filename)
        for i in range(0, len(df), 6):
            df_output = pd.DataFrame()
            df_one_race = df[i:i + 6].sort_values('艇番', ascending=True).reset_index()
            print(df_one_race)

            date = pd.DataFrame([df_one_race['Date'][0]])
            race = pd.DataFrame([df_one_race['Round'][0]])
            place = pd.DataFrame([df_one_race['会場'][0]])
            data_battle_type = pd.DataFrame([df_one_race['試合タイプ'][0]])
            data_weather = pd.DataFrame([df_one_race['天候'][0]])
            data_wind_dir = pd.DataFrame([df_one_race['風向'][0]])
            data_wind = pd.DataFrame([df_one_race['風速'][0]])
            data_wave = pd.DataFrame([df_one_race['波高'][0]])
            df_output = pd.concat([df_output, date, race, place, data_battle_type, data_weather, data_wind_dir, data_wind, data_wave], axis=0)

            data_toban = df_one_race['選手登番']
            data_name = df_one_race['選手名']
            data_tenji = df_one_race['展示タイム'].rank()
            data_start_time = df_one_race['スタートタイム'].rank()
            data_sinnyuu = df_one_race['進入順位']

            df_output = pd.concat([df_output, data_toban, data_name, data_tenji, data_start_time, data_sinnyuu], axis=0).T
            sh = df_output.shape
            df_output.columns = range(sh[1])  # 列名のインデックスを振り直し
            df_output_all = pd.concat([df_output_all, df_output], axis=0)
            df_output_all_new = df_output_all.rename(columns=columns3_)

            df_output_all_new.to_csv('./output_csv_all/Kout_' + str(no) + '.csv', index=None)


if __name__ == '__main__':
    filepath_K = sorted(glob.glob('./output_csv/out_K_*.csv'))
    print(filepath_K)
    time.sleep(3)

    process_num = 13
    processes = []
    for ii in range(1, process_num + 1):
        # マルチプロセスで高速処理
        p = multiprocessing.Process(target=worker_K, args=(ii, filepath_K[(ii - 1) * 30:ii * 30]))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
